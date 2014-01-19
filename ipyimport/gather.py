"""
Helper functions for modules imported by python files.
"""
import os
from modulefinder import ModuleFinder


def return_missing_base_modules(failed_import_dict):
    """Takes a dict of modules we failed to load and removes repeats."""
    return set([m.split('.')[0] for m in failed_import_dict])


def find_failed_imports(module_path):
    """Returns all modules that failed to import when loading a particular
    module."""
    finder = ModuleFinder()
    finder.run_script(module_path)
    bad_modules = dict(finder.badmodules)
    return return_missing_base_modules(bad_modules)


def find_failed_imports_by_directory(directory):
    """Returns all modules that failed to import when loading all modules below
    a directory."""
    finder = ModuleFinder()
    py_files = _find_all_python_modules(directory)
    for f in py_files:
        finder.run_script(f)
    bad_modules = dict(finder.badmodules)
    return return_missing_base_modules(bad_modules)


def _find_all_python_modules(directory):
    py_files = []

    def accumulate_py_files(arg, dirname, names):
        files = [os.path.join(dirname, n) for n in names if n.endswith('.py')]
        py_files.extend(files)

    os.path.walk(directory, accumulate_py_files, None)
    return py_files
