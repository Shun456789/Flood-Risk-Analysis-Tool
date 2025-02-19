from raster import Raster
import pandas as pd
import numpy as np
import config
import gui
import os
from pdfdocument import PDFDocument


def create_summary_table(risk_data, inundation_data, land_use_data, output_path):
    """
    Generates a statistical summary table based on risk, inundation, land use and saves it as a CSV file.

    :param risk_data: numpy array with risk raster data
    :param inundation_data: numpy array with inundation raster data
    :param land_use_data: numpy array with land use raster data
    :param output_path: string where CSV will be saved
    """
    summary = {
        "Raster": ["Risk", "Inundation", "Land Use"],
        "Mean": [np.nanmean(risk_data), np.nanmean(inundation_data), np.nanmean(land_use_data)],
        "Median": [np.nanmedian(risk_data), np.nanmedian(inundation_data), np.nanmedian(land_use_data)],
        "Standard Deviation": [np.nanstd(risk_data), np.nanstd(inundation_data), np.nanstd(land_use_data)],
        "Minimum": [np.nanmin(risk_data), np.nanmin(inundation_data), np.nanmin(land_use_data)],
        "Maximum": [np.nanmax(risk_data), np.nanmax(inundation_data), np.nanmax(land_use_data)],
    }
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(output_path, index=False)
    print(f"Summary table saved to {output_path}")


def calculate_risk_by_land_use(risk_data, land_use_data, no_data_value, output_path):
    """
    Computes the total, average, and count of risk values for each land use category, saves as CSV file.

    :param risk_data: numpy array with risk raster data
    :param land_use_data: numpy array with land use raster data
    :param no_data_value: number representing the no-data pixels, exclude from statistics
    :param output_path: string where CSV will be saved
    """
    # Flatten arrays for analysis, make PD dataframe
    risk_flat = risk_data.flatten()
    land_use_flat = land_use_data.flatten()
    df = pd.DataFrame({"Land Use": land_use_flat, "Risk": risk_flat})

    # Remove no-data values
    df = df[df["Risk"] != no_data_value]

    # Group by land-use type and calculate stats
    risk_summary = df.groupby("Land Use")["Risk"].agg(["sum", "mean", "count"]).reset_index()
    risk_summary.columns = ["Land Use Category", "Total Risk", "Average Risk", "Pixel Count"]

    # Save to file
    risk_summary.to_csv(output_path, index=False)
    print(f"Risk breakdown by land use saved to {output_path}")


def main():
    """
    Executes the flood risk analysis workflow, following these steps:
    1. Launches a GUI to collect user inputs.
    2. Loads and processes raster datasets (flood depth, land use, and optionally velocity).
    3. Resamples the land-use raster to match the flood depth raster resolution.
    4. Computes flood risk using land use values and inundation characteristics.
    5. Saves the computed risk raster as a GeoTIFF file.
    6. Generates statistical summaries and CSV outputs for risk analysis.
    7. Optionally generates a PDF report summarizing the results.
    """
    #### BEGIN SECTION OF GUI
    # Launch GUI and get user inputs
    user_inputs = gui.launch_gui()

    # Extract inputs
    return_period = user_inputs["return_period"]
    no_data_value = user_inputs["no_data_value"]
    flood_depth_file = user_inputs["flood_depth_file"]
    velocity_file = user_inputs.get("velocity_file")  # Optional, defaults to None if not provided
    output_dir = user_inputs["output_dir"]

    #### END SECTION OF GUI
    #### BEGIN SECTION OF RASTER CLASS INIT, TRANSFORM, RESAMPLE

    # File path and values for land use map
    land_use_path = config.LAND_USE_PATH
    land_use_map = config.LAND_USE_MAP

    # Instantiate Raster objects
    inundation_raster = Raster(flood_depth_file)
    land_use_raster = Raster(land_use_path)
    velocity_raster = Raster(velocity_file) if velocity_file else None

    # Resample land-use raster to match inundation raster
    resampled_land_use = inundation_raster.resample_raster(land_use_path)

    # Update the land_use_raster object with the resampled data
    land_use_raster.data = resampled_land_use
    land_use_raster.transform = inundation_raster.transform
    land_use_raster.bounds = inundation_raster.bounds

    #### END SECTION OF RASTER CLASS INIT, TRANSFORM, RESAMPLE
    #### BEGIN SECTION OF RISK CALCULATION

    # Calculation of the value (of the pixelated property)
    land_use_values = np.vectorize(land_use_map.get)(resampled_land_use.data)

    # Handle the optional velocity raster, only if it was inputted
    if velocity_raster:
        velocity_inundation_product = np.where(
            velocity_raster.data > config.VELOCITY_THRESHOLD,
            inundation_raster.data * velocity_raster.data,
            inundation_raster.data
        )
    else:
        velocity_inundation_product = inundation_raster.data

    # Calculation of the damage and risk
    damage = land_use_values * velocity_inundation_product
    risk = damage * (1 / return_period)

    # Replace 0s in risk array with the no_data_value
    risk_cleaned = np.where(risk == 0, no_data_value, risk)

    # Creates new empty risk raster and then fills it with calculated risk data, so it can be saved
    risk_raster = Raster(file_path=None)
    risk_raster.data = risk_cleaned
    risk_raster.transform = inundation_raster.transform
    risk_raster.crs = inundation_raster.crs
    risk_raster.bounds = inundation_raster.bounds

    # Concatenates the user-defined output path with the output tif and then saves it
    output_path = os.path.join(output_dir, "risk_output.tif")
    risk_raster.save_raster(output_path, risk_raster.data, no_data_value=no_data_value)
    print(f"Risk raster saved to {output_path}")
    print(f"Risk raster CRS: {risk_raster.crs}")

    #### END SECTION OF RISK CALCULATION
    #### BEGIN SECTION OF STATISTICS SUMMARY, PDF GENERATION

    # Generates PDF
    if user_inputs.get("generate_pdf"):
        print("Generating PDF...")
        pdf_output_path = os.path.join(output_dir, "FloodRiskAnalysis.pdf")
        pdf = PDFDocument(pdf_output_path, title="Flood Risk Summary", author="Automated System")
        pdf.generate_from_raster(output_path, output_dir)
        print(f"PDF saved to {pdf_output_path}")

    summary_csv_path = os.path.join(output_dir, "summary_table.csv")
    create_summary_table(risk_cleaned, inundation_raster.data, land_use_values, summary_csv_path)

    land_use_risk_csv_path = os.path.join(output_dir, "land_use_risk.csv")
    calculate_risk_by_land_use(risk_cleaned, land_use_values, no_data_value, land_use_risk_csv_path)

    ### END SECTION OF STATISTICS SUMMARY

if __name__ == "__main__":
    # Run the main function when this script is executed
    main()