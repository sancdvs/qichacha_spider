import re
from excel_util import style_title, style


# 导出错误企业信息
def export_error_data(error_data,workbook):
    worksheet = workbook.add_sheet("抓取失败企业信息",cell_overwrite_ok=True)
    worksheet.write(0, 0, u"序号", style_title)
    worksheet.write(0, 1, u"公司名称", style_title)

    worksheet.col(1).width = 256 * 50
    i = 0
    for company_name in error_data:
        i += 1
        worksheet.write(i, 0, i, style)
        worksheet.write(i, 1, company_name, style)
    return worksheet

