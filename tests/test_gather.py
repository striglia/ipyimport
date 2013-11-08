from ipyimport import gather


def test_find_imported_modules(capsys):
    failed_imports = gather.find_failed_imports('tests/testing/sample.py')
    assert ['foobar'] == failed_imports.keys()


def test_find_imported_modules_for_subdir():
    failed_imports = gather.find_failed_imports_by_directory('tests/testing/')
    assert ['foobar', 'other_foobar'] == failed_imports.keys()
