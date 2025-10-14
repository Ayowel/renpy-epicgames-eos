"""Representation of EOS JSON spec file entries."""
import logging
import re
from .mapper import Mapper

logger = logging.getLogger(__name__)

def write_function(out, mapper, function, localname, is_static = False, base_indent = ''):
    # type: (any, generator.Mapper, FunctionEntry, str, str) -> None
    """Write a function alias for use in classes."""
    assert localname
    if is_static:
        effective_params = function.params
        out.write(f'{base_indent}@staticmethod\n')
    else:
        effective_params = function.params[1:]
    out.write(f'{base_indent}def {localname}')
    # Function parameters
    out.write('(')
    if not is_static:
        out.write('self')
    for (i, param) in enumerate(effective_params):
        if not is_static or i > 0:
            out.write(', ')
        out.write(f'{param["name"]}')
        # TODO: add default value support
    out.write('):\n')

    # Function signature
    out.write(f'{base_indent}    # type: (')
    for (i, param) in enumerate(function.params):
        out.write(f'{mapper.resolve(param["type"])}')
        if i < len(function.params) - 1:
            out.write(', ')
    out.write(') -> ')
    if function.returntype == 'void':
        out.write('None')
    else:
        out.write(f'{mapper.resolve(function.returntype)}')
    out.write('\n')

    # Function body
    out.write(f'{base_indent}    return {function.name}(')
    if not is_static:
        out.write('self')
    for (i, param) in enumerate(effective_params):
        if not is_static or i > 0:
            out.write(', ')
        out.write(f'{param["name"]}')
    out.write(')\n')

class Entry():
    """A spec entry"""
    def provides(self): # type: () -> List[str]
        """Get the list of variables/types provided by this entry."""
        return tuple()
    def requires(self):
        """Get the list of variables/types needed by this entry."""
        return tuple()
    def write(self, out, mapper):
        """Write out an entry to the provided file handle."""
        raise NotImplementedError()
    def provides_defaults(self, mapper):
        # type: (Mapper) -> Dict[str, str]
        """Returns a dict of default values for the entry"""
        _ = mapper
        return {}

class CallbackEntry(Entry):
    """Representation of a callback function's entry."""
    def __init__(self, entry_dict):
        self.name = entry_dict['callbackname']
        self.returntype = entry_dict['returntype']
        self.params = entry_dict['params']

    def provides_defaults(self, mapper):
        return {
            self.name: 'None'
        }

    def provides(self):
        return (self.name,)

    def requires(self):
        if self.returntype == 'void':
            return (*(p['type'] for p in self.params),)
        else:
            return (self.returntype, *(p['type'] for p in self.params),)

    def write(self, out, mapper):
        if self.returntype == 'void':
            rettype = 'None'
        else:
            rettype = mapper.resolve(self.returntype)
        out.write(f'{self.name} = CFUNCTYPE({rettype}')
        for param in self.params:
            out.write(f', {mapper.resolve(param["type"])}')
        out.write(')\n')

class DefineEntry(Entry):
    """Representation of a define's entry."""
    def __init__(self, entry_dict):
        self.name = entry_dict['name']
        self.expression = entry_dict['expression']
        self.parameters = entry_dict.get('parameters', tuple())
        self.resolved_requires = None

    @property
    def is_parameterized(self):
        """Check whether this define should have arguments."""
        return bool(self.parameters)

    def provides(self):
        return (self.name,)

    def requires(self):
        if self.resolved_requires is None:
            requires = []
            if re.match(r'^("[^"]+"|-?[0-9]+|0x[0-9a-fA-F]+|0o[0-8]+)$', self.expression) is None:
                req_list = re.findall(r'[A-Z][a-zA-Z0-9_]+', self.expression)
                for r in req_list:
                    if r != 'NULL':
                        requires.append(r)
            self.resolved_requires = requires
        return self.resolved_requires

    def write(self, out, mapper):
        assert not self.parameters # No need to support this ATM
        expression = self.expression
        if re.match(r'^(\([^)]*\))?NULL$', expression):
            expression = 'None'
        typed_match = re.match(r'^(\(\((?P<index1>[^()]+)\)(?P<value1>[^()]+)\)|\((?P<index2>[^()]+)\)\((?P<value2>[^()]+)\))$', expression)
        if typed_match:
            index = typed_match['index1'] or typed_match['index2']
            value = typed_match['value1'] or typed_match['value2']
            assert index and value
            expression = f'{index}({value})'
        out.write(f'{self.name} = {expression}\n')

