from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import contextily as ctx
import rasterio
from rasterio.plot import show
import os


class PDFDocument:
    """
    A class for generating a PDF report with a title, image overlay, and text.

    Author: Shun Shiina
    """
    def __init__(self, file_path, title="Document", author="Author"):
        """
        Initializes the PDFDocument object.

        :param file_path: The output file path for the generated PDF
        :param title: The title of the document
        :param author: The author of the document
        """
        self.file_path = file_path
        self.title = title
        self.author = author
        self.elements = []
        self.styles = getSampleStyleSheet()

        # Initialize the SimpleDocTemplate
        self.doc = SimpleDocTemplate(file_path, pagesize=letter)

    def add_title(self):
        """
        Defines the title for the PDF
        """
        title_style = self.styles["Title"]
        title = Paragraph(self.title, title_style)
        self.elements.append(title)
        self.elements.append(Spacer(1, 20))

    def add_image(self, raster_path, output_dir):
        """
        Adds the flood risk raster image overlaid on OpenStreetMap at the same position.

        :param raster_path: Path to the raster file
        :param output_dir: Directory where the temp image gets saved
        """
        with rasterio.open(raster_path) as src:
            # Plot the raster data
            fig, ax = plt.subplots(figsize=(8, 8))
            show(src, ax=ax, cmap='Reds')
            ctx.add_basemap(ax, crs=src.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.4)
            ax.axis('off')  # Turn off axes for a clean look

            # Save the figure as a temporary image
            image_path = os.path.join(output_dir, "temp_overlay.png")
            plt.savefig(image_path, bbox_inches="tight")
            plt.close(fig)

        # Add the image to the PDF
        img = Image(image_path, width=500, height=400)
        self.elements.append(img)
        self.elements.append(Spacer(1, 6))

        # Delay file removal until the PDF is saved
        self.temp_image_path = image_path

    def save(self):
        """
        Saves the PDF with all added elements, removes temporary image.
        """
        self.doc.build(self.elements)
        if hasattr(self, 'temp_image_path') and os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def add_bounds(self, bounds):
        """
        Adds information as text to the PDF.
        """
        bounds_text = f"Bounds of the image: {bounds}"
        notice_text = "Darker red indicates a higher flood risk. Lighter red indicates a lower flood risk."
        text = Paragraph(bounds_text, self.styles["BodyText"])
        text2 = Paragraph(notice_text, self.styles["BodyText"])
        self.elements.append(text2)
        self.elements.append(Spacer(1, 20))
        self.elements.append(text)

    def generate_from_raster(self, raster_path, output_dir):
        """
        Main method to build the PDF report. The steps are as follows:
        1. Extracts the bounding box of the raster
        2. Adds a title to the PDF
        3. Overlays the raster image on a map
        4. Includes the bounds of the raster as text
        5. Saves the final PDF document

        :param raster_path: Path to the raster outputted by the main function
        :param output_dir: Directory where the output files get saved
        """
        with rasterio.open(raster_path) as src:
            bounds = src.bounds

        self.add_title()
        self.add_image(raster_path, output_dir)
        self.add_bounds(bounds)
        self.save()
