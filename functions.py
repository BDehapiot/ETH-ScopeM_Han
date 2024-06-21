#%% Imports -------------------------------------------------------------------

import tifffile

#%% Functions -----------------------------------------------------------------

def get_voxel_size(file_path):

    def _xy_voxel_size(tags, key):
        assert key in ['XResolution', 'YResolution']
        if key in tags:
            num_pixels, units = tags[key].value
            return units / num_pixels
        return 1.

    with tifffile.TiffFile(file_path) as tiff:
        image_metadata = tiff.imagej_metadata
        if image_metadata is not None:
            z = image_metadata.get('spacing', 1.)
        else:
            z = 1.
        tags = tiff.pages[0].tags
        y = _xy_voxel_size(tags, 'YResolution')
        x = _xy_voxel_size(tags, 'XResolution')
        return [z, y, x]