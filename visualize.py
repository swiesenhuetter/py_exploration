import Cython.Compiler.Options
from Cython.Build import cythonize
from Cython.Shadow import annotation_typing

Cython.Compiler.Options.annotate = True
Cython.Compiler.Options.annotation_typing = False

cythonize("cython_test.py",
          compiler_directives={
              "language_level": "3",
              "annotation_typing": True,
          },
          annotate=True)
