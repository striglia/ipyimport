import pytest
import uuid
import os
import contextlib
from ipyimport import gather


@contextlib.contextmanager
def stub_file(basedir):
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    filename = os.path.join(basedir, str(uuid.uuid4()) + '.py')
    with open(filename, 'w') as outf:
        yield outf

    # Clean up
    os.remove(filename)
    try:
        os.rmdir(basedir)
    except:
        pass


def write_imports_to_file(file_obj, modules_to_import):
    content = '\n'.join(['import %s' % m for m in modules_to_import])
    file_obj.write(content)
    file_obj.flush()


@pytest.mark.parametrize("modules, expected", [
    (['foobar', 're'], ['foobar']),
    (['foobar', 'foobar.baz'], ['foobar']),
    (['foo', 'bar'], ['foo', 'bar']),
])
def test_find_imported_modules(modules, expected):
    with stub_file('testing') as file1:
        write_imports_to_file(file1, modules)
        failed_imports = gather.find_failed_imports(file1.name)
    assert set(expected) == set(failed_imports)


@pytest.mark.parametrize("modules, expected", [
    (['foobar', 're'], ['foobar']),
    (['foobar', 'foobar.baz'], ['foobar']),
    (['foo', 'bar'], ['foo', 'bar']),
])
def test_find_imported_modules_for_subdir(modules, expected):
    basedir = 'testing'
    num_modules = len(modules)
    with stub_file(basedir) as file1:
        with stub_file(basedir) as file2:
            write_imports_to_file(file1, modules[:num_modules // 2])
            write_imports_to_file(file2, modules[num_modules // 2:])
            failed_imports = gather.find_failed_imports_by_directory(basedir)
    assert set(expected) == failed_imports
