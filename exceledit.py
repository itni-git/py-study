import openpyxl

file_path = 'testA.xlsx'
old_name = '황은율'
new_name = '황가달'

try:
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active  # Assuming the data is on the first sheet

    # Iterate through all cells to find and replace the string
    for row in sheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and old_name in cell.value:
                cell.value = new_name

    workbook.save(file_path)
    print(f"Successfully replaced '{old_name}' with '{new_name}' in {file_path}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")