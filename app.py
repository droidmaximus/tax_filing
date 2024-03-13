import tkinter as tk
from tkinter import filedialog, simpledialog
import PyPDF2
import requests
import json
import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

class PDFUploader:
    def __init__(self):
        self.user_bank_number = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("PDF Uploader")

        # Create and configure the frame
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(padx=20, pady=20)

        # Create and configure the Upload button
        self.upload_button = tk.Button(self.frame, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        # Run the Tkinter event loop
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.root.mainloop()

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.download_pdf(file_path)

    def download_pdf(self, file_path):
        try:
            # Get user's bank number as input
            self.get_user_bank_number()

            # Call the fake API to get financials
            financials = self.get_user_financials()

            # Open the PDF file locally
            with open(file_path, 'rb') as local_file:
                pdf_reader = PyPDF2.PdfReader(local_file)
                num_pages = len(pdf_reader.pages)
                print(f"Number of pages in the PDF: {num_pages}")

                # Download the PDF from the local file path
                pdf_output_path = os.path.join("coding", "financials.pdf")
                with open(pdf_output_path, 'wb') as downloaded_file:
                    downloaded_file.write(local_file.read())

                print("PDF downloaded and saved as financials.pdf")

            # Save financials as JSON
            self.save_financials_to_json(financials)

            print(f"User's bank number: {self.user_bank_number}")
        except Exception as e:
            print(f"Error processing or downloading PDF: {e}")

    def get_user_bank_number(self):
        # Function to get user's bank number as input within the Tkinter UI
        user_bank_number_input = simpledialog.askstring("User Bank Number", "Enter your bank number:")
        if user_bank_number_input is not None:
            self.user_bank_number = user_bank_number_input

    def get_user_financials(self):
        # Function to call the fake API and get user financials
        api_url = f"http://127.0.0.1:5000/api/financials?bank_number={self.user_bank_number}"
        response = requests.get(api_url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching financials from API: {response.status_code}")
            return None

    def save_financials_to_json(self, financials):
        # Function to save financials as JSON
        if financials:
            json_output_path = os.path.join("coding", "financials.json")
            with open(json_output_path, 'w') as json_file:
                json_file.write(json.dumps(financials, indent=2))
            print("Financials saved as financials.json")

    def on_window_close(self):
        config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
        assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
        user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False})
        user_proxy.initiate_chat(assistant, message="Read the data from financials.pdf and financials.json and give a tax report based on the data, and save the tax report in an excel file in the same coding folder. financials.json contains transactions and account_balance along with each transactions containing amount, date and description. Read the pdf file using an ocr, and extract the text and feed it back to the llm so that it can generate a tax report.")
        self.root.destroy()

# Create an instance of the PDFUploader class
pdf_uploader = PDFUploader()