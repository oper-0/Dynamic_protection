# Модуль, который преобразует excel формулы в python
import pycel as px

excel_compiler = px.ExcelCompiler("calc.xlsx")
excel_compiler.evaluate("Sheet1!U4")
# excel_compiler.evaluate("Sheet1!U10")
excel_compiler.to_file()

# print(excel_compoler.evaluate("Sheet1!A3"))
