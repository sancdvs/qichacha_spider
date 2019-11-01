import re

from config import spider_result_file_name, key_personnel_sheet_name
from excel_util import *
from log import logging

# 导出企业主要人员
def export_key_personnel(data_list, workbook, is_exsit):
    start_row = 1  # 数据起始excel行号
    order_number = 0  # 数据起始序号
    if not is_exsit:
        worksheet = workbook.add_sheet(key_personnel_sheet_name, cell_overwrite_ok=True)
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
        start_row = read_excel_rows(spider_result_file_name, key_personnel_sheet_name)
        worksheet = workbook.get_sheet(key_personnel_sheet_name)
        order_number = int(get_merged_cells_value(spider_result_file_name,key_personnel_sheet_name, start_row - 1, 0))  # 序号位置是第一列

    for _response in data_list:
        order_number += 1
        # 公司名称
        company_name = _response.find(class_="content")
        if company_name is not None:
            company_name = company_name.select('h1')[0].text.replace('\n', '').replace(' ', '') if len(company_name.select('h1')) > 0 else '无'
        print('公司名称：' + company_name)
        personnel_array = _response.select("#Mainmember > table > tbody > tr")  # 包含了标题tr
        # print(personnel_array)
        if len(personnel_array)-1 > 0:
            worksheet.write_merge(start_row, start_row + len(personnel_array)-2, 0, 0, order_number, style_merge)  # 合并序号单元格
            worksheet.write_merge(start_row, start_row + len(personnel_array)-2, 1, 1, company_name, style_merge)  # 合并公司名称单元格
        else:
            worksheet.write(start_row, 0, order_number, style)
            worksheet.write(start_row, 1, company_name, style)
            worksheet.write(start_row, 2, '--', style)
            worksheet.write(start_row, 3, '--', style)
            start_row += 1

        if len(personnel_array) == 0:
            logging.error('未找到该公司主要人员============{}'.format(company_name))

        if len(personnel_array) > 1:
            for i in range(1, len(personnel_array)):
                # 姓名
                if len(personnel_array[i].select('td')) > 1 and len(personnel_array[i].select('td')[1].select('h3')) > 0:
                    name = personnel_array[i].select('td')[1].select('h3')[0].text.replace('\n', '').replace(' ', '')
                print('姓名：' + name)
                worksheet.write(start_row, 2, name, style)  # 将信息输入表格
                # 职务
                if len(personnel_array[i].select('td')) > 2:
                    job = personnel_array[i].select('td')[2].text.replace('\n', '').replace(' ', '')
                print('职务：' + job)
                worksheet.write(start_row, 3, job, style)  # 将信息输入表格
                start_row += 1

        # order_number += 1
        # 公司名称
        # company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)
        # if len(company_name) > 0:
        #     company_name = company_name[0].strip()
        # else:
        #     company_name = '--'
        # print('公司名称：' + company_name)
        # personnel_list = re.findall('<a class="employee-item" href=".*?" style="display: block;">(\s*.*?\s*)</a>', _response)
        # # print(personnel_list)
        # if len(personnel_list) > 0:
        #     worksheet.write_merge(start_row, start_row + len(personnel_list)-1, 0, 0, order_number, style_merge)  # 合并序号单元格
        #     worksheet.write_merge(start_row, start_row + len(personnel_list)-1, 1, 1, company_name, style_merge)  # 合并公司名称单元格
        # else:
        #     worksheet.write(start_row, 0, order_number, style)
        #     worksheet.write(start_row, 1, company_name, style)
        #     worksheet.write(start_row, 2, '--', style)
        #     worksheet.write(start_row, 3, '--', style)
        #     start_row += 1
        #
        # for personnel in personnel_list:
        #     # 姓名
        #     name = re.findall('<div class="employee-name">(\s*.*?\s*)</div>', personnel)
        #     if len(name) > 0:
        #         name = name[0].strip()
        #     else:
        #         name = '--'
        #     print('姓名：' + name)
        #     worksheet.write(start_row, 2, name, style)  # 将信息输入表格
        #     # 职务
        #     job = re.findall('<div class="employee-job">(\s*.*?\s*)</div>', personnel)
        #     if len(job) > 0:
        #         job = job[0].strip()
        #     else:
        #         job = '--'
        #     print('职务：' + job)
        #     worksheet.write(start_row, 3, job, style)  # 将信息输入表格
        #     start_row += 1
        # print('----------------------------------------------------------------------')
    return worksheet


if __name__ == '__main__':
    for i in range(1, 4):
        print(i)