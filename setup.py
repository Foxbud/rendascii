"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


ext_modules = [
    Extension(
      'rendascii.interface',
      sources=['rendascii/interface.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.resource',
      sources=['rendascii/resource.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.utility',
      sources=['rendascii/utility.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.pipeline.shader',
      sources=['rendascii/pipeline/shader.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.pipeline.stage',
      sources=['rendascii/pipeline/stage.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.geometry.matrix',
      sources=['rendascii/geometry/matrix.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.geometry.polygon',
      sources=['rendascii/geometry/polygon.py',],
      extra_compile_args=['-O1',]
      ),
    Extension(
      'rendascii.geometry.vector',
      sources=['rendascii/geometry/vector.py',],
      extra_compile_args=['-O1',]
      ),
    ]


setup(
    name='rendascii',
    use_scm_version=True,
    ext_modules=cythonize(
      ext_modules,
      compiler_directives={
        'embedsignature': True,
        }
      ),
    setup_requires=['setuptools_scm', 'cython',],
    description='ASCII 3D rendering engine',
    url='https://bitbucket.org/foxbudpersonal/rendascii',
    author='Garrett Fairburn',
    author_email='breadboardfox@gmail.com',
    license='MIT',
    packages=find_packages(),
    data_files = [("", ["LICENSE.txt"])]
)
