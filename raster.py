import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

class Raster:
    """
    A class for handling raster datasets (loading, resampling, and saving)

    Author: Hunter Moe
    """
    def __init__(self, file_path=None):
        """
        Initializes the Raster object.

        :param file_path: Path to the raster file. If provided, the raster is loaded automatically
        """
        self.file_path = file_path
        self.crs = None
        self.transform = None
        self.bounds = None
        self.resolution = None
        self.data = None

        # Only load the raster if file_path is provided (i.e. not None) - needed for the empty raster creation
        if self.file_path:
            self._load_raster()

    def _load_raster(self):
        """
        Loads the raster file into memory, extracting CRS, transform, bounds, and resolution.
        """
        with rasterio.open(self.file_path) as src:
            self.crs = src.crs
            self.transform = src.transform
            self.bounds = src.bounds
            self.resolution = src.res  # (x_res, y_res)
            self.data = src.read(1)  # First band

    def resample_raster(self, raster2_path):
        """
        Resamples another raster to match the current raster's resolution and CRS.

        NOTE! Uses bilinear interpolation for continuous data, although consider using nearest-neighbor resampling

        :param raster2_path: Path to the raster file to be resampled
        :return: A numpy array with resampled raster data
        """
        with rasterio.open(raster2_path) as src2:
            # Calculate the transform and dimensions for the target raster (self)
            transform, width, height = calculate_default_transform(
                src2.crs, self.crs, self.data.shape[1], self.data.shape[0], *self.bounds
            )

            # Prepare the resampled raster array
            resampled_data = np.empty((self.data.shape[0], self.data.shape[1]), dtype=src2.meta['dtype'])

            # Perform the resampling
            reproject(
                source=rasterio.band(src2, 1),
                destination=resampled_data,
                src_transform=src2.transform,
                src_crs=src2.crs,
                dst_transform=self.transform,
                dst_crs=self.crs,
                resampling=Resampling.bilinear  # Change to nearest for categorical data
            )

        return resampled_data

    def save_raster(self, output_path, data, no_data_value=None):
        """
        Saves the raster to a new file.

        :param output_path: The file path where the raster will be saved
        :param data: A numpy array containing the raster data
        :param no_data_value: No-data value to be assigned in the metadata (if defined, QGIS will recognize it automatically)
        """
        with rasterio.open(
                output_path,
                'w',
                driver='GTiff',
                height=data.shape[0],
                width=data.shape[1],
                count=1,
                dtype=data.dtype,
                crs=self.crs,
                transform=self.transform
        ) as dst:
            dst.write(data, 1)
            if no_data_value is not None:
                dst.nodata = no_data_value