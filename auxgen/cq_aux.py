"""
Functions for ploting CadQuery models in
Google Colab.

This required to install Open3D in the notebook

!pip install cadquery open3d

JCA
"""

import open3d as o3d
import numpy as np
import plotly.graph_objects as go

import tempfile
import os


def show(cq_model):
    """Show CadQuery model by saving it and loading again"""
    # Create a temp file path (does not create the file yet)
    temp_dir = tempfile.gettempdir()
    file_name = "untitled-tmp.stl"
    temp_file_path = os.path.join(temp_dir, file_name)

    cq_model.export(temp_file_path)

    mesh = o3d.io.read_triangle_mesh(temp_file_path)


    if not mesh.has_vertex_normals(): mesh.compute_vertex_normals()
    if not mesh.has_triangle_normals(): mesh.compute_triangle_normals()


    triangles = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)
    colors = None
    if mesh.has_triangle_normals():
        colors = (0.5, 0.5, 0.5) + np.asarray(mesh.triangle_normals) * 0.5
        colors = tuple(map(tuple, colors))
    else:
        colors = (1.0, 0.0, 0.0)


    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=vertices[:,0],
                y=vertices[:,1],
                z=vertices[:,2],
                i=triangles[:,0],
                j=triangles[:,1],
                k=triangles[:,2],
                facecolor=colors,
                opacity=0.50)
        ],
        layout=dict(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            )
        )
    )
    fig.show()

