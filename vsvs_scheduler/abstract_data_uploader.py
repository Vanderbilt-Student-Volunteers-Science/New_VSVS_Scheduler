from abc import ABC, abstractmethod
import csv
import os

class AbstractDataUploader(ABC):
    def __init__(self, applicant_type: str):
        """ Abstract class for uploading data from csv/excel file into objects."""

        super().__init__()
        self.filename = self.file_prompt(applicant_type)
        self.applicants = []



    def file_prompt(self, applicant_file: str) -> str:
        """ Prompt user for file path to csv/excel file."""

        filename = input(f"Enter the file path to the {applicant_file} file:\n")

        # Keep prompting user until they enter a valid file path
        while (not os.path.isfile(filename)):
            if filename == "" or filename is None:
                filename = f"data/{applicant_file}.csv"
            else:  
                filename = input(f"Enter the file path to the {applicant_file} file:\n")

        print(f"\nImporting {applicant_file} ...")

        return filename
    


    def import_data(self):
        """ Import data from csv/excel file into objects. """

        with open(self.filename) as current_csv:

            # DictReader creates an ordered dictionary for each row in the csv file
            csv_reader = csv.DictReader(current_csv)

            for row in csv_reader:
                self.process_row_data(row)
        
        print (f"\nImport complete. {len(self.applicants)} records added.\n")



    @abstractmethod
    def process_row_data(self, row: dict):
        """ Abstract method for processing row data from csv/excel file into objects. """
        pass

