import tkinter as tk
from tkinter import filedialog, messagebox

def launch_gui():
    """
    Launches the gui for flood risk analysis user inputs: return period, no data value, file paths, optional PDF generation.

    Returns dictionary containing user-defined parameters:
        - "return_period" (int): The flood return period
        - "no_data_value" (float): The no-data value used in analysis
        - "flood_depth_file" (str): Path to the inundation file
        - "velocity_file" (str or None): Path to the optional flow velocity file
        - "output_dir" (str): Directory for saving output files
        - "generate_pdf" (bool): Whether to generate a PDF report
    """
    def on_run_script():
        """
        Collects user inputs from the gui, stores them in user_inputs dictionary, ensures fields are filled
        """
        try:
            # Collect values from the GUI
            return_period = return_period_var.get()
            no_data_value = no_data_var.get()
            flood_depth_file = flood_depth_var.get()
            velocity_file = flow_velocity_var.get() or None  # Optional
            output_dir = output_path_var.get()
            generate_pdf = generate_pdf_var.get()

            # Validate mandatory inputs
            if not all([return_period, no_data_value, flood_depth_file, output_dir]):
                raise ValueError("All mandatory fields must be filled in!")

            # Save inputs in the global dictionary
            nonlocal user_inputs
            user_inputs = {
                "return_period": return_period,
                "no_data_value": no_data_value,
                "flood_depth_file": flood_depth_file,
                "velocity_file": velocity_file,
                "output_dir": output_dir,
                "generate_pdf": generate_pdf
            }

            # Close GUI
            root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # File selection dialogs
    def select_file(variable):
        """
        Opens a file dialog for selecting a file (inundation or flow velocity) and assigns the selected file path as a variable.

        :param variable: The variable to store the selected file path
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            variable.set(file_path)

    def select_output_directory(variable):
        """
        Opens a file dialog for selecting a folder (output directory) and assigns the selected file path as a variable.

        :param variable: The variable to store the selected file path
        """
        output_path = filedialog.askdirectory()
        if output_path:
            variable.set(output_path)

    # Initialize GUI
    root = tk.Tk()
    root.title("Flood Risk Analysis Configuration")

    # Input fields
    return_period_var = tk.IntVar()
    no_data_var = tk.DoubleVar()
    flood_depth_var = tk.StringVar()
    flow_velocity_var = tk.StringVar()
    output_path_var = tk.StringVar()
    generate_pdf_var = tk.BooleanVar()

    fields = [
        ("Return Period:", return_period_var),
        ("No-Data Value:", no_data_var),
    ]

    file_fields = [
        ("Inundation File:", flood_depth_var, select_file),
        ("Flow Velocity File (Optional):", flow_velocity_var, select_file),
        ("Output Directory:", output_path_var, select_output_directory),
    ]

    for idx, (label, var) in enumerate(fields):
        tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(root, textvariable=var).grid(row=idx, column=1, padx=10, pady=5, sticky="we")

    for idx, (label, var, browse_function) in enumerate(file_fields, start=len(fields)):
        tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(root, textvariable=var, width=40).grid(row=idx, column=1, padx=10, pady=5, sticky="we")
        tk.Button(root, text="Browse...", command=lambda v=var, func=browse_function: func(v)).grid(row=idx, column=2, padx=10, pady=5)

    # Checkbox for PDF generation
    tk.Checkbutton(root, text="Generate PDF", variable=generate_pdf_var).grid(
        row=len(fields) + len(file_fields), column=0, columnspan=3, pady=10
    )

    # Run button
    tk.Button(root, text="Run Script", command=on_run_script).grid(
        row=len(fields) + len(file_fields) + 1, column=0, columnspan=3, pady=20
    )

    user_inputs = None
    root.mainloop()

    return user_inputs  # Return the user inputs dictionary after GUI is closed