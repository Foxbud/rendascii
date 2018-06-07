"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from pkg_resources import get_distribution, DistributionNotFound


try:
  __version__ = get_distribution(__name__).version
except DistributionNotFound:
  __version__ = ""
