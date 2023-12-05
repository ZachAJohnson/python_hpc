# setup.py
# compile with: python setup.py build_ext --inplace


from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules=cythonize(
		"cython_smart.pyx", compiler_directives={"language_level":"3"},force=True)

	)


