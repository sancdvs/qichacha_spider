import re

from config import spider_result_file_name
from excel_util import style_title, style, read_excel_rows


# 导出错误企业信息
def export_error_data(error_data,workbook, is_new):
    start_row = 1  # 数据起始excel行号
    if is_new:
        worksheet = workbook.add_sheet("抓取失败企业信息",cell_overwrite_ok=True)
        worksheet.write(0, 0, u"序号", style_title)
        worksheet.write(0, 1, u"公司名称", style_title)

        worksheet.col(1).width = 256 * 50
    else:
        start_row = read_excel_rows(spider_result_file_name, 3)
        worksheet = workbook.get_sheet(3)

    for company_name in error_data:
        worksheet.write(start_row, 0, start_row, style)
        worksheet.write(start_row, 1, company_name, style)
        start_row += 1
    return worksheet

