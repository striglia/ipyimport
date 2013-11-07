from ipyimport import gather

def test_find_imported_modules():
    gather.find_failed_imports('tests/testing/sample.py')
