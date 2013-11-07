"""
Helper functions for modules imported by python files.
"""
import os
import mock
from modulefinder import ModuleFinder
from contextlib import contextmanager


def find_failed_imports(module_path):
    """Returns all modules that failed to import when loading a particular
    module."""
    with _tracking_importer():
        ModuleFinder().load_file(module_path)


def find_failed_imports_by_directory(directory):
    """Returns all modules that failed to import when loading all modules below
    a directory."""
    modules = _find_all_python_modules(directory)
    with _tracking_importer():
        for m in modules:
            ModuleFinder().load_file(m)


@contextmanager
def _tracking_importer():
    """Within this context manager, we will catch any failed imports and log
    them."""
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


def _find_all_python_modules(directory):
    py_files = []

    def accumulate_py_files(dirname, names):
        py_files.extend([n for n in names if n.endswith('.py')])

    os.path.walk(directory, accumulate_py_files)
    return py_files