# Operators support is required as some values are derived from other enum values
ENUM_ENTRY_BASE_FUNCTIONS = '''
def __init__(self, value):
    if isinstance(value, c_int32):
        value = value.value
    super().__init__(value)
def __rrshift__(self, other):
    return other >> self.value
def __rshift__(self, other):
    return self.value >> other
def __rlshift__(self, other):
    return other << self.value
def __lshift__(self, other):
    return self.value << other
def __invert__(self):
    return CLASS(~self.value)
def __or__(self, other):
    return CLASS(self.value | other)
def __ror__(self, other):
    return CLASS(other | self.value)
def __int__(self):
    return self.value
'''.strip()

class EnumEntry(Entry):
    """Representation of an enum's entry."""
    def __init__(self, entry_dict):
        self.name = entry_dict['enumname']
        self.values = entry_dict['values']
        self.functions = []
        self.resolved_requires = None

    def provides_defaults(self, mapper):
        def eval_value(v):
            if re.match('^([0-9]+|0o[0-8]+|0x[0-9a-fA-F]+)$', v):
                if 'x' in v:
                    return int(v, 16)
                if 'o' in v:
                    return int(v, 8)
                return int(v)
            # Assume that all other values are derivatives that would not be the smallest value
            return -1
        min_positive_value = min(eval_value(v['value']) for v in self.values if eval_value(v['value']) >= 0)
        return {
            self.name: str(min_positive_value)
        }

    def add_function(self, function, local_name, static = False):
        """Add a function to be used by the entry."""
        self.functions.append((function, local_name, static))

    def requires(self):
        if self.resolved_requires is None:
            self.resolved_requires = ['int32_t']
            provides = self.provides()
            for v in self.values:
                if re.match('^([0-9]+|0o[0-8]+|0x[0-9a-fA-F]+)$', v['value']):
                    continue
                for r in re.findall('[A-Z][A-Za-z0-9_]+', v['value']):
                    # Some enum values depend on other enum values.
                    # We assume that they will be defined in the right order.
                    if r not in self.resolved_requires and r not in provides:
                        self.resolved_requires.append(r)
        return self.resolved_requires

    def provides(self):
        return (self.name, *(v['name'] for v in self.values))

    def write(self, out, mapper):
        out.write('\n')
        out.write(f'class {self.name}(c_int32):\n')
        for f in ENUM_ENTRY_BASE_FUNCTIONS.split('\n'):
            out.write(f'    {f.replace("CLASS", self.name)}\n')
        for (f, name, is_static) in self.functions:
            write_function(out, mapper, f, name, is_static, base_indent = '    ')
        out.write('\n')
        for v in self.values:
            out.write(f'{v["name"]} = {self.name}({v["value"]})\n')
        out.write('\n')

class FunctionEntry(Entry):
    """Representation of an function's entry."""
    def __init__(self, entry_dict):
        self.name = entry_dict['methodname_flat']
        self.params = entry_dict['params']
        self.returntype = entry_dict['returntype']

    def requires(self):
        if self.returntype == 'void':
            return (*(p['type'] for p in self.params),)
        else:
            return (self.returntype, *(p['type'] for p in self.params),)

    def provides(self):
        return (self.name,)

    def write(self, out, mapper):
        if self.returntype == 'void':
            restype = 'None'
        else:
            restype = mapper.resolve(self.returntype)
        out.write(f'    global {self.name}\n')
        out.write(f'    {self.name} = dll.{self.name}\n')
        out.write(f'    {self.name}.argtypes = [')
        for (i, param) in enumerate(self.params):
            out.write(f'{mapper.resolve(param["type"])}')
            if i < len(self.params) - 1:
                out.write(', ')
        out.write(']\n')
        out.write(f'    {self.name}.restype = {restype}\n')
        out.write('\n')

