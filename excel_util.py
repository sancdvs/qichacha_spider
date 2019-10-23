import xlwt
import xlrd
import os
from xlutils.copy import copy

# 创建一个样式对象，初始化样式
style_title = xlwt.XFStyle()  # 标题样式
style_merge = xlwt.XFStyle()  # 合并单元格样式
style = xlwt.XFStyle()  # 普通单元格样式

# 设置字体，包括字体、字号和颜色样式特性
font_title = xlwt.Font()
font_title.bold = True  # 是否粗体
font_title.name = u'微软雅黑'
font_title.color = 'black'
font_title.height = 200  # 字体大小，220就是11号字体，大概就是11*20得来的吧
# font_title.colour_index = 2  # 红色

# 给单元格加框线
border = xlwt.Borders()
border.left = xlwt.Borders.THIN  # 左
border.top = xlwt.Borders.THIN  # 上
border.right = xlwt.Borders.THIN  # 右
border.bottom = xlwt.Borders.THIN  # 下
border.left_colour = 0x40  # 设置框线颜色，0x40是黑色
border.right_colour = 0x40
border.top_colour = 0x40
border.bottom_colour = 0x40

# 设置单元格对齐方式
alignment_merge = xlwt.Alignment()
alignment_merge.horz = xlwt.Alignment.HORZ_LEFT  # 设置水平左对齐
alignment_merge.vert = xlwt.Alignment.VERT_CENTER  # 设置垂直居中

# 设置背景颜色
pattern_title = xlwt.Pattern()
pattern_title.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_title.pattern_fore_colour = xlwt.Style.colour_map['yellow']  # 设置单元格背景色为黄色

style_title.font = font_title
style_title.pattern = pattern_title
style_title.borders = border
style_merge.alignment = alignment_merge
style_merge.alignment.wrap = 1
style.alignment = alignment_merge
style.alignment.wrap = 1    # 自动换行


# 设置栏位自适应宽度
def set_auto_width(worksheet):
    col_width = get_col_width(worksheet)
    # 设置栏位宽度，栏位宽度小于10时候采用默认宽度
    for i in range(len(col_width)):
        if col_width[i] > 10:
            worksheet.col(i).width = 256 * (col_width[i] + 1)


# 确定栏位宽度
def get_col_width(worksheet):
    col_width = []
    # 获取每一列的内容的最大宽度
    i = 0
    # 每列
    print("cols===========" + str(worksheet.get_cols()))
    for col in worksheet.get_cols():
        # 每行
        print(col)
        for j in range(len(col)):
            if j == 0:
                # 数组增加一个元素
                col_width.append(len_byte(str(col[j].value)))
            else:
                # 获得每列中的内容的最大宽度
                if col_width[i] < len_byte(str(col[j].value)):
                    col_width[i] = len_byte(str(col[j].value))
        i = i + 1
    return col_width


# 获取字符串长度，一个中文的长度为2
def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)

# 读取excel行数
def read_excel_rows(filePath,sheetindex):
    # 打开文件
    x1 = xlrd.open_workbook(filePath)
    # 获取sheet的汇总数据
    sheet = x1.sheet_by_index(sheetindex)
    # print("sheet name:{}".format(sheet.name))  # get sheet name
    # print("row num:{}".format(sheet.nrows))  # get sheet all rows number
    # print("col num:{}".format(sheet.ncols))  # get sheet all columns number
    return sheet.nrows


# 判断文件是否存在
def check_file(filePath):
    # print(os.path.exists(filePath)) # 文件是否存在
    # print(os.path.isfile(filePath)) # 是否是文件
    # print(os.access(filePath, os.W_OK)) # 检查文件是否可以写入
    return os.path.exists(filePath) and os.access(filePath, os.W_OK)


# 获取工作簿中所有的合并单元格
def get_merged_cells(sheet):
    """
    获取所有的合并单元格，格式如下：
    [(4, 5, 2, 4), (5, 6, 2, 4), (1, 4, 3, 4)]
    (4, 5, 2, 4) 的含义为：行 从下标4开始，到下标5（不包含）  列 从下标2开始，到下标4（不包含），为合并单元格
    :param sheet:
    :return:
    """
    return sheet.merged_cells


# 获取合并单元格的值
def get_merged_cells_value(filePath, sheetindex, row_index, col_index):
    """
    先判断给定的单元格，是否属于合并单元格；
    如果是合并单元格，就返回合并单元格的内容
    :return:
    """
    is_merged_cell = False
    cell_value = None
    # 打开文件
    # 读取文件的时候需要将formatting_info参数设置为True，默认是False，不然上面获取合并的单元格数组为空
    x1 = xlrd.open_workbook(filePath,formatting_info=True)
    # 获取sheet的汇总数据
    sheet = x1.sheet_by_index(sheetindex)
    merged = get_merged_cells(sheet)
    for (rlow, rhigh, clow, chigh) in merged:
        if (row_index >= rlow and row_index < rhigh):
            if (col_index >= clow and col_index < chigh):
                cell_value = sheet.cell_value(rlow, clow)
                is_merged_cell = True
                # print('该单元格[%d,%d]属于合并单元格，值为[%s]' % (row_index, col_index, cell_value))
                break
    if not is_merged_cell:
        cell_value = sheet.cell_value(row_index, col_index)
    return cell_value


if __name__ == '__main__':
    filename = '企业抓取信息.xls'
    filePath = os.path.join(os.getcwd(), filename)
    print(filePath)
    # print(check_file(filePath))
    # print(read_excel_rows(filePath))
    # xlutils:修改excel
    # book1 = xlrd.open_workbook(filePath,formatting_info=True)
    # book2 = copy(book1)  # 拷贝一份原来的excel
    # # print(dir(book2))
    # sheet = book2.get_sheet(0)  # 获取第几个sheet页，book2现在的是xlutils里的方法，不是xlrd的
    # sheet.write(763, 0, 763,style)
    # sheet.write(763, 1, 'ss',style)
    # sheet.get
    # book2.save(filePath)
    # 打开文件
    x1 = xlrd.open_workbook(filePath,formatting_info=True)
    # 获取sheet的汇总数据
    sheet = x1.sheet_by_index(2)
    print(sheet.name)
    print(sheet.merged_cells)
