"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from datetime import datetime
from rendascii.geometry import matrix, vector
import time


class FrameRateManager:

  def __init__(self, max_fps=None, fps_interval=0.0):
    # Initialize instance attributes.
    self._total_time = 0.0
    self._total_frames = 0
    self._time_delta = 0.0
    self._fps = 0.0
    self._start_last = datetime.now()
    self._start_this = self._start_last
    self._min_delta = None if max_fps is None else 1 / max_fps
    self._interval = fps_interval
    self._delta_sum = 0.0
    self._delta_num = 0

  def update(self):
    # Update timing data.
    self._start_last = self._start_this
    self._start_this = datetime.now()
    self._time_delta = (self._start_this - self._start_last).total_seconds()
    # Trigger delay if FPS exceeds max.
    if self._min_delta is not None:
      wait_time = self._min_delta - self._time_delta
      if wait_time > 0.0:
        time.sleep(wait_time)
        self._time_delta = self._min_delta
        self._start_this = datetime.now()
    self._total_time += self._time_delta
    self._total_frames += 1
    self._delta_sum += self._time_delta
    self._delta_num += 1
    # Update FPS if interval has elapsed.
    if self._delta_sum >= self._interval:
      self._fps = 1.0 / (self._delta_sum / self._delta_num)
      self._delta_sum = 0.0
      self._delta_num = 0

  def get_total_time(self):
    return self._total_time

  def get_total_frames(self):
    return self._total_frames

  def get_delta_time(self):
    return self._time_delta

  def get_fps(self, as_int=False):
    fps = self._fps
    if as_int:
      fps = int(round(fps))
    return fps


class Transformer:

  def __init__(self, inverse=False):
    # Initialize instance attributes.
    self._inverse = inverse
    self._transformation = matrix.IDENTITY_H

  def scale(self, scalar):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.scaling_h(
            1.0 / scalar
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.scaling_h(
            scalar
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def translate(self, vec):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.translation_h(
            vector.negate(
              vec
              )
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.translation_h(
            vec
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def rotate(self, theta, axis_normal):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.rotation_h(
            -theta,
            axis_normal
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.rotation_h(
            theta,
            axis_normal
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def apply(self, vec):
    return vector.conv_h_to_3d(
        matrix.transform_h(
          self._transformation,
          vector.conv_3d_to_h(
            vec
            )
          )
        )

  def clear(self):
    self._transformation = matrix.IDENTITY_H

    # Return self for convenience.
    return self

  def get_transformation(self):
    return self._transformation
