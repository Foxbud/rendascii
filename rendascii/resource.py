"""
TBA.
"""


from rendascii.geometry import X, Y
from rendascii.geometry import vec2d
from rendascii.geometry import vec3d
import yaml


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
    return yaml.load(f_in)['colors']


def load_model(model_filename, model_dir, material_dir):
  # Initialize return values.
  vertices = []
  faces = []
  face_normals = []
  face_colors = []

  # Open file.
  vertex_normals = []
  face_vert_norms = []
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

        # Check for vertex normal definition.
        elif words[0] == 'vn':
          vertex_normals.append(
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
          # Extract vertex and normal indices.
          verts = []
          norms = []
          for component in words[1:]:
            vert_info = component.split('/')
            verts.append(int(vert_info[0]) - 1)
            norms.append(int(vert_info[2]) - 1)
          # Construct face data.
          faces.append(verts)
          face_vert_norms.append(norms)

        # Check for material to use.
        elif words[0] == 'usemtl':
          cur_mtl = words[1]

        # Check for material library.
        elif words[0] == 'mtllib':
          materials = _load_materials(words[1], material_dir)

  # Calculate face normals from vertex normals.
  for i in range(len(faces)):
    # Calculate average of vertex normals.
    avg_vert_norm = (0.0, 0.0, 0.0,)
    for j in range(len(face_vert_norms[i])):
      avg_vert_norm = vec3d.add(
          avg_vert_norm,
          vertex_normals[face_vert_norms[i][j]]
          )
    avg_vert_norm = vec3d.multiply(avg_vert_norm, 1 / len(face_vert_norms[i]))

    # Calculate face normal with arbitrary direction.
    origin = vertices[faces[i][0]]
    u = vec3d.subtract(vertices[faces[i][1]], origin)
    v = vec3d.subtract(vertices[faces[i][2]], origin)
    face_normal = vec3d.cross(u, v)

    # Point face normal in correct direction.
    if vec3d.dot(face_normal, avg_vert_norm) < 0:
      face_normal = vec3d.negate(face_normal)

    # Assign new face normal to face.
    face_normals.append(face_normal)

  return (
    vertices,
    faces,
    face_normals,
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
