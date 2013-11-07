"""
Helper functions for modules imported by python files.
"""
import mock
from modulefinder import ModuleFinder
from contextlib import contextmanager

@contextmanager
def tracking_importer():
    """Within this context manager, we will catch any failed imports and log them."""
    # We need to bind this variable now to the real import method so when it's
    # evaluated later it won't be affected by our Mock.
    real_import = __import__

    def printing_import(*args, **kwargs):
        try:
            return real_import(*args, **kwargs)
        except ImportError as e:
            print e
            #raise ValueError('lol')

    with mock.patch('__builtin__.__import__', new=printing_import):
        yield

def find_imported_modules_for_module(module_path):
    """Returns all modules imported by loading a particular module."""
    with tracking_importer():
        ModuleFinder().load_file(module_path)
