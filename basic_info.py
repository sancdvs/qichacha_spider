import re
from excel_util import *


# 导出企业基本信息
def export_basic_inf(data_list, workbook):
    worksheet = workbook.add_sheet("基本信息", cell_overwrite_ok=True)
    worksheet.write(0, 0, "序号", style_title)
    worksheet.write(0, 1, "公司名称", style_title)
    worksheet.write(0, 2, "法人", style_title)
    worksheet.write(0, 3, "电话", style_title)
    worksheet.write(0, 4, "地址", style_title)
    worksheet.write(0, 5, "邮箱", style_title)
    worksheet.write(0, 6, "注册号", style_title)
    worksheet.write(0, 7, "统一社会信用代码", style_title)
    worksheet.write(0, 8, "注册资本", style_title)
    worksheet.write(0, 9, "成立日期", style_title)
    worksheet.write(0, 10, "企业类型", style_title)
    worksheet.write(0, 11, "经营范围", style_title)
    worksheet.write(0, 12, "公司住所", style_title)
    worksheet.write(0, 13, "营业期限", style_title)
    worksheet.write(0, 14, "企业状态", style_title)
    # 设置表格列宽
    for i in range(15):
        if i == 0:
            continue
        elif i == 11:
            worksheet.col(i).width = 256 * 50  # 设置第二列宽度，256为衡量单位，50表示50个字符宽度
        else:
            worksheet.col(i).width = 256 * 20
    i = 0
    for _response in data_list:
        i += 1
        worksheet.write(i, 0, i, style)
        # 公司名称
        company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)
        if len(company_name) > 0:
            company_name = company_name[0].strip()
        else:
            company_name = '--'
        print('公司名称：' + company_name)
        worksheet.write(i, 1, company_name, style)  # 将信息输入表格
        # 法人
        legal_person = re.findall('<a class="oper" href=".*?">(.*?\s*)</a>', _response)
        if len(legal_person) > 0:
            legal_person = legal_person[0].strip()
        else:
            legal_person = '--'
        print('法人：' + legal_person)
        worksheet.write(i, 2, legal_person, style)  # 将信息输入表格
        # 电话
        telephone = re.findall('<a href="tel:.*?" class="phone a-decoration">(.*?\s*)</a>', _response)
        if len(telephone) > 0:
            telephone = telephone[0].strip()
        else:
            telephone = '--'
        print('电话：' + telephone)
        worksheet.write(i, 3, telephone, style)  # 将信息输入表格
        # 地址
        address = re.findall('</div> <div class="address">(\s*.*?\s*)</div> </div>', _response)
        if len(address) > 0:
            address = address[0].strip()
        else:
            address = '--'
        print('地址：' + address)
        worksheet.write(i, 4, address, style)  # 将信息输入表格
        # 邮箱
        email = re.findall('<a href="javascript:;" class="email a-decoration">(.*?\s*)</a>', _response)
        if len(email) > 0:
            email = email[0].strip()
        else:
            email = '--'
        print('邮箱：' + email)
        worksheet.write(i, 5, email, style)  # 将信息输入表格
        basic_list = re.findall('</div> <div class="basic-item-right">(\s*.*?\s*)</div>', _response)
        if len(basic_list) > 0:
            # 注册号
            registration_number = basic_list[0].strip()
        else:
            registration_number = '--'
        print('注册号：' + registration_number)
        worksheet.write(i, 6, registration_number, style)  # 将信息输入表格
        if len(basic_list) > 1:
            # 统一社会信用代码
            credit_ode = basic_list[1].strip()
        else:
            credit_ode = '--'
        print('统一社会信用代码：' + credit_ode)
        worksheet.write(i, 7, credit_ode, style)  # 将信息输入表格
        if len(basic_list) > 2:
            # 注册资本
            registration_capital = basic_list[2].strip()
        else:
            registration_capital = '--'
        print('注册资本：' + registration_capital)
        worksheet.write(i, 8, registration_capital, style)  # 将信息输入表格
        if len(basic_list) > 3:
            # 成立日期
            registration_date = basic_list[3].strip()
        else:
            registration_date = '--'
        print('成立日期：' + registration_date)
        worksheet.write(i, 9, registration_date, style)  # 将信息输入表格
        if len(basic_list) > 4:
            # 企业类型
            company_type = basic_list[4].strip()
        else:
            company_type = '--'
        print('企业类型：' + company_type)
        worksheet.write(i, 10, company_type, style)  # 将信息输入表格
        if len(basic_list) > 5:
            # 经营范围
            business_scope = basic_list[5].strip()
        else:
            business_scope = '--'
        print('经营范围：' + business_scope)
        worksheet.write(i, 11, business_scope, style)  # 将信息输入表格
        if len(basic_list) > 6:
            # 公司住所
            company_address = basic_list[6].strip()
        else:
            company_address = '--'
        print('公司住所：' + company_address)
        worksheet.write(i, 12, company_address, style)  # 将信息输入表格
        if len(basic_list) > 7:
            # 营业期限
            business_term = basic_list[7].strip()
        else:
            business_term = '--'
        print('营业期限：' + business_term)
        worksheet.write(i, 13, business_term, style)  # 将信息输入表格
        if len(basic_list) > 8:
            # 企业状态
            enterprise_state = basic_list[8].strip()
        else:
            enterprise_state = '--'
        print('企业状态：' + enterprise_state)
        worksheet.write(i, 14, enterprise_state, style)  # 将信息输入表格
        print('----------------------------------------------------------------------')
    return worksheet
