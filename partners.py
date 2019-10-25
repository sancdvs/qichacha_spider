import re

from config import spider_result_file_name
from excel_util import style_title, style_merge, style, read_excel_rows, get_merged_cells_value


# 导出企业股东信息
def export_partners(data_list,workbook, is_new):
    start_row = 1   # 数据起始excel行号
    order_number = 0    # 数据起始序号
    if is_new:
        worksheet = workbook.add_sheet("股东信息",cell_overwrite_ok=True)
        worksheet.write(0, 0, u"序号", style_title)
        worksheet.write(0, 1, u"公司名称", style_title)
        worksheet.write(0, 2, u"股东名称", style_title)
        worksheet.write(0, 3, u"持股比例", style_title)
        worksheet.write(0, 4, u"最终受益股份", style_title)
        worksheet.write(0, 5, u"认缴出资额(万元)", style_title)
        worksheet.write(0, 6, u"认缴出资日期", style_title)
        worksheet.write(0, 7, u"实缴出资额(万元)", style_title)
        worksheet.write(0, 8, u"实缴出资日期", style_title)

        # Setting row height and column width 设置宽和高 xlwt中是行和列都是从0开始计算的
        worksheet.col(1).width = 256 * 50
        worksheet.col(2).width = 256 * 20
        worksheet.col(3).width = 256 * 20
        worksheet.col(4).width = 256 * 30
        worksheet.col(5).width = 256 * 30
        worksheet.col(6).width = 256 * 30
        worksheet.col(7).width = 256 * 30
        worksheet.col(8).width = 256 * 30
    else:
        start_row = read_excel_rows(spider_result_file_name, 1)
        worksheet = workbook.get_sheet(1)
        order_number = int(get_merged_cells_value(spider_result_file_name, 1, start_row-1, 0))  # 序号位置是第一列

    for _response in data_list:
        order_number += 1
        # 公司名称
        company_name = _response.find(class_="row title jk-tip").select('h1')[0].text.replace('\n', '').replace(' ', '')
        print('公司名称：' + company_name)
        partner_array = _response.select("#partnerslist > table > tr")
        if len(partner_array)-1 > 0:
            worksheet.write_merge(start_row, start_row + len(partner_array)-2, 0, 0, order_number, style_merge)   # 序号
            worksheet.write_merge(start_row, start_row + len(partner_array)-2, 1, 1, company_name, style_merge)  # 合并公司名称单元格
        else:
            worksheet.write(start_row, 0, order_number, style)
            worksheet.write(start_row, 1, company_name, style)
            worksheet.write(start_row, 2, '--', style)
            worksheet.write(start_row, 3, '--', style)
            worksheet.write(start_row, 4, '--', style)
            worksheet.write(start_row, 5, '--', style)
            worksheet.write(start_row, 6, '--', style)
            worksheet.write(start_row, 7, '--', style)
            worksheet.write(start_row, 8, '--', style)
            start_row += 1
    #
        for i in range(1, len(partner_array)):
            partner = partner_array[0].select('th')
            #股东及出资信息
            partner_name = partner_array[i].select('td')[1].select('h3')[0].text.replace('\n', '').replace(' ', '')
            worksheet.write(start_row, 2, partner_name, style)  # 将信息输入表格
            print('股东名称：' + partner_name)
            #持股比例
            stock_rate= partner_array[i].select('td')[4].text.replace('\n', '').replace(' ', '')
            if '%' in stock_rate:
                stock_rate = stock_rate.split('%')[0]+'%'
            worksheet.write(start_row, 3, stock_rate, style)  # 将信息输入表格
            print('持股比例：' + stock_rate)
            #最终受益股份
            if partner[3].text == '最终受益股份':
              final_rate = partner_array[i].select('td')[5].text.replace('\n', '').replace(' ', '')
              if '%' in final_rate:
                  final_rate= final_rate.split('%')[0]+'%'
            else:
                final_rate = '--'
            worksheet.write(start_row, 4, final_rate, style)  # 将信息输入表格
            print('最终受益股份：' + final_rate)

            # 认缴出资额(万元)
            if len(partner) == 5:
                money = partner_array[i].select('td')[5].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            elif len(partner) == 7:
                money = partner_array[i].select('td')[5].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            elif len(partner) == 8:
                money = partner_array[i].select('td')[6].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            else:
                money = '--'
            worksheet.write(start_row, 5, money, style)  # 将信息输入表格
            print('认缴出资额：' + money)

            #认缴出资日期
            if len(partner) == 5:
                time = partner_array[i].select('td')[6].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            elif len(partner) == 7:
                time = partner_array[i].select('td')[6].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            elif len(partner) == 8:
                time = partner_array[i].select('td')[7].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            else:
                time = '--'
            worksheet.write(start_row, 6, time, style)  # 将信息输入表格
            print('认缴出资日期：' + time)

            #实缴出资额(万元)
            if len(partner) == 7:
                real_money = partner_array[i].select('td')[7].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            elif len(partner) == 8:
                real_money = partner_array[i].select('td')[8].text.replace('\n', '').replace(' ', '').replace('<br>', '')
            else:
                real_money = '--'
            worksheet.write(start_row, 7, real_money, style)  # 将信息输入表格
            print('实缴出资额：' + real_money)

            #实缴出资日期
            if len(partner) == 7:
                real_time = partner_array[i].select('td')[8].text.replace('\n', '').replace(' ', '').replace('<br>',
                                                                                                              '')
            elif len(partner) == 8:
                real_time = partner_array[i].select('td')[9].text.replace('\n', '').replace(' ', '').replace('<br>',
                                                                                                              '')
            else:
                real_time = '--'
            worksheet.write(start_row, 8, real_time, style)  # 将信息输入表格
            print('实缴出日期：' + real_time)
            start_row += 1

            # 公司名称
            # company_name = re.findall('<div class="company-name">(.*?\s*)<', _response)
            # if len(company_name) > 0:
            #     company_name = company_name[0].strip()
            # else:
            #     company_name = '--'
            # print('公司名称：' + company_name)
            # print(_response)
            # list = re.findall('<div class="stock-item">(.*?\s*\n*.*?\s*\n*.*?\s*\n*)</div>\n?\s*</div>\n?\s*</div>\n?\s*</div>', _response)
            # for partner in list:
            # print(partner)
            # partner_list = re.findall('<div class="stock-text">(.*?\s*)<', partner)
            # #股东名称
            # partner_name = re.findall(' <div class="stock-title"> <span > <a class="text-blue a-decoration"( href=".*?")? >(.*?\s*)</a>', partner)
            # if len(partner_name) > 0:
            #     partner_name = partner_name[0][1].strip()
            # else:
            #     partner_name = '--'
            # print('股东名称：' + partner_name)
            # worksheet.write(start_row, 2, partner_name,style)  # 将信息输入表格
            # if len(partner_list) > 0:
            #     #持股比例
            #     stock_rate = partner_list[0].strip()
            # else:
            #     stock_rate = '--'
            # print('持股比例：' + stock_rate)
            # worksheet.write(start_row, 3, stock_rate,style)  # 将信息输入表格
            # if len(partner_list) > 1:
            #     #股东类型
            #     stock_type = partner_list[1].strip()
            # else:
            #     stock_type = '--'
            # print('股东类型：' + stock_type)
            # worksheet.write(start_row, 4, stock_type,style)  # 将信息输入表格
            # if len(partner_list) > 2:
            #     #认缴出资额(万元)
            #     money = partner_list[2].strip()
            # else:
            #     money = '--'
            # print('认缴出资额(万元)：' + money)
            # worksheet.write(start_row, 5, money,style)  # 将信息输入表格
            # if len(partner_list) > 3:
            #     #认缴出资日期
            #     time = partner_list[3].strip()
            # else:
            #     time = '--'
            # print('认缴出资日期：' + time)
            # worksheet.write(start_row, 6, time,style)  # 将信息输入表格
            # start_row += 1
        print('----------------------------------------------------------------------')
    return worksheet


