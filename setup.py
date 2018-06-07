"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""



from setuptools import Extension, find_packages, setup


setup(
    name='rendascii',
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'cython',],
    ext_modules=[
      Extension(
        'rendascii.__init__',
        sources=['rendascii/__init__.py',]
        ),
      Extension(
        'rendascii.interface',
        sources=['rendascii/interface.py',]
        ),
      Extension(
        'rendascii.resource',
        sources=['rendascii/resource.py',]
        ),
      Extension(
        'rendascii.pipeline.__init__',
        sources=['rendascii/pipeline/__init__.py',]
        ),
      Extension(
        'rendascii.pipeline.shader',
        sources=['rendascii/pipeline/shader.py',]
        ),
      Extension(
        'rendascii.pipeline.stage',
        sources=['rendascii/pipeline/stage.py',]
        ),
      Extension(
        'rendascii.geometry.__init__',
        sources=['rendascii/geometry/__init__.py',]
        ),
      Extension(
        'rendascii.geometry.matrix',
        sources=['rendascii/geometry/matrix.py',]
        ),
      Extension(
        'rendascii.geometry.poly2d',
        sources=['rendascii/geometry/poly2d.py',]
        ),
      Extension(
        'rendascii.geometry.poly3d',
        sources=['rendascii/geometry/poly3d.py',]
        ),
      Extension(
        'rendascii.geometry.vec2d',
        sources=['rendascii/geometry/vec2d.py',]
        ),
      Extension(
        'rendascii.geometry.vec3d',
        sources=['rendascii/geometry/vec3d.py',]
        ),
      Extension(
        'rendascii.geometry.vech',
        sources=['rendascii/geometry/vech.py',]
        ),
      ],
    description='ASCII 3D rendering engine',
    url='https://bitbucket.org/foxbudpersonal/rendascii',
    author='Garrett Fairburn',
    author_email='breadboardfox@gmail.com',
    license='MIT',
    packages=find_packages(),
    data_files = [("", ["LICENSE.txt"])]
)
