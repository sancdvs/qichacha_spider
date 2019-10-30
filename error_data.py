import re

from config import spider_result_file_name, error_data_sheet_name
from excel_util import style_title, style, read_excel_rows, get_sheet_by_name


# 导出错误企业信息
def export_error_data(error_data,workbook, is_exsit):
    start_row = 1  # 数据起始excel行号
    if not is_exsit:
        worksheet = workbook.add_sheet(error_data_sheet_name,cell_overwrite_ok=True)
        worksheet.write(0, 0, u"序号", style_title)
        worksheet.write(0, 1, u"公司名称", style_title)

        worksheet.col(1).width = 256 * 50
    else:
        start_row = read_excel_rows(spider_result_file_name, error_data_sheet_name)
        worksheet = workbook.get_sheet(error_data_sheet_name)

    for company_name in error_data:
        print('公司名称：{}'.format(company_name))
        worksheet.write(start_row, 0, start_row, style)
        worksheet.write(start_row, 1, company_name, style)
        start_row += 1
    return worksheet

