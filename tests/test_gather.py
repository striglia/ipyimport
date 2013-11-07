from ipyimport import gather

def test_find_imported_modules():
    gather.find_imported_modules_for_module('tests/sample.py')
    assert False
