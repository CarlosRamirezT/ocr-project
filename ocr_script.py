import os
from pypdf import PdfReader
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
        file_path = "/Users/cadara/Documents/CONTABILIDAD Y FINANZAS PERSONALES/Estados de Cuenta 2024 BSC/802840-2024-11-13-to-2024-12-13_241217_104523.pdf"
        file_reader = PdfReader(file_path)
        file_clean_data= list()
        for page in file_reader.pages:

            page_clean_data = list()

            page_text = page.extract_text()
            lines = page_text.splitlines()

            statement_date = datetime.strptime(lines[15].replace('FECHA DE CORTE: ', ''), '%d/%m/%Y').date()

            date_strings = list()
            description_strings = list()
            amount_strings = list()

            for line in lines[85:]:
                # end of data reached, break
                if "TITULAR" in line:
                    break
                
                # for date lines
                if "/" in line and len(line) >= 4 and len(line) <= 5:
                    date_strings.append(line)

                # for amount lines
                elif line[0] == " " and "." in line:
                    amount_strings.append(line)

                # for description lines
                else:
                    description_strings.append(line)

            # clean page data

            lines_real_qty = len(description_strings)
            transaction_date_strings = date_strings[:lines_real_qty]
            account_date_strings = date_strings[lines_real_qty:]

            for transaction_date, account_date, description, amount in zip(
                transaction_date_strings, 
                account_date_strings, 
                description_strings, 
                amount_strings
            ):
                current_date = statement_date
                page_clean_data.append(
                    {
                        'transaction_date': datetime.strptime(transaction_date, '%d/%m').date().replace(year=current_date.year),
                        'account_date': datetime.strptime(account_date, '%d/%m').date().replace(year=current_date.year),
                        'description': description.replace(' * ', '').rstrip(),
                        'amount': float(amount.replace(' ', '').replace(',', ''))
                    }
                )



    
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


if __name__ == "__main__":
    execute()


