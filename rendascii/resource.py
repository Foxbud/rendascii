"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


import json
from rendascii.geometry import X


def load_colormap(colormap_filename, colormap_dir):
  # Open file.
  colormap = {}
  with open(colormap_dir + colormap_filename, 'r') as f_in:
    raw_map = json.load(f_in)
    for key in raw_map:
      value = raw_map[key]
      colormap[key.lower()] = '\0' if value == '' else value[0]

  return colormap


def load_sprite(sprite_filename, sprite_dir):
  # Initialize output data.
  sprite = []

  # Open file.
  with open(sprite_dir + sprite_filename, 'r') as ppm_f:
    raw_contents = ppm_f.read()
    # Strip comments from file and break it into words.
    words = []
    for line in raw_contents.splitlines():
      if line[0] != '#':
        words += line.split()
    # Skip first word for now, which should be 'P3'.
    # Get sprite width and height.
    width = int(words[1])
    height = int(words[2])
    # Get maximum pixel component value.
    maxval = int(words[3])
    del words[0:4]

    # Iterate over every row of the sprite.
    for r in range(height):
      start = r * width * 3
      end = start + width * 3
      row = []
      # Iterate over every pixel in row.
      for p in range(start, end, 3):
        row.append(
            ''.join(
              [
                '{0:02x}'.format(int(words[c]))
                for c
                in range(p, p + 3)
                ]
              )
            )
      sprite.append(row)
  
  return tuple(sprite[::-1])


def load_model(model_filename, model_dir, material_dir, right_handed):
  # Initialize output data.
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
          vertex = [
              float(component)
              for component
              in words[1:]
              ]
          # Flip X axis if right-handed model.
          if right_handed:
            vertex[X] = -vertex[X]
          vertices.append(tuple(vertex))

        # Check for face definition.
        elif words[0] == 'f':
          # Assign face color.
          face_colors.append(materials[cur_mtl])
          # Extract vertex indices.
          verts = []
          for component in words[1:]:
            vert_info = component.split('/')
            verts.append(int(vert_info[0]) - 1)
          # Reverse vertex order if right-handed model.
          if right_handed:
            verts = verts[::-1]
          # Construct face data.
          faces.append(tuple(verts))

        # Check for material to use.
        elif words[0] == 'usemtl':
          cur_mtl = words[1]

        # Check for material library.
        elif words[0] == 'mtllib':
          materials = _load_materials(words[1], material_dir)

  # Pack output data.
  return (
    tuple(vertices),
    tuple(faces),
    tuple(face_colors),
    )


def _load_materials(material_filename, material_dir):
  # Initialize output data.
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
