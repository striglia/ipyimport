from ipyimport import gather


def test_find_imported_modules(capsys):
    failed_imports = gather.find_failed_imports('tests/testing/sample.py')
    assert set(['foobar']) == failed_imports


def test_find_imported_modules_for_subdir():
    failed_imports = gather.find_failed_imports_by_directory('tests/testing/')
    assert set(['foobar']) == failed_imports
