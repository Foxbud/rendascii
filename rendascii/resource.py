"""
TBA.
"""


class Model:

  def __init__(self, file_name):
    # Initialize instance attributes.
    self.vertices = []
    self.faces = []
    self.face_normals = []
    self.face_colors = []

    # Load materials from file.
    materials = {}
    with open(file_name + '.mtl', 'r') as mtl_f:
      cur_mtl = None
      for line in mtl_f:
        words = line.split()
        # Check for new material.
        if words[0] == 'newmtl':
          cur_mtl = words[1]
        # Check for material color (diffuse).
        elif words[1] == 'Kd':
          materials[cur_mtl] = ''.join(
              [
                hex(round(float(component)))[2:]
                for component
                in words[1:]
                ]
              )
