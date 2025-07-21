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

def show(cq_model, axis_length=10, show_axis=True, figsize=(800, 800)):
    """Show CadQuery model with optional axis arrows and figure size using Plotly"""
    import open3d as o3d
    import numpy as np
    import plotly.graph_objects as go
    import tempfile
    import os

    # Create a temp file path
    temp_dir = tempfile.gettempdir()
    file_name = "untitled-tmp.stl"
    temp_file_path = os.path.join(temp_dir, file_name)
    cq_model.export(temp_file_path)

    mesh = o3d.io.read_triangle_mesh(temp_file_path)
    if not mesh.has_vertex_normals(): mesh.compute_vertex_normals()
    if not mesh.has_triangle_normals(): mesh.compute_triangle_normals()

    triangles = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)
    colors = (0.5, 0.5, 0.5) + np.asarray(mesh.triangle_normals) * 0.5
    colors = tuple(map(tuple, colors))

    mesh3d = go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=triangles[:, 0],
        j=triangles[:, 1],
        k=triangles[:, 2],
        facecolor=colors,
        opacity=0.5
    )

    # Axis arrows (optional)
    axis_data = []
    if show_axis:
        origin = [0, 0, 0]
        axis_data = [
            go.Scatter3d(x=[origin[0], axis_length], y=[origin[1], 0], z=[origin[2], 0],
                         mode='lines', line=dict(color='red', width=5), showlegend=False),
            go.Scatter3d(x=[origin[0], 0], y=[origin[1], axis_length], z=[origin[2], 0],
                         mode='lines', line=dict(color='green', width=5), showlegend=False),
            go.Scatter3d(x=[origin[0], 0], y=[origin[1], 0], z=[origin[2], axis_length],
                         mode='lines', line=dict(color='blue', width=5), showlegend=False)
        ]

    fig = go.Figure(
        data=[mesh3d] + axis_data,
        layout=dict(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                aspectmode='data'
            ),
            showlegend=False,
            width=figsize[0],
            height=figsize[1]
        )
    )

    fig.show()


