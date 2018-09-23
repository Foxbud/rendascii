"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from setuptools import find_packages, setup
import sys


# Package building parameters.
setup_info = dict(
    name='rendascii',
    use_scm_version=True,
    setup_requires=['setuptools_scm',],
    description='Real-time ASCII 3D rendering engine',
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/Foxbud/rendascii',
    author='Garrett Fairburn',
    author_email='rendascii@gmail.com',
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


# Compile extensions if not building a wheel.
if 'bdist_wheel' not in sys.argv:
  from Cython.Build import cythonize
  from setuptools import Extension

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

  setup_info['ext_modules'] = cythonize(
      ext_modules,
      compiler_directives={
        'embedsignature': True,
        }
      )
  setup_info['setup_requires'] += ['cython',]


setup(**setup_info)
