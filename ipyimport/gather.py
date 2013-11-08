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
    with _tracking_importer() as failed_imports:
        finder = ModuleFinder()
        finder.load_file(module_path)
    return failed_imports


def find_failed_imports_by_directory(directory):
    """Returns all modules that failed to import when loading all modules below
    a directory."""
    py_files = _find_all_python_modules(directory)
    with _tracking_importer() as failed_imports:
        for f in py_files:
            ModuleFinder().load_file(f)
    return failed_imports


@contextmanager
def _tracking_importer():
    """Within this context manager, we will catch any failed imports and log
    them."""
    # We need to bind this variable now to the real import method so when it's
    # evaluated later it won't be affected by our Mock.
    real_import = __import__

    # Failed_imports will be where we accumulate all unsucessful imports. Note
    # that it's a list, so when we pass back a reference to it, items added
    # from printing_import will be reflected.
    failed_imports = set()

    def printing_import(*args, **kwargs):
        try:
            return real_import(*args, **kwargs)
        except ImportError as e:
            missing_module = ' '.join(e.message.split()[3:])
            #print missing_module
            failed_imports.add(missing_module)

    with mock.patch('__builtin__.__import__', new=printing_import):
        yield failed_imports


def _find_all_python_modules(directory):
    py_files = []

    def accumulate_py_files(arg, dirname, names):
        files = [os.path.join(dirname, n) for n in names if n.endswith('.py')]
        py_files.extend(files)

    os.path.walk(directory, accumulate_py_files, None)
    return py_files
