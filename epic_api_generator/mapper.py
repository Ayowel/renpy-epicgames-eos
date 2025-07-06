"""Map c types to python."""
import logging
import re

logger = logging.getLogger(__name__)

class Mapper():
    """Helper class to handle c to python types mappings."""
    def __init__(self, mapper):
        self.indexed_values = set(mapper.keys())
        self.mappings = mapper

    def update(self, iterable):
        # type: (Mapping, str[]) -> None
        """Add a list of valid types in both c and python."""
        self.indexed_values.update(iterable)

    def is_indexed(self, key):
        # type: (Mapping, str) -> bool
        """Check whether the provided c type can be resolved."""
        if '(*)' in key: # Ignore function signatures
            return True
        if key.endswith(']'):
            key_length = re.search(r'\[(?P<length>[a-zA-Z0-9_]+)\]$', key)
            assert key_length is not None
            if not self.is_indexed(key_length['length']):
                return False
            key = re.sub(r'\[[a-zA-Z0-9_]+\]$', '', key)
        if 'const' in key:
            prev_key = ''
            while prev_key != key:
                prev_key = key
                key = re.sub(r'(^|(?![a-zA-Z0-9_])) *const *((?![a-zA-Z0-9_]) *|$)', '', key)
        if key in self.indexed_values:
            return True
        if key.endswith('*'):
            return self.is_indexed(key[:-1].rstrip())
        return False

    def resolve(self, key):
        # type: (Mapping, str) -> str
        """Resolve the provided c type to its equivalent python type."""
        if '(*)' in key: # received a function's signature
            return 'c_void_p'
        if 'const' in key: # Drop all const components
            prev_key = ''
            while prev_key != key:
                prev_key = key
                key = re.sub(r'(^|(?![a-zA-Z0-9_])) *const *((?![a-zA-Z0-9_]) *|$)', '', key)

        if key in self.indexed_values:
            return self.mappings.get(key, key)

        if key.endswith('*'):
            return f'POINTER({self.resolve(key[:-1].strip())})'

        if key.endswith(']'):
            key_info = re.search(r'\[(?P<length>[a-zA-Z0-9_]+)\]$', key)
            assert key_info is not None
            array_length = key_info['length']
            return f'{self.resolve(key[:-len(array_length)-2])} * {array_length}'

        raise Exception(f'Failed to resolve key "{key}".')
