# Tests management

## Install dependencies

```pip2 install -U -r requirements.txt```

## How to run

Before run tests, create inside the test dir a file named `test.cfg` by copying the file `example.cfg`. Fill the properties `url`, `username` and `password` with your Yggtorrent account information.

Now you're able to run unit tests by launching the command : ```$python -m pytest test/test.py ygg --pep8 --cov ygg --cov-report term-missing```

You should see something like this :
```console
============================= test session starts =============================
platform win32 -- Python 2.7.12, pytest-3.0.5, py-1.4.32, pluggy-0.4.0 -- C:\Python27\python.exe
cachedir: .cache
rootdir: F:\workspace\potatoygg, inifile:
plugins: cov-2.5.1, pep8-1.0.6
collecting ... collected 11 items

test/test.py PASSED
test/test.py::TestPotatoYGG::test_loginKO PASSED
test/test.py::TestPotatoYGG::test_login PASSED
test/test.py::TestPotatoYGG::test_loginCheck PASSED
test/test.py::TestPotatoYGG::test_searchMovie PASSED
test/test.py::TestPotatoYGG::test_searchMoviePagination PASSED
test/test.py::TestPotatoYGG::test_searchAnim PASSED
test/test.py::TestPotatoYGG::test_extraCheck PASSED
test/test.py::TestPotatoYGG::test_download PASSED
ygg/__init__.py PASSED
ygg/ygg.py PASSED

---------- coverage: platform win32, python 2.7.12-final-0 -----------
Name         Stmts   Miss  Cover   Missing
------------------------------------------
ygg\ygg.py      96      8    92%   69, 95-96, 115, 117, 119, 179-180


========================= 11 passed in 17.10 seconds ==========================
```

Cfg files are snippets of the CouchPotato configuration file `settings.conf`. Depending your execution environment (proxies, etc...), you can customize them if necessary to run unit tests.
