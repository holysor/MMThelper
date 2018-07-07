import xlrd

def get_data_from_excel():
    workbook = xlrd.open_workbook(r'employees.xlsx')
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    employees = []
    for r in range(rows):
        array = []
        for n in range(cols):
            value = sheet.cell(r, n).value
            if n == 1:
                value = value.split('-')[1]
            array.append(value)
        employees.append(array)
    return employees

def get_fail_data():
    workbook = xlrd.open_workbook(r'employees.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    cols = sheet.ncols
    employees = []
    for r in range(rows):
        for n in range(cols):
            value = sheet.cell(r, n).value
            if '失败' in value:
                employees.append(value)
    return employees

print(get_fail_data())