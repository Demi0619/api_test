from class_09.VAR import *
import openpyxl

def read_excel():
    excel_path = EXCEL_PATH
    excel = openpyxl.load_workbook('data/api_cases_demo.xlsx')
    sheet = excel['Sheet1']
    tuple_list = []
    for value in sheet.values:
        if type(value[0]) is int:  # only collect case with case no
            tuple_list.append(value)
    return tuple_list