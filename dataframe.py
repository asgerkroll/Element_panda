# dataframe.py
from element import Element
import pandas as pd
import os
from datetime import datetime
import random


class AddNewElement:
    def __init__(self, element: Element, amount: int):  # New parameter for amount
        now = datetime.now()
        self.element = element
        self.current_date = now.strftime("%d-%m-%y")
        self.source = os.getlogin()
        self.amount = amount

    def new_dataframe(self):
        # Create a new DataFrame from the user input
        # Repeat the data `amount` times using pd.concat
        if "Steel" in self.element.type:
            self.new_data = pd.concat([self.generate_dataframe("-") for _ in range(self.amount)], ignore_index=True)
        else:
            self.new_data = pd.concat([self.generate_dataframe(self.element.concrete_type) for _ in range(self.amount)], ignore_index=True)

    def generate_dataframe(self, concrete_type):
        self.SKU = self.element.type[1] + str(self.element.width) + str(random.randint(1, 1000))
        single_data = pd.DataFrame({"Element type": [self.element.type],
                                    "Internal_name": [self.element.internal_name],
                                    "Height": [self.element.height],
                                    "Width": [self.element.width],
                                    "Thickness": [self.element.thickness],
                                    "Vertical load design": [self.element.vertical_load_design],
                                    "Horizontal load design": [self.element.horizontal_load_design],
                                    "Steel type": [self.element.steel_type],
                                    "Concrete type": [concrete_type],
                                    "Date added": [self.current_date],
                                    "Source": [self.source],
                                    "SKU": [self.SKU]})
        return single_data
    def write_csv(self):
        # Try to read the existing data
        try:
            df = pd.read_csv("data.csv")
            df = pd.concat([df, self.new_data], ignore_index=True)  # Concatenate the new data to the existing data
        except pd.errors.EmptyDataError:  # If the file is empty or doesn't exist, use the new data as the DataFrame
            df = self.new_data

        # Write the DataFrame to the CSV file
        df.to_csv("data.csv", index=False)
