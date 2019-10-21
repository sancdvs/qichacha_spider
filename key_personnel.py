import re

from config import spider_result_file_name
from excel_util import *


# 导出企业主要人员
def export_key_personnel(data_list, workbook, is_new):
    start_row = 1  # 数据起始excel行号
    order_number = 0  # 数据起始序号
    if is_new:
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
    else:
        start_row = read_excel_rows(spider_result_file_name, 2)
        worksheet = workbook.get_sheet(2)
        order_number = get_merged_cells_value(spider_result_file_name, 2, start_row - 1, 0)  # 序号位置是第一列

    for _response in data_list:
        order_number += 1
        # 公司名称
        company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)
        if len(company_name) > 0:
            company_name = company_name[0].strip()
        else:
            company_name = '--'
        print('公司名称：' + company_name)
        personnel_list = re.findall('<a class="employee-item" href=".*?" style="display: block;">(\s*.*?\s*)</a>', _response)
        # print(personnel_list)
        if len(personnel_list) > 0:
            worksheet.write_merge(start_row, start_row + len(personnel_list)-1, 0, 0, order_number, style_merge)  # 合并序号单元格
            worksheet.write_merge(start_row, start_row + len(personnel_list)-1, 1, 1, company_name, style_merge)  # 合并公司名称单元格
        else:
            worksheet.write(start_row, 0, order_number, style)
            worksheet.write(start_row, 1, company_name, style)
            worksheet.write(start_row, 2, '--', style)
            worksheet.write(start_row, 3, '--', style)
            start_row += 1

        for personnel in personnel_list:
            # 姓名
            name = re.findall('<div class="employee-name">(\s*.*?\s*)</div>', personnel)
            if len(name) > 0:
                name = name[0].strip()
            else:
                name = '--'
            print('姓名：' + name)
            worksheet.write(start_row, 2, name, style)  # 将信息输入表格
            # 职务
            job = re.findall('<div class="employee-job">(\s*.*?\s*)</div>', personnel)
            if len(job) > 0:
                job = job[0].strip()
            else:
                job = '--'
            print('职务：' + job)
            worksheet.write(start_row, 3, job, style)  # 将信息输入表格
            start_row += 1
        # print('----------------------------------------------------------------------')
    return worksheet
