import sys
#from pkg_resources import normalize_path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1'
install_requires = ['ply']
tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose',
            '--ignore=build',
            #'--cov=objpack',
            #'--cov-report=term-missing',
            '--pep8',
            'objpack']
        self.test_suite = True

    def run_tests(self):
        import pytest
        from pkg_resources import normalize_path, _namespace_packages

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and getattr(self.distribution, 'use_2to3', False):
            module = self.test_args[-1].split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code
            ## This will prevent the old 2.x code from being found
            ## by py.test discovery mechanism, that apparently
            ## ignores sys.path..
            ei_cmd = self.get_finalized_command("egg_info")

            ## Replace the module name with normalized path
            self.test_args[-1] = normalize_path(ei_cmd.egg_base)

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='ObjPack',
    version=version,
    packages=find_packages(),
    url='http://rshk.github.io/objpack',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='Object serialization format, superset of JSON',
    long_description='Object serialization format, superset of JSON',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='objpack.tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        #"Programming Language :: Python :: Implementation :: PyPy",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    **extra)