if __name__ == '__main__':
   _response =  '''
        股东信息
                    <span class="block-num">3</span> <img onclick="collapse(this)" src="/material/theme/mobile/img/wxa-service/arrow_down.png" alt=""> </div> 
                    <div> <div class="stock-wrap"> <div class="stock-item"> <div class="stock-title"> <span > <a class="text-blue a-decoration" >东莞市吉田焊接材料有限公司</a> </span><span class="company-status status-normal">企业法人</span> </div> <div class="stock-content"> <div class="stock-row"> <div class="stock-col-left"> <div class="stock-subtitle">持股比例</div> <div class="stock-text">51.00%</div> </div> <div class="stock-col-right"> <div class="stock-subtitle">股东类型</div> <div class="stock-text">企业法人</div> </div> </div> <div class="stock-row" style="margin-top: 20px;"> <div class="stock-col-left"> <div class="stock-subtitle">认缴出资额(万元)</div> <div class="stock-text">                                                                                -
                    </div> </div> <div class="stock-col-right"> <div class="stock-subtitle">认缴出资日期</div> <div class="stock-text">                                        -
                                        </div> </div> </div> </div> </div> </div> <div class="stock-wrap"> <div class="stock-item"> <div class="stock-title"> <span > <a class="text-blue a-decoration" >深圳市吉田新电子有限公司</a> </span><span class="company-status status-normal">企业法人</span> </div> <div class="stock-content"> <div class="stock-row"> <div class="stock-col-left"> <div class="stock-subtitle">持股比例</div> <div class="stock-text">34.00%</div> </div> <div class="stock-col-right"> <div class="stock-subtitle">股东类型</div> <div class="stock-text">企业法人</div> </div> </div> <div class="stock-row" style="margin-top: 20px;"> <div class="stock-col-left"> <div class="stock-subtitle">认缴出资额(万元)</div> <div class="stock-text">                                                                                680<br/> </div> </div> <div class="stock-col-right"> <div class="stock-subtitle">认缴出资日期</div> <div class="stock-text">                                        -
                                        </div> </div> </div> </div> </div> </div> <div class="stock-wrap"> <div class="stock-item"> <div class="stock-title"> <span > <a class="text-blue a-decoration" >珠海横琴吉田成长投资合伙企业（有限合伙）</a> </span><span class="company-status status-normal">其他投资者</span> </div> <div class="stock-content"> <div class="stock-row"> <div class="stock-col-left"> <div class="stock-subtitle">持股比例</div> <div class="stock-text">15.00%</div> </div> <div class="stock-col-right"> <div class="stock-subtitle">股东类型</div> <div class="stock-text">其他投资者</div> </div> </div> <div class="stock-row" style="margin-top: 20px;"> <div class="stock-col-left"> <div class="stock-subtitle">认缴出资额(万元)</div> <div class="stock-text">                                                                                300<br/> </div> </div> <div class="stock-col-right"> <div class="stock-subtitle">认缴出资日期</div> <div class="stock-text">                                        -
                                        </div> </div> </div> </div> </div> </div> </div> </div>
        '''
   list = re.findall('<div class="stock-item">(.*?\s*\n*.*?\s*\n*.*?\s*\n*)</div>\n?\s*</div>\n?\s*</div>\n?\s*</div>', _response)

   # list = re.findall(
   # '<div class="stock-item"> <div class="stock-title"> <span > <a class="text-blue a-decoration"( href=".*?")? >(\n*\s*.*?\s*\n*)</div>\n*\s*</div>\n*\s*</div>\n*\s*</div>', _response)

   print(list)

   # _response1 =  '''
   # <div id="partners" class="content-block"> <div class="block-title">
   #                  股东信息
   #                  <span class="block-num">1</span> <img onclick="collapse(this)" src="/material/theme/mobile/img/wxa-service/arrow_down.png" alt=""> </div> <div> <div class="stock-wrap"> <div class="stock-item"> <div class="stock-title"> <span > <a class="text-blue a-decoration" href="/pl_p5280f170c45532c4fbcbe4b1c9b4c3f.html" >朱成华</a> </span><span class="company-status status-normal">自然人股东</span> </div> <div class="stock-content"> <div class="stock-row"> <div class="stock-col-left"> <div class="stock-subtitle">持股比例</div> <div class="stock-text">100%</div> </div> <div class="stock-col-right"> <div class="stock-subtitle">股东类型</div> <div class="stock-text">自然人股东</div> </div> </div> <div class="stock-row" style="margin-top: 20px;"> <div class="stock-col-left"> <div class="stock-subtitle">认缴出资额(万元)</div> <div class="stock-text">                                                                                1000<br/> </div> </div> <div class="stock-col-right"> <div class="stock-subtitle">认缴出资日期</div> <div class="stock-text">                                        -
   #                                      </div> </div> </div> </div> </div> </div> </div> </div>
   # '''
   # list1 = re.findall('<div class="stock-item">(.*\s*\n*.*\s*\n*.*\s*\n*)</div>\n?\s*</div>\n?\s*</div>\n?\s*</div>', _response1)
   # print(list1)