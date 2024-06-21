#%% Imports -------------------------------------------------------------------

import napari
from skimage import io
from pathlib import Path
from functions import get_voxel_size

# Skimage
from skimage.filters import gaussian, threshold_otsu

#%% Inputs --------------------------------------------------------------------

img_name = "spheroid_series_02.tif"
data_path = Path(Path.cwd(), "data")
img_path = data_path / img_name

# Parameters
sigma = 3
C1_tresh_coeff = 0.75
C2_tresh_coeff = 0.75

#%% Execute -------------------------------------------------------------------

# Read
voxSize = get_voxel_size(img_path)
C1 = io.imread(img_path)[:, 0, ...]
C2 = io.imread(img_path)[:, 1, ...]

# Process
if sigma > 0:
    for z in range(C1.shape[0]):
        C1[z, ...] = gaussian(
            C1[z, ...], sigma=sigma, preserve_range=True)
        C2[z, ...] = gaussian(
            C2[z, ...], sigma=sigma, preserve_range=True)
C1_tresh = threshold_otsu(C1)
C2_tresh = threshold_otsu(C2)
C1_mask = C1 > C1_tresh * C1_tresh_coeff
C2_mask = C2 > C2_tresh * C2_tresh_coeff

#%% Display -------------------------------------------------------------------

# Viewer #1
viewer = napari.Viewer()
viewer.add_image(
    C1, name="channel#1", colormap="green", scale=voxSize,
    blending="additive", rendering="attenuated_mip",
    )
viewer.add_image(
    C2, name="channel#2", colormap="magenta", scale=voxSize,
    blending="additive", rendering="attenuated_mip",
    )
viewer.dims.ndisplay = 3

# Viewer #2
viewer = napari.Viewer()
viewer.add_image(
    C1_mask, name="channel#1", colormap="green", scale=voxSize,
    blending="additive", rendering="attenuated_mip", attenuation=1,
    )
viewer.add_image(
    C2_mask, name="channel#2", colormap="magenta", scale=voxSize,
    blending="additive", rendering="attenuated_mip", attenuation=1,
    )
viewer.dims.ndisplay = 3