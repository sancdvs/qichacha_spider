import xlwt
# import xlrd

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

