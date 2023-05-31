from dataframe import AddNewElement
from element import Element
from pandasgui import show
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.units = {}
        self.entries = {}

        # Define UI elements
        self.input_fields = ['Internal name', 'Height/Length', 'Width', 'Thickness', 'Vertical load design',
                             'Horizontal load design', 'Steel type', 'Concrete type', 'Amount']
        self.units = ['-', 'mm', 'mm', 'mm', 'kN/m^2 or kN/m (Largest load)', 'kN/m^2 or kN/m (Largest load)',
                      'S235, S460 etc.', 'C25, C35 etc.', 'Number']  # Corresponding units for each input field
        self.element_type = tk.StringVar()  # For the dropdown menu

        # Initial image
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(f"wall.png")))

        # Dropdown menu for Element type
        self.create_dropdown('Element type:')

        for field, unit in zip(self.input_fields, self.units):
            self.create_widgets(field, unit)

        self.create_buttons()

        # Create a frame for the image
        self.image_frame = tk.Frame(self.master)  # self.master is the parent
        # Arrange image_frame with grid
        self.image_frame.grid(column=2, row=0, rowspan=6, padx=10, pady=10, sticky='n')

        # Create an image label
        self.image_label = tk.Label(self.image_frame, image=self.img)
        self.image_label.grid()

    def create_dropdown(self, field):
        label = tk.Label(self, text=field)
        label.grid(row=0, column=0)

        self.element_type.trace('w', lambda *args: self.update_image_and_concrete(self.element_type.get()))

        dropdown = tk.OptionMenu(self, self.element_type, 'Wall', 'Hollow core', 'TTS-Beam', 'HEB', 'HEA', 'HEM', 'IPE')
        dropdown.grid(row=1, column=0)

    def create_widgets(self, field, unit):
        label = tk.Label(self, text=field)
        label.grid()
        entry = tk.Entry(self)
        entry.grid()

        # Add unit label
        unit_label = tk.Label(self, text=unit)
        unit_label.grid()

        self.entries[field] = entry

    def create_buttons(self):
        submit_button = tk.Button(self, text="Submit", fg="red", command=self.submit_data)
        submit_button.grid()

        view_button = tk.Button(self, text="View Data", fg="blue", command=self.view_data)
        view_button.grid()

    def submit_data(self):
        element_type = self.element_type.get()
        internal_name = self.entries['Internal name'].get()
        height = float(self.entries['Height/Length'].get())
        width = float(self.entries['Width'].get())
        thickness = float(self.entries['Thickness'].get())
        vertical_load_design = float(self.entries['Vertical load design'].get())
        horizontal_load_design = float(self.entries['Horizontal load design'].get())
        steel_type = self.entries['Steel type'].get() if self.entries['Steel type'].get() else None
        concrete_type = self.entries['Concrete type'].get() if self.entries['Concrete type'].get() else None
        amount = int(self.entries['Amount'].get())

        element = Element(element_type, internal_name, height, width, thickness, vertical_load_design,
                          horizontal_load_design, steel_type, concrete_type)
        new_element = AddNewElement(element, amount)

        new_element.new_dataframe()
        new_element.write_csv()

        for field in self.input_fields:
            self.entries[field].delete(0, tk.END)

    def view_data(self):
        try:
            df = pd.read_csv("data.csv")
            show(df)
        except pd.errors.EmptyDataError:
            print("The file is empty or doesn't exist.")

    def update_image_and_concrete(self, value):
        if value in ['HEB', 'HEA', 'HEM', 'IPE']:
            self.entries['Concrete type'].config(state='disabled')
            img_path = os.path.join(f"steel_beam.png")
            self.img = ImageTk.PhotoImage(Image.open(img_path))
            self.image_label.config(image=self.img)
            self.image_label.image = self.img
        elif value in ['Wall']:
            self.entries['Concrete type'].config(state='normal')
            img_path = os.path.join(f"wall.png")
            self.img = ImageTk.PhotoImage(Image.open(img_path))
            self.image_label.config(image=self.img)
            self.image_label.image = self.img
        elif value in ['Hollow core']:
            self.entries['Concrete type'].config(state='normal')
            img_path = os.path.join(f"hollow_core.png")
            self.img = ImageTk.PhotoImage(Image.open(img_path))
            self.image_label.config(image=self.img)
            self.image_label.image = self.img
        elif value in ['TTS-Beam']:
            self.entries['Concrete type'].config(state='normal')
            img_path = os.path.join(f"TTS_beam.png")
            self.img = ImageTk.PhotoImage(Image.open(img_path))
            self.image_label.config(image=self.img)
            self.image_label.image = self.img
        else:
            img_path = os.path.join("wall.png")  # Default image if specific one doesn't exist
            self.img = ImageTk.PhotoImage(Image.open(img_path))
            self.image_label.config(image=self.img)
            self.image_label.image = self.img


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