class StructEntry(Entry):
    """Representation of a struct's entry."""
    def __init__(self, entry_dict):
        self.name = entry_dict['struct']
        self.fields = entry_dict['fields']
        self.resolved_requires = None
        self.functions = []

    def add_function(self, function, local_name, static = False):
        """Add a function to be used by the entry."""
        self.functions.append((function, local_name, static))

    def provides_defaults(self, mapper):
        return {
            self.name: f'{self.name}()'
        }

    def requires(self):
        if self.resolved_requires is None:
            requires = set()
            for f in self.fields:
                for i in f.get('unionitems', (f,)):
                    requires.add(i['type'])
            self.resolved_requires = [*requires]
        return self.resolved_requires

    def provides(self):
        return (self.name,)

    def write_fields(self, out, fields, mapper, base_name = ''):
        """Write the fields of the struct."""
        out.write('    _fields_ = [\n')
        for field in fields:
            if field.get('unionitems', None):
                field_type = f'{base_name}_INTERNAL_UNION_{field["name"]}'
            else:
                field_type = mapper.resolve(field['type'])
            out.write(f"        ('{field['name']}', {field_type}),\n")
        out.write('    ]\n')

    def write(self, out, mapper):
        for f in self.fields:
            if f.get('unionitems', None):
                unionname = f'{self.name}_INTERNAL_UNION_{f["name"]}'
                out.write(f'class {unionname}(Union):\n')
                out.write('    _pack_ = PACK\n')
                self.write_fields(out, f['unionitems'], mapper, unionname)
        out.write(f'class {self.name}(Structure):\n')
        out.write('    _pack_ = PACK\n')
        # Fields spec
        self.write_fields(out, self.fields, mapper, self.name)
        # init function
        out.write('    def __init__(self')
        for f in self.fields:
            out.write(f', {f["name"]} = ')
            reftype = mapper.resolve(f['unionitems'][0]['type'] if f.get('unionitems', None) else f['type'])
            if 'recommended_value' in f:
                out.write(f['recommended_value'])
            else:
                out.write(f"{mapper.get_ctype_default(reftype)}")
        out.write('):\n')
        out.write('        Structure.__init__(self')
        for f in self.fields:
            out.write(f', {f["name"]} = {f["name"]}')
        out.write(')\n')
        # Struct functions
        for (f, name, is_static) in self.functions:
            write_function(out, mapper, f, name, is_static, base_indent = '    ')
class TypedefEntry(Entry):
    """Representation of a typedef's entry."""
    def __init__(self, entry_dict):
        self.is_extern = entry_dict.get('extern', False)
        self.name = entry_dict['name']
        self.source_type = entry_dict['type']
        self.functype = entry_dict.get('functype', None)
        self.functions = []
        if re.match(r'^struct [a-zA-Z][a-zA-Z0-9_]+\*$', self.source_type):
            # Coerce pointers to structs declared on-the-fly to anonymous pointers
            self.type = 'void*'
        else:
            self.type = self.source_type
        self.resolved_requires = None

    def provides_defaults(self, mapper):
        if self.functype:
            return {self.name: f'{self.name}(0)'}
        if re.match(r'^struct [a-zA-Z][a-zA-Z0-9_]+\*$', self.source_type):
            return {self.name: 'None'}
        ctype_string = mapper.resolve(self.type)
        logger.debug("Resolving default for %s", ctype_string)
        return {self.name: mapper.get_ctype_default(ctype_string)}

    def add_function(self, function, local_name, static = False):
        """Add a function to be used by the entry."""
        self.functions.append((function, local_name, static))

    def provides(self):
        return (self.name,)

    def requires(self):
        if self.resolved_requires is None:
            self.resolved_requires = [self.type]
            if self.functype is not None:
                if self.functype['returntype'] != 'void':
                    self.resolved_requires.append(self.functype['returntype'])
                for param in self.functype['params']:
                    self.resolved_requires.append(param['type'])
            else:
                self.resolved_requires.append(self.type)
        return self.resolved_requires

    def write(self, out, mapper):
        if self.functype is not None:
            out.write(f'{self.name} = CFUNCTYPE(')
            if self.functype['returntype'] != 'void':
                out.write(f'{mapper.resolve(self.functype["returntype"])}')
            else:
                out.write('None')
            for param in self.functype['params']:
                out.write(f', {mapper.resolve(param["type"])}')
            out.write(')\n')
        else:
            out.write(f'class {self.name}({mapper.resolve(self.type)}):\n')
            if not self.functions:
                out.write('    pass\n')
            else:
                for (f, name, is_static) in self.functions:
                    write_function(out, mapper, f, name, is_static, base_indent = '    ')
