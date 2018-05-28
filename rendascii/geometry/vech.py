"""
TBA.
"""


from rendascii.geometry import X, Y, Z, W


def homogenize(vec, w=1.0):
  return (
      vec[X],
      vec[Y],
      vec[Z],
      w,
      )


def normalize(vec):
  return (
      vec[X] / vec[W],
      vec[Y] / vec[W],
      vec[Z] / vec[W],
      )


def project_z(vec, focus, ):
  ratio = -focus[Z] / (
      vec[Z] - focus[Z]
      )
  return (
      focus[X] + ratio * (
        vec[X] - focus[X]
        ),
      focus[Y] + ratio * (
        vec[Y] - focus[Y]
        ),
      0.0,
      focus[W] + ratio * (
        vec[W] - focus[W]
        ),
      )
