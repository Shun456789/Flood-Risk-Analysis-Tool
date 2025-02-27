# Documentation of Functions and Custom Classes

This page provides an overview of all functions and custom classes in the tool, discussing their actions, input arguments, and output data types.

## 1. `main.py`

### **`create_summary_table(risk_data, inundation_data, land_use_data, output_path)`**
Generates a statistical summary table based on risk, inundation, and land use data and saves it as a CSV file.

#### **Input Arguments**
- `risk_data` (`np.ndarray`): Flood risk raster data.
- `inundation_data` (`np.ndarray`): Inundation raster data.
- `land_use_data` (`np.ndarray`): Land use raster data.
- `output_path` (`str`): Path to save the CSV file.

#### **Output**
- None (CSV file is saved).

---

### **`calculate_risk_by_land_use(risk_data, land_use_data, no_data_value, output_path)`**
Calculates total, average, and count of risk values for each land use category and saves the outcome as a CSV file.

#### **Input Arguments**
- `risk_data` (`np.ndarray`): Flood risk raster data.
- `land_use_data` (`np.ndarray`): Land use raster data.
- `no_data_value` (`float`): No-data pixel value.
- `output_path` (`str`): Path to save the CSV file.

#### **Output**
- None (CSV file is saved).

---

### **`main()`**
Executes the flood risk analysis workflow by collecting user inputs, processing raster data, computing risk, and generating outputs.

#### **Input Arguments**
- None (User inputs are collected via GUI).

#### **Output**
- None (Generates output files: GeoTIFF, CSV, and optional PDF).

---

## 2. `gui.py`

### **`launch_gui()`**
Launches a GUI to collect user inputs and returns a dictionary of parameters defined by users.

#### **Input Arguments**
- None.

#### **Output**
- `dict`: A dictionary holding user-defined parameters such as return period, file paths, and output settings.

---

## 3. `raster.py`

### **`Raster` Class**
A class for handling raster datasets, as well as loading, resampling, and saving.

#### **Methods**

#### **`__init__(self, file_path=None)`**
Initializes a `Raster` object and loads a raster if a file path is provided.

- `file_path` (`str` or `None`): Path to the raster file.

#### **`resample_raster(self, raster2_path)`**
Resamples another raster to match the current raster’s resolution and CRS.

- `raster2_path` (`str`): Path to the raster file to be resampled.
- **Returns:** `np.ndarray` containing resampled raster data.

#### **`save_raster(self, output_path, data, no_data_value=None)`**
Saves a raster to a new file.

- `output_path` (`str`): Path where the raster will be saved.
- `data` (`np.ndarray`): Raster data to save.
- `no_data_value` (`float` or `None`): No-data value for metadata.

---

## 4. `pdfdocument.py`

### **`PDFDocument` Class**
A class for generating PDF reports with flood risk maps and descriptions.

#### **Methods**

#### **`__init__(self, file_path, title="Document", author="Author")`**
Initializes a `PDFDocument` object.

- `file_path` (`str`): Output file path for the created PDF.
- `title` (`str`): Title of the document.
- `author` (`str`): Author of the document.

#### **`add_title(self)`**
Adds a title to the PDF.

#### **`add_image(self, raster_path, output_dir)`**
Adds a flood risk raster image overlaid on OpenStreetMap to the PDF.

- `raster_path` (`str`): Path to the raster file.
- `output_dir` (`str`): Directory for saving the temporary image.

#### **`add_bounds(self, bounds)`**
Adds bounding box information as text to the PDF.

- `bounds` (`tuple`): Raster bounding box `(min_x, min_y, max_x, max_y)`.

#### **`save(self)`**
Saves the PDF and removes temporary image files.

#### **`generate_from_raster(self, raster_path, output_dir)`**
Generates a complete PDF report from a raster.

- `raster_path` (`str`): Path to the raster output file.
- `output_dir` (`str`): Directory for saving output files.

---
