"""
TBA.
"""


import json
from rendascii.geometry import poly3d, vec2d, vec3d
from rendascii.geometry import X, Y


def generate_camera_fragments(width, height, num_pixels_x, num_pixels_y):
  bound_min = (-width / 2, -height / 2,)
  frag_size = (width / num_pixels_x, height / num_pixels_y,)

  fragments = tuple(
      tuple(
        (
          bound_min[X] + frag_size[X] * (x + 0.5),
          bound_min[Y] + frag_size[Y] * (y + 0.5),
          )
        for x
        in range(num_pixels_x)
        )
      for y
      in range(num_pixels_y)
      )
  
  return fragments


def load_colormap(colormap_filename, colormap_dir):
  with open(colormap_dir + colormap_filename, 'r') as f_in:
    return json.load(f_in)


def load_model(model_filename, model_dir, material_dir):
  # Initialize return values.
  vertices = []
  faces = []
  face_colors = []

  # Open file.
  materials = None
  with open(model_dir + model_filename, 'r') as obj_f:
    cur_mtl = None
    for line in obj_f:
      words = line.split()
      if len(words) > 0:

        # Check for vertex definition.
        if words[0] == 'v':
          vertices.append(
              tuple(
                float(component)
                for component
                in words[1:]
                )
              )

        # Check for face definition.
        elif words[0] == 'f':
          # Assign face color.
          face_colors.append(materials[cur_mtl])
          # Extract vertex indices.
          verts = []
          for component in words[1:]:
            vert_info = component.split('/')
            verts.append(int(vert_info[0]) - 1)
          # Construct face data.
          faces.append(verts)

        # Check for material to use.
        elif words[0] == 'usemtl':
          cur_mtl = words[1]

        # Check for material library.
        elif words[0] == 'mtllib':
          materials = _load_materials(words[1], material_dir)

  return (
    vertices,
    faces,
    face_colors,
    )


def _load_materials(material_filename, material_dir):
  # Initialize return values.
  materials = {}

  # Open file.
  with open(material_dir + material_filename, 'r') as mtl_f:
    cur_mtl = None
    for line in mtl_f:
      words = line.split()
      if len(words) > 0:

        # Check for new material.
        if words[0] == 'newmtl':
          cur_mtl = words[1]

        # Check for material color (diffuse).
        elif words[0] == 'Kd':
          materials[cur_mtl] = ''.join(
              [
                '{0:02x}'.format(round(float(component) * 255))
                for component
                in words[1:]
                ]
              )

  return materials
