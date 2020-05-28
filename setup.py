"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


import os
from setuptools import find_packages, setup


# Custom environment variable to disable extension building.
PURE_PY_ENV_VAR = 'PURE_PY_DIST'


# Package building parameters.
setup_info = dict(
    name='rendascii',
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'cython',],
    description='Real-time ASCII 3D rendering engine',
    long_description_content_type='text/markdown',
    url='https://github.com/Foxbud/rendascii',
    author='Garrett Fairburn',
    author_email='garrett@fairburn.dev',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        ],
    )


# Load README.
with open('README.md', 'r') as f_in:
  setup_info['long_description'] = f_in.read()


# Only cythonize extensions if not disabled.
if PURE_PY_ENV_VAR not in os.environ:
  from setuptools import Extension

  setup_info['ext_modules'] = [
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


setup(**setup_info)
