# RendASCII

RendASCII is a real-time, z-buffering based 3D rendering engine written from scratch in and for Python 3. Unlike traditional real-time rendering engines, RendASCII renders frames as printable strings using ASCII characters for pixels. RendASCII is open source under the MIT license.

[Project Homepage](https://bitbucket.org/Foxbud/rendascii)

[Project Documentation](https://bitbucket.org/Foxbud/rendascii/wiki)

Please direct questions to **rendascii@gmail.com**.

## Features

* No external dependencies; uses just the Python standard library.
* Multiprocess based rendering.
* Optional Cython based accelerator extension modules.
* Load and render 3D models from Wavefront object and material files (\*.obj and \*.mtl, respectively).
* Load and render 2D sprites from ASCII based Portable PixMap files (\*.ppm).
* Render the same or different scene(s) using multiple virtual cameras.
* ASCII overlays for displaying fixed graphics and/or information.
* Map sprite and material colors to ASCII characters using JSON colormaps.
* Transform models, sprites, and virtual cameras using arbitrary homogeneous transformation matrices.
* Utility for easily constructing complex transformation matrices with scaling, translations, and rotations.
* Utility for managing frame-rate and calculating delta time.

## Installation

`# pip3 install rendascii` - system wide installation **without** compiled extensions.

`$ pip3 install --user rendascii` - local user installation **without** compiled extensions.

`# pip3 install --no-binary :all: rendascii` - system wide installation **with** compiled extensions.

`$ pip3 install --user --no-binary :all: rendascii` - local user installation **with** compiled extensions.

## Building

`$ git clone https://bitbucket.org/Foxbud/rendascii.git` - clone repository source.

`$ cd rendascii` - change working directory to local repository.

`$ python3 -m setup bdist_wheel` - build distribution **without** extension modules.

`$ python3 -m setup bdist` - build distribution **with** extension modules.
