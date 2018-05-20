"""
TBA.
"""


from rendascii.geometry import vec3d


def load_model(objmesh_name, resource_dir):
  # Initialize return values.
  vertices = []
  faces = []
  face_normals = []
  face_colors = []

  # Open file.
  vertex_normals = []
  face_vert_norms = []
  materials = None
  with open(resource_dir + objmesh_name, 'r') as obj_f:
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
          materials = self._load_mtllib(words[1], resource_dir)

  # Calculate face normals from vertex normals.
  for i in range(len(faces)):
    # Calculate average of vertex normals.
    avg_vert_norm = (0.0, 0.0, 0.0)
    for j in range(len(face_vert_norms[i])):
      avg_vert_norm = vec3d.add(
          avg_vert_norm,
          vertex_normals[face_vert_norms[i][j]]
          )
    avg_vert_norm = vec3d.multiply(avg_vert_norm, 1 / len(face_vert_norms[i]))

    # Calculate face normal with arbitrary direction.
    origin = vertices[faces[i][0]]
    u = vec3d.subtract(vertices[faces[i][1], origin)
    v = vec3d.subtract(vertices[faces[i][2], origin)
    face_normal = vec3d.cross(u, v)

    # Point face normal in correct direction.
    if vec3d.dot(face_normal, avg_vert_norm) < 0:
      face_normal = vec3d.negate(face_normal)

    # Assign new face normal to face.
    face_normals.append(face_normal)

  return vertices, faces, face_normals, face_colors


def _load_mtllib(mtllib_name, resource_dir):
  # Initialize return values.
  materials = {}

  # Open file.
  with open(resource_dir + mtllib_name, 'r') as mtl_f:
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
