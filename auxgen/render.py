"""
Functions to render 3D models
Requires to install:
- numpy-stl
- tqdm

JCA

"""
import os
import math

from tqdm import tqdm
import numpy as np
from stl import mesh

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource
import matplotlib.image as mpimg


def render_stl_to_image(stl_path, show=False, model_color='lightgrey', color_normals=False):
    """Load STL files on path and render with matplotlib. If color_normals used model_color not taken into account"""
    # Load the STL file
    model = mesh.Mesh.from_file(stl_path)
    vectors = model.vectors

    # Create a matplotlib figure and 3D axis
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')

    # Estimate normals and create grayscale colors based on them
    triangle_normals = model.normals

    # # # Add the mesh as a collection of 3D polygons
    light = LightSource(azdeg=0, altdeg=0)
    if color_normals:
        coords = np.asarray(triangle_normals)
        norms = np.linalg.norm(coords, axis=1, keepdims=True)
        norms[norms == 0] = 1.0  # Avoid division by zero
        # colors = np.abs(coords/norms)
        colors = coords/norms
        colors = 0.5*colors + 0.5
        mesh_poly = Poly3DCollection(model.vectors, alpha=0.6, facecolors=colors, shade=True,  lightsource=light)
    else:
        mesh_poly = Poly3DCollection(vectors, alpha=1, shade=True,  lightsource=light, facecolors=model_color)

    ax.add_collection3d(mesh_poly)

    # Auto scale to the mesh size
    scale = model.points.flatten()
    ax.auto_scale_xyz(scale, scale, scale)

    # # Set axis limits
    vertices = vectors.reshape(-1, 3)

    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    ax.set_xlim([x.min(), x.max()])
    ax.set_ylim([y.min(), y.max()])
    ax.set_zlim([z.min(), z.max()])
    ax.set_box_aspect([
        x.max() - x.min(),
        y.max() - y.min(),
        z.max() - z.min()
    ])

    # Set view angle and remove axes
    ax.view_init(elev=20, azim=30)
    ax.axis('off')

    # Construct output path
    base, _ = os.path.splitext(stl_path)
    output_image = base + '.png'

    # Save and close
    plt.tight_layout()
    plt.savefig(output_image, dpi=120)
    
    if show:
        plt.show()
    else:
        plt.close()


def render_each(save_path,  model_color='lightcoral', color_normals=False ):
    """ Render each STL file in path"""
    print('Rendering STL models in folder...')
    format='stl'

    files = os.listdir(save_path)
    for filename in tqdm(files, total=len(files)):
        if filename.endswith(f'.{format}'):
            model_file = os.path.join(save_path, filename)
            render_stl_to_image(model_file, model_color=model_color, color_normals=color_normals)



def image_mosaic(folder_path, cols=4, image_ext='.png', figsize=(12, 12), show=False):
    """
    Display a mosaic of images rendered from STL files in a given folder.

    Parameters:
        folder_path (str): Directory containing PNG images.
        cols (int): Number of columns in the mosaic.
        image_ext (str): Image file extension (default: '.png').
        figsize (tuple): Figure size for the mosaic.
    """
    print('Generating image moisaic...')

    # Collect image paths
    image_files = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(image_ext)
    ]

    if not image_files:
        print("No images found.")
        return

    rows = math.ceil(len(image_files) / cols)
    fig, axs = plt.subplots(rows, cols, figsize=figsize)
    axs = axs.flatten()  # Flatten in case of single row

    for ax, img_path in zip(axs, image_files):
        img = mpimg.imread(img_path)
        ax.imshow(img)
        ax.axis('off')
        name = os.path.basename(img_path).split('.')[0]
        ax.set_title(name, fontsize=10)

    # Hide remaining axes if there are any
    for ax in axs[len(image_files):]:
        ax.axis('off')

    plt.tight_layout()
    savepath = os.path.join(folder_path, 'output.pdf')
    plt.savefig(savepath)
    if show: plt.show()



if __name__ == '__main__':
    # render_stl_to_image('/Users/jarbel16/Downloads/Bottles-v0/model-0.stl', show=True, model_color='lightgrey')
    save_path = '/Users/jarbel16/Downloads/chair-stl'
    # render_each(save_path)
    image_mosaic(save_path)