import json
from typing import List
import numpy as np
import re


def hex_to_rgb(dec):
    B = dec & 255
    G = (dec >> 8) & 255
    R = (dec >> 16) & 255
    A = (dec >> 24) & 255
    return (R, G, B), A


def remove_strings(json_string):
    def replacer(x): return re.sub(r'"', '', x.group())
    pattern = r'[\"|\'](\[+.*\]+)[\"|\']'
    return re.sub(pattern, replacer, json_string)


class SubMesh:
    def __init__(self, vertices: List[List[float]], faces: List[List[int]], color: int):
        self.vertices = vertices
        self.faces = faces
        self.color = color

    def __repr__(self):
        return f"SubMesh(vertices={len(self.vertices)}, faces={len(self.faces)}, color={hex_to_rgb(self.color)[0]})"


class Mesh:
    def __init__(self, vertices: List[List[float]],
                        faces: List[List[int]],
                        colors: List[int],
                        positions:List[List[float]]=[[0,0,0]],
                        orientations:List[List[float]]=[np.eye(3).tolist()],
                        ):
        self.positions = positions
        self.orientations = orientations  # Quaternion orientation, can be updated later
        self.submeshes = self.create_submeshes(vertices, faces, colors)

    def create_submeshes(
            self, vertices: List[List[float]],
            faces: List[List[int]],
            colors: List[int]) -> List[SubMesh]:
        color_dict = {}

        for i, face in enumerate(faces):
            color = colors[i]
            if color not in color_dict:
                color_dict[color] = []  
            color_dict[color].append(face)

        submeshes = []
        for color, faces in color_dict.items():
            submesh = SubMesh(vertices, faces, color)
            submeshes.append(submesh)

        return submeshes
    
    def plot(self, plotter=None):
        import pyvista as pv
        
        show = True
        if plotter is None:
            plotter = pv.Plotter(lighting="three lights")
            show = False

        for submesh in self.submeshes:
            vertices = np.array(submesh.vertices)
            # The "3" is the number of vertices in each face
            faces = np.hstack([[3] + face for face in submesh.faces])
            mesh = pv.PolyData(vertices, faces)
            plotter.add_mesh(mesh, 
                             color=hex_to_rgb(submesh.color)[0],
                             opacity=hex_to_rgb(submesh.color)[1]/255
                            )  # Convert the uint16 color to RGB

        if show:
            plotter.show()

    def to_json(self, as_string=True) -> str:
        submeshes_json = [
            {"vertices": str(submesh.vertices), "faces": str(submesh.faces), "color": submesh.color}
            for submesh in self.submeshes]
        mesh_json = {
            "position": str(self.positions), "orientation": str(self.orientations),
            "submeshes": submeshes_json}
        if not as_string:
            return mesh_json
        return remove_strings(json.dumps(mesh_json, indent=4))

    def __repr__(self):
        return f"Mesh(position={self.position}, orientation={self.orientation}, submeshes={self.submeshes})"
    
class Geometry:
    def __init__(self, geo):
        self.unique_solids = list(set(geo.solids))
        self.unique_meshes = self.to_meshes(geo)

    def to_meshes(self, geo):
        solid_orientations = {i: {"displacement": [], "rotation": []} for i in range(len(self.unique_solids))}

        for i, unique_solid in enumerate(self.unique_solids):
            mask = np.asarray(geo.solids) == unique_solid
            solid_orientations[i]["displacement"] = np.round(np.asarray(self.solid_displacements)[mask], 6).tolist()
            solid_orientations[i]["rotation"] = np.round(np.asarray(self.solid_rotations)[mask], 6).tolist()
                    
        return [
            Mesh(np.round(solid.mesh.vertices, 6).tolist(),
                 solid.mesh.triangles.tolist(),
                 solid.color.tolist(),
                 solid_orientations[i]["displacement"],
                 solid_orientations[i]["rotation"])
            for i, solid in enumerate(self.unique_solids)
        ]

    def to_json(self):
        total_json = {"meshes": [mesh.to_json(as_string=False) for mesh in self.unique_meshes]}
        return remove_strings(json.dumps(total_json, indent=4))