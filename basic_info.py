import re

from config import spider_result_file_name, basic_inf_sheet_name
from excel_util import *
from log import logging

# 导出企业基本信息
def export_basic_inf(data_list, workbook, is_exsit):
    start_row = 1   # 数据起始excel行号
    if not is_exsit:
        worksheet = workbook.add_sheet(basic_inf_sheet_name, cell_overwrite_ok=True)
        worksheet.write(0, 0, "序号", style_title)
        worksheet.write(0, 1, "公司名称", style_title)
        worksheet.write(0, 2, "法定代表人", style_title)
        worksheet.write(0, 3, "注册资本", style_title)
        worksheet.write(0, 4, "实缴资本", style_title)
        worksheet.write(0, 5, "经营状态", style_title)
        worksheet.write(0, 6, "成立日期", style_title)
        worksheet.write(0, 7, "统一社会信用代码", style_title)
        worksheet.write(0, 8, "纳税人识别号", style_title)
        worksheet.write(0, 9, "注册号", style_title)
        worksheet.write(0, 10, "组织机构代码", style_title)
        worksheet.write(0, 11, "企业类型", style_title)
        worksheet.write(0, 12, "所属行业", style_title)
        worksheet.write(0, 13, "人员规模", style_title)
        worksheet.write(0, 14, "营业期限", style_title)
        worksheet.write(0, 15, "企业地址", style_title)
        worksheet.write(0, 16, "经营范围", style_title)

        # worksheet.write(0, 3, "电话", style_title)
        # worksheet.write(0, 4, "地址", style_title)
        # worksheet.write(0, 5, "邮箱", style_title)
        # worksheet.write(0, 6, "注册号", style_title)
        # worksheet.write(0, 7, "统一社会信用代码", style_title)
        # worksheet.write(0, 8, "注册资本", style_title)
        # worksheet.write(0, 9, "成立日期", style_title)
        # worksheet.write(0, 10, "企业类型", style_title)
        # worksheet.write(0, 11, "经营范围", style_title)
        # worksheet.write(0, 12, "公司住所", style_title)
        # worksheet.write(0, 13, "营业期限", style_title)
        # worksheet.write(0, 14, "企业状态", style_title)
        # 设置表格列宽
        for i in range(17):
            if i == 0:
                continue
            elif i == 16:
                worksheet.col(i).width = 256 * 200  # 设置第二列宽度，256为衡量单位，50表示50个字符宽度
            else:
                worksheet.col(i).width = 256 * 20
    else:
        start_row = read_excel_rows(spider_result_file_name,basic_inf_sheet_name)
        worksheet = workbook.get_sheet(basic_inf_sheet_name)

    # 定义excel表头列表
    basic_info_title = ['序号', '公司名称', '法定代表人/法人/负责人/经营者/投资人/执行事务合伙人', '注册资本/开办资金', '实缴资本', '经营状态/登记状态', '成立日期', '统一社会信用代码',
                        '纳税人识别号','注册号','组织机构代码','企业类型/社会组织类型','所属行业','人员规模','营业期限/证书有效期/有效期','企业地址/住所/地址','经营范围/业务范围']

    for _response in data_list:
        worksheet.write(start_row, 0, start_row, style)
        # 公司名称
        company_name = _response.find(class_="content")
        if company_name is not None:
            company_name = company_name.select('h1')[0].text.replace('\n', '').replace(' ', '') if len(company_name.select('h1')) > 0 else '无'
        print('公司名称：' + company_name)
        worksheet.write(start_row, 1, company_name, style)  # 将信息输入表格

        basic_informatiion_array =_response.select("#Cominfo > table > tbody > tr")     # 符号">"为上一个标签下的直接子标签

        if len(basic_informatiion_array) == 0:
            logging.error('未找到该公司基本信息============{}'.format(company_name))

        for basic_tr in basic_informatiion_array:   # 循环tr
            basic_td_array = [data for data in basic_tr.children if data != ' ']
            i = 0
            while i < len(basic_td_array):         # 循环td
                key = basic_td_array[i].text.replace('\n', '').replace(' ', '')
                if len(basic_td_array[i+1].select('h2')) > 0:
                    value = basic_td_array[i+1].select('h2')[0].text.replace('\n', '').replace(' ', '')
                else:
                    value = basic_td_array[i+1].text.replace('\n', '').replace(' ', '').replace('查看地图', '').replace('附近企业', '')
                # 查出表格的标题在自定义的basic_info_title中的索引位置，为写入excel的列索引。
                index = [k for k, x in enumerate(basic_info_title) if key in x]
                if len(index) > 0:
                    print(key+'：'+value)
                    worksheet.write(start_row, index[0], value, style)  # 将信息输入表格
                i += 2
        start_row += 1

        # if len(basic_informatiion_array) > 0:
        #     # 法人
        #     legal_person = '-'
        #     if len(basic_informatiion_array[0].select('td')) > 1:
        #         # legal_person_item = basic_informatiion_array[0].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         # if len(basic_informatiion_array[0].select('td')[1].select('h2')) > 0 and ('法定代表人' in legal_person_item or '经营者' in legal_person_item):
        #         if len(basic_informatiion_array[0].select('td')[1].select('h2')) > 0:
        #             legal_person = basic_informatiion_array[0].select('td')[1].select('h2')[0].text.replace('\n', '').replace(' ', '')
        #     print('法人：' + legal_person)
        #     worksheet.write(start_row, 2, legal_person, style)  # 将信息输入表格
        #     # 注册资本
        #     registration_capital = '-'
        #     if len(basic_informatiion_array[0].select('td')) > 3:
        #         registration_capital_item = basic_informatiion_array[0].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '注册资本' in registration_capital_item:
        #             registration_capital = basic_informatiion_array[0].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('注册资本：' + registration_capital)
        #     worksheet.write(start_row, 3, registration_capital, style)  # 将信息输入表格
        #     # 实缴资本
        #     real_capital = '-'
        #     if len(basic_informatiion_array) > 1 and len(basic_informatiion_array[1].select('td')) > 1:
        #         real_capital_item = basic_informatiion_array[1].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '实缴资本' in real_capital_item:
        #             real_capital = basic_informatiion_array[1].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('实缴资本：' + real_capital)
        #     worksheet.write(start_row, 4, real_capital, style)  # 将信息输入表格
        #     # 经营状态
        #     operating_status = '-'
        #     if len(basic_informatiion_array) > 2 and len(basic_informatiion_array[2].select('td')) > 1:
        #         operating_status_item = basic_informatiion_array[2].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '经营状态' in operating_status_item:
        #             operating_status = basic_informatiion_array[2].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('经营状态：' + operating_status)
        #     worksheet.write(start_row, 5, operating_status, style)  # 将信息输入表格
        #     # 成立日期
        #     establishment_date = '-'
        #     if len(basic_informatiion_array) > 2 and len(basic_informatiion_array[2].select('td')) > 3:
        #         establishment_date_item = basic_informatiion_array[2].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '成立日期' in establishment_date_item:
        #             establishment_date = basic_informatiion_array[2].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('成立日期：' + establishment_date)
        #     worksheet.write(start_row, 6, establishment_date, style)  # 将信息输入表格
        #     # 统一社会信用代码
        #     unified_credit_code = '-'
        #     if len(basic_informatiion_array) > 3 and len(basic_informatiion_array[3].select('td')) > 1:
        #         unified_credit_code_item = basic_informatiion_array[3].select('td')[0].text.replace('\n', '').replace(' ','')
        #         if '统一社会信用代码' in unified_credit_code_item:
        #             unified_credit_code = basic_informatiion_array[3].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('统一社会信用代码：' + unified_credit_code)
        #     worksheet.write(start_row, 7, unified_credit_code, style)  # 将信息输入表格
        #     # 纳税人识别号
        #     taxpayer_identification = '-'
        #     if len(basic_informatiion_array) > 3 and len(basic_informatiion_array[3].select('td')) > 3:
        #         taxpayer_identification_item = basic_informatiion_array[3].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '纳税人识别号' in taxpayer_identification_item:
        #             taxpayer_identification = basic_informatiion_array[3].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('纳税人识别号：' + taxpayer_identification)
        #     worksheet.write(start_row, 8, taxpayer_identification, style)  # 将信息输入表格
        #     # 注册号
        #     registration_number = '-'
        #     if len(basic_informatiion_array) > 4 and len(basic_informatiion_array[4].select('td')) > 1:
        #         registration_number_item = basic_informatiion_array[4].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '注册号' in registration_number_item:
        #             registration_number = basic_informatiion_array[4].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('注册号：' + registration_number)
        #     worksheet.write(start_row, 9, registration_number, style)  # 将信息输入表格
        #     # 组织机构代码
        #     organization_code = '-'
        #     if len(basic_informatiion_array) > 4 and len(basic_informatiion_array[4].select('td')) > 3:
        #         organization_code_item = basic_informatiion_array[4].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '组织机构代码' in organization_code_item:
        #             organization_code = basic_informatiion_array[4].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('组织机构代码：' + organization_code)
        #     worksheet.write(start_row, 10, organization_code, style)  # 将信息输入表格
        #     # 企业类型
        #     company_type = '-'
        #     if len(basic_informatiion_array) > 5 and len(basic_informatiion_array[5].select('td')) > 1:
        #         company_type_item = basic_informatiion_array[5].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '企业类型' in company_type_item:
        #             company_type = basic_informatiion_array[5].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('企业类型：' + company_type)
        #     worksheet.write(start_row, 11, company_type, style)  # 将信息输入表格
        #     # 所属行业
        #     industry = '-'
        #     if len(basic_informatiion_array) > 5 and len(basic_informatiion_array[5].select('td')) > 3:
        #         industry_item = basic_informatiion_array[5].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '所属行业' in industry_item:
        #             industry = basic_informatiion_array[5].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('所属行业：' + industry)
        #     worksheet.write(start_row, 12, industry, style)  # 将信息输入表格
        #     # 人员规模
        #     employees = '-'
        #     if len(basic_informatiion_array) > 9 and len(basic_informatiion_array[9].select('td')) > 1:
        #         employees_item = basic_informatiion_array[9].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '人员规模' in employees_item:
        #             employees = basic_informatiion_array[9].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('人员规模：' + employees)
        #     worksheet.write(start_row, 13, employees, style)  # 将信息输入表格
        #     # 营业期限
        #     business_term = '-'
        #     if len(basic_informatiion_array) > 9 and len(basic_informatiion_array[9].select('td')) > 3:
        #         business_term_item = basic_informatiion_array[9].select('td')[2].text.replace('\n', '').replace(' ', '')
        #         if '营业期限' in business_term_item:
        #             business_term = basic_informatiion_array[9].select('td')[3].text.replace('\n', '').replace(' ', '')
        #     print('营业期限：' + business_term)
        #     worksheet.write(start_row, 14, business_term, style)  # 将信息输入表格
        #     # 企业地址
        #     adress = '-'
        #     if len(basic_informatiion_array) > 10 and len(basic_informatiion_array[10].select('td')) > 1:
        #         adress_item = basic_informatiion_array[10].select('td')[0].text.replace('\n','').replace(' ', '')
        #         if '企业地址' in adress_item:
        #             adress = basic_informatiion_array[10].select('td')[1].text.replace('查看地图', '').replace('附近企业', '').replace('\n', '').replace(' ', '')
        #     print('企业地址：' + adress)
        #     worksheet.write(start_row, 15, adress, style)  # 将信息输入表格
        #     # 经营范围
        #     business_scope = '-'
        #     if len(basic_informatiion_array) > 11 and len(basic_informatiion_array[11].select('td')) > 1:
        #         business_scope_item = basic_informatiion_array[11].select('td')[0].text.replace('\n', '').replace(' ', '')
        #         if '经营范围' in business_scope_item:
        #             business_scope = basic_informatiion_array[11].select('td')[1].text.replace('\n', '').replace(' ', '')
        #     print('经营范围：' + business_scope)
        #     worksheet.write(start_row, 16, business_scope, style)  # 将信息输入表格
        # start_row += 1

        # 公司名称
        # # company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)
        # if len(company_name) > 0:
        #     company_name = company_name.strip()
        # else:
        #     company_name = '--'
        # print('公司名称：' + company_name)
        # worksheet.write(start_row, 1, company_name, style)  # 将信息输入表格
        # 法人
        # legal_person = re.findall('<a class="oper" href=".*?">(.*?\s*)</a>', _response)
        # if len(legal_person) > 0:
        #     legal_person = legal_person.strip()
        # else:
        #     legal_person = '--'
        # print('法人：' + legal_person)
        # worksheet.write(start_row, 2, legal_person, style)  # 将信息输入表格
        # 电话
        # telephone = re.findall('<a href="tel:.*?" class="phone a-decoration">(.*?\s*)</a>', _response)
        # if len(telephone) > 0:
        #     telephone = telephone[0].strip()
        # else:
        #     telephone = '--'
        # print('电话：' + telephone)
        # worksheet.write(start_row, 3, telephone, style)  # 将信息输入表格
        # 地址
        # address = re.findall('</div> <div class="address">(\s*.*?\s*)</div> </div>', _response)
        # if len(address) > 0:
        #     address = address[0].strip()
        # else:
        #     address = '--'
        # print('地址：' + address)
        # worksheet.write(start_row, 4, address, style)  # 将信息输入表格
        # 邮箱
        # email = re.findall('<a href="javascript:;" class="email a-decoration">(.*?\s*)</a>', _response)
        # if len(email) > 0:
        #     email = email[0].strip()
        # else:
        #     email = '--'
        # print('邮箱：' + email)
        # worksheet.write(start_row, 5, email, style)  # 将信息输入表格
        # basic_list = re.findall('</div> <div class="basic-item-right">(\s*.*?\s*)</div>', _response)
        # if len(basic_list) > 0:
        #     # 注册号
        #     registration_number = basic_list[0].strip()
        # else:
        #     registration_number = '--'
        # print('注册号：' + registration_number)
        # worksheet.write(start_row, 6, registration_number, style)  # 将信息输入表格
        # if len(basic_list) > 1:
        #     # 统一社会信用代码
        #     credit_ode = basic_list[1].strip()
        # else:
        #     credit_ode = '--'
        # print('统一社会信用代码：' + credit_ode)
        # worksheet.write(start_row, 7, credit_ode, style)  # 将信息输入表格
        # 注册资本
        # if len(basic_list) > 2:
        #     registration_capital = basic_list[2].strip()
        # else:
        #     registration_capital = '--'
        # print('注册资本：' + registration_capital)
        # worksheet.write(start_row, 8, registration_capital, style)  # 将信息输入表格
        # if len(basic_list) > 3:
        #     # 成立日期
        #     registration_date = basic_list[3].strip()
        # else:
        #     registration_date = '--'
        # print('成立日期：' + registration_date)
        # worksheet.write(start_row, 9, registration_date, style)  # 将信息输入表格
        # if len(basic_list) > 4:
        #     # 企业类型
        #     company_type = basic_list[4].strip()
        # else:
        #     company_type = '--'
        # print('企业类型：' + company_type)
        # worksheet.write(start_row, 10, company_type, style)  # 将信息输入表格
        # if len(basic_list) > 5:
        #     # 经营范围
        #     business_scope = basic_list[5].strip()
        # else:
        #     business_scope = '--'
        # print('经营范围：' + business_scope)
        # worksheet.write(start_row, 11, business_scope, style)  # 将信息输入表格
        # if len(basic_list) > 6:
        #     # 公司住所
        #     company_address = basic_list[6].strip()
        # else:
        #     company_address = '--'
        # print('公司住所：' + company_address)
        # worksheet.write(start_row, 12, company_address, style)  # 将信息输入表格
        # if len(basic_list) > 7:
        #     # 营业期限
        #     business_term = basic_list[7].strip()
        # else:
        #     business_term = '--'
        # print('营业期限：' + business_term)
        # worksheet.write(start_row, 13, business_term, style)  # 将信息输入表格
        # if len(basic_list) > 8:
        #     # 企业状态
        #     enterprise_state = basic_list[8].strip()
        # else:
        #     enterprise_state = '--'
        # print('企业状态：' + enterprise_state)
        # worksheet.write(start_row, 14, enterprise_state, style)  # 将信息输入表格
        # start_row += 1
        # print('----------------------------------------------------------------------')
    return worksheet


if __name__ == '__main__':
    basic_info_title = ['序号', '公司名称', '法定代表人/法人/负责人/经营者/投资人', '注册资本/开办资金', '实缴资本', '经营状态/登记状态', '成立日期', '统一社会信用代码',
                        '纳税人识别号', '注册号', '组织机构代码', '企业类型/社会组织类型', '所属行业', '人员规模', '营业期限/证书有效期/有效期', '企业地址/住所/地址',
                        '经营范围/业务范围']
    key = '法人/负责人'
    index = [k for k, x in enumerate(basic_info_title) if key in x]
    print(index)
