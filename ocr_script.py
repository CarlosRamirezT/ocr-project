import os
import re
from pypdf import PdfReader
import pdfplumber
from datetime import datetime

OPERATION_OPTIONS = {
    1: "Convert PDF to Excel"
}

def execute():
    # display files in this route
    # and ask user to select which file(s) to parse
    print("Welcome to Cadara's Personal OCR Script!")
    print("Please select the operation you want to perform:")
    print()
    for option, description in OPERATION_OPTIONS.items():
        print(f'{option}: {description}')
    print()
    
    # operation_option = input("Option: ")

    # if operation_option == "1":
        # execute_convert_pdf_to_excel()

def execute_convert_pdf_to_excel():
    file_paths = _get_files_to_convert()
    output_mode = _get_output_mode()

    for file_path in file_paths:
        file = pdfplumber.open(file_path)
        # get data depending on file type and bank
        file_data = _get_file_data(file)
        # write data to excel
        
def _get_files_to_convert(path=False):
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    if not path:
        print(f"""
        Please select the directory you want to work on:
            
        1 (current path): {current_path}
        2 (parent path): {parent_path}
        3 (other path) ...

        """)
        
        dir_option = input("Select the option:")

        if dir_option == "1":
            path = current_path
        elif dir_option == "2":
            path = parent_path
        elif dir_option == "3":
            path = input("Enter the path to work on:")

        file_names = [entry.name for entry in os.scandir(path) if entry.is_file()]

        print("Please, select the files that you want to work with. (comma separated number of file(s)):")
        print()
        for i, file_name in enumerate(file_names):
            no = i + 1
            print(f'{no}: {file_name}')
        print()
        file_numbers = input("Enter file numbers (comma separated):").split(",")

        file_paths = [path + '/' + file_names[int(number) - 1] for number in file_numbers]
        
        return file_paths
    
def _get_output_mode():
    print("""
    How do you want to convert these files?
          
    1. Into a single excel file
    2. Separate excel files
          
    """)

    output_option = input("Select your option:")

    if output_option == "1":
        output_mode = 'single_file'
    elif output_option == "2":
        output_mode = 'multiple_files'

    return output_mode

def _get_file_data(file):
    
    file_data = dict()
    file_data['lines'] = list()

    for page in file.pages:
        page_text = page.extract_text()
        lines = page_text.splitlines()

        statement_date = datetime.strptime(lines[4].replace('FECHA DE CORTE: ', ''), '%d/%m/%Y').date()

        file_data['statement_date'] = statement_date
        file_data['product_name'] = lines[1].split(": ")[1]
        file_data['product_number'] = lines[2].split(": ")[1]
        file_data['customer_name'] = lines[3].split(": ")[1]

        for i, line in enumerate(lines[19:]):
            # if last line of the page, break
            if 'PUNTOS GANADOS PDUNTOS' in line:
                break
            if line[2] != "/":
                continue

            try:
                file_data['lines'].append(
                    {
                        'transaction_date': datetime.strptime(line.split(' ')[0], '%d/%m').date().replace(year=statement_date.year),
                        'account_date': datetime.strptime(line.split(' ')[1], '%d/%m').date().replace(year=statement_date.year),
                        'description': line[12:].split(' * ')[0],
                        'amount': float(line[12:].split(' * ')[1].replace(',', ''))
                    }
                )
            except Exception as e:
                print(f'error on line: idx: {i}: {line}')
                raise e
    return file_data['lines']


# if __name__ == "__main__":
#     execute()


