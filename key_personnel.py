import re
from excel_util import *


# 导出企业主要人员
def export_key_personnel(data_list, workbook):
    worksheet = workbook.add_sheet("主要人员", cell_overwrite_ok=True)
    worksheet.write(0, 0, "序号", style_title)
    worksheet.write(0, 1, "公司名称", style_title)
    worksheet.write(0, 2, "姓名", style_title)
    worksheet.write(0, 3, "职务", style_title)
    # 设置表格列宽
    for i in range(4):
        if i == 0:
            continue
        else:
            worksheet.col(i).width = 256 * 20
    i = 0
    j = 0
    for _response in data_list:
        j += 1
        # 公司名称
        company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)[0].strip()
        print('公司名称：' + company_name)
        personnel_list = re.findall('<a class="employee-item" href=".*?" style="display: block;">(\s*.*?\s*)</a>', _response)
        # print(personnel_list)
        if len(personnel_list) > 0:
            worksheet.write_merge(i + 1, i + len(personnel_list), 0, 0, j, style_merge)  # 合并序号单元格
            worksheet.write_merge(i + 1, i + len(personnel_list), 1, 1, company_name, style_merge)  # 合并公司名称单元格
        else:
            worksheet.write(i+1, 0, j, style)
            worksheet.write(i+1, 1, company_name, style)
            worksheet.write(i+1, 2, '--', style)
            worksheet.write(i+1, 3, '--', style)
            i += 1

        for personnel in personnel_list:
            i += 1
            # 姓名
            name = re.findall('<div class="employee-name">(\s*.*?\s*)</div>', personnel)[0].strip()
            print('姓名：' + name)
            worksheet.write(i, 2, name, style)  # 将信息输入表格
            # 职务
            job = re.findall('<div class="employee-job">(\s*.*?\s*)</div>', personnel)[0].strip()
            print('职务：' + job)
            worksheet.write(i, 3, job, style)  # 将信息输入表格
        print('----------------------------------------------------------------------')
    return worksheet
