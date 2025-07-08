#!/usr/bin/env python3
"""Generate python code from Epic EOS SDK API."""

import json
import logging
import re
import sys
from .entries import CallbackEntry, DefineEntry, EnumEntry, FunctionEntry, StructEntry, TypedefEntry
from .mapper import Mapper

logger = logging.getLogger(__name__)

# A mapping from a type to the corresponding ctypes constructor.
INITIAL_MAPPINGS = {
    "char" : "c_char",
    "char*" : "c_char_p",
    "void*" : "c_void_p",
    "uint64_t": "c_uint64",
    "uint32_t": "c_uint32",
    "uint16_t": "c_uint16",
    "uint8_t": "c_uint8",
    "int16_t" : "c_int16",
    "int32_t" : "c_int32",
    "int64_t" : "c_int64",
    "double": "c_double",
    "float": "c_float",
    "size_t": "c_size_t"
}

FILE_START = '''
# pylint: disable

from ctypes import (
    Array, Structure, Union, CFUNCTYPE, POINTER,
    c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64,
    c_char, c_char_p, c_void_p, c_float, c_double, c_size_t,
    )

try:
    from typing import Any
except ImportError:
    pass

def not_ready(*args): # type: (...) -> Any
    raise RuntimeError("Please call epic_eos.cdefs.load() before this function.")

PACK = 8
'''

SPEC_ENTRIES = (
    ('defines', DefineEntry),
    ('enums', EnumEntry),
    ('typedefs', TypedefEntry),
    ('callback_methods', CallbackEntry),
    ('structs', StructEntry),
    ('functions', FunctionEntry),
)

class SpecManager():
    """Entrypoint for spec generation."""
    def __init__(self, mappings = None):
        self.file_entries = []
        self.mapper = Mapper(mappings if mappings is not None else INITIAL_MAPPINGS.copy())
        self.metadata = {}

    def ingest_spec(self, spec):
        """Main entrypoint"""
        entries = []
        functions_index = {}
        enum_types_structs_index = {}
        # Initialize entries list & create indexes for later use
        for key, classobject in SPEC_ENTRIES:
            for f in spec[key]:
                obj = classobject(f)
                entries.append(obj)
                if key == 'functions':
                    assert obj.name not in functions_index
                    functions_index[obj.name] = obj
                if key in ('enums', 'typedefs', 'structs'):
                    assert obj.name not in enum_types_structs_index
                    enum_types_structs_index[obj.name] = obj

        # Helper function that adds an entry to the class's entries
        # and returns whether the entry was not added to allow to
        # filter it out below.
        def record(entry):
            if all(self.mapper.is_indexed(r) for r in entry.requires()):
                self.mapper.update(entry.provides())
                for k, v in entry.provides_defaults(self.mapper).items():
                    self.mapper.add_ctype_default(k, v)
                self.file_entries.append(entry)
                return False
            return True

        last_len = len(entries)
        while entries:
            entries = [*filter(record, entries)]
            if len(entries) == last_len:
                # We failed to remove any records this round, this should never happen
                logging.debug(json.dumps([{
                    'name': e.name,
                    'class': e.__class__.__name__,
                    'req': e.requires(),
                    'missing': [m for m in e.requires() if not self.mapper.is_indexed(m)],
                } for e in entries], indent = 2))
                raise Exception(f"Failed to sort {len(entries)} entries.")
            last_len = len(entries)

        # Associate each function to its corresponding class
        for funcname, function in functions_index.items():
            base_split_name = funcname.split('_')
            for i in range(2, len(base_split_name))[::-1]:
                found = False
                # Match from the function's name or from its "handle" version
                for split_name in (base_split_name[:i], (base_split_name[0], f'H{base_split_name[1]}', *base_split_name[2:i])):
                    contextname = '_'.join(split_name)
                    if contextname in enum_types_structs_index:
                        obj = enum_types_structs_index[contextname]
                        local_name = '_'.join(base_split_name[i:])
                        is_static = contextname in function.returntype
                        obj.add_function(function, local_name, is_static)
                        found = True
                        break
                if found:
                    break
            else:
                logger.info('No context object found for function %s.', funcname)

    def render(self, out):
        """Write spec to the provided file handle"""
        out.write('#!/usr/bin/env python3\n')
        out.write('"""Epic Game\'s API interface for Python"""\n')
        if self.metadata and 'version' in self.metadata:
            out.write(f'# api_version: {self.metadata["version"]}\n')
        out.write(FILE_START)
        out.write('\n')
        # Add 'blank' function entries
        for e in self.file_entries:
            if isinstance(e, FunctionEntry):
                out.write(f'{e.name} = not_ready\n')
        # Write out every entry
        for e in self.file_entries:
            if not isinstance(e, FunctionEntry):
                e.write(out, self.mapper)
        # Load fuction pointers from dll
        out.write('def load(dll):\n')
        for e in self.file_entries:
            if isinstance(e, FunctionEntry):
                e.write(out, self.mapper)
