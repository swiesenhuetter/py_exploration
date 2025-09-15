from setuptools import setup
from Cython.Build import cythonize

setup(
    name="My Math Module Cythonized",
    ext_modules=cythonize(
        "cython_test.py", # Compile the .py file
        show_all_warnings=True,
        compiler_directives={'language_level': "3",
                             'annotation_typing': False
                             },
        build_dir = 'cython_build')
)