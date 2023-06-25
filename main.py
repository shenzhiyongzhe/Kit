# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import xlwt  # 导入模块
from xmindparser import xmind_to_dict
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter import messagebox  # 导入模块


class XlwtSeting(object):
    @staticmethod  # 静态方法装饰器，使用此装饰器装饰后，可以直接使用类名.方法名调用（XlwtSeting.styles()），并且不需要self参数
    def template_one(worksheet):
        dicts = {"horz": "CENTER", "vert": "CENTER"}
        sizes = [10, 10, 20, 20, 45, 60, 60, 60]
        se = XlwtSeting()
        style = se.styles()
        style.alignment = se.alignments(**dicts)
        style.font = se.fonts(bold=True)
        style.borders = se.borders()
        style.pattern = se.patterns(7)
        se.heights(worksheet, 0)
        for i in range(len(sizes)):
            se.widths(worksheet, i, size=sizes[i])
        return style

    @staticmethod
    def template_two():
        dicts2 = {"vert": "CENTER"}
        se = XlwtSeting()
        style = se.styles()
        style.borders = se.borders()
        style.alignment = se.alignments(**dicts2)
        return style

    @staticmethod
    def styles():
        """设置单元格的样式的基础方法"""

        style = xlwt.XFStyle()
        return style

    @staticmethod
    def borders(status=1):
        """设置单元格的边框，
        细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13"""

        border = xlwt.Borders()
        border.left = status
        border.right = status
        border.top = status
        border.bottom = status
        return border

    @staticmethod
    def heights(worksheet, line, size=4):
        """设置单元格的高度"""

        worksheet.row(line).height_mismatch = True
        worksheet.row(line).height = size * 256

    @staticmethod
    def widths(worksheet, line, size=11):
        """设置单元格的宽度"""

        worksheet.col(line).width = size * 256

    @staticmethod
    def alignments(wrap=1, **kwargs):
        """设置单元格的对齐方式，
        ：接收一个对齐参数的字典{"horz": "CENTER", "vert": "CENTER"}horz（水平），vert（垂直）
        ：horz中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,GENERAL,CENTER_ACROSS_SEL（分散）,RIGHT（右边）,LEFT（左边）
        ：vert中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,BOTTOM(下方),TOP（上方）"""

        alignment = xlwt.Alignment()

        if "horz" in kwargs.keys():
            alignment.horz = eval(f"xlwt.Alignment.HORZ_{kwargs['horz'].upper()}")
        if "vert" in kwargs.keys():
            alignment.vert = eval(f"xlwt.Alignment.VERT_{kwargs['vert'].upper()}")
        alignment.wrap = wrap  # 设置自动换行
        return alignment

    @staticmethod
    def fonts(name='宋体', bold=False, underline=False, italic=False, colour='black', height=11):
        """设置单元格中字体的样式，
        默认字体为宋体，不加粗，没有下划线，不是斜体，黑色字体"""

        font = xlwt.Font()
        # 字体
        font.name = name
        # 加粗
        font.bold = bold
        # 下划线
        font.underline = underline
        # 斜体
        font.italic = italic
        # 颜色
        font.colour_index = xlwt.Style.colour_map[colour]
        # 大小
        font.height = 20 * height
        return font

    @staticmethod
    def patterns(colors=1):
        """设置单元格的背景颜色，该数字表示的颜色在xlwt库的其他方法中也适用，默认颜色为白色
        0 = Black, 1 = White,2 = Red, 3 = Green, 4 = Blue,5 = Yellow, 6 = Magenta, 7 = Cyan,
        16 = Maroon, 17 = Dark Green,18 = Dark Blue, 19 = Dark Yellow ,almost brown), 20 = Dark Magenta,
        21 = Teal, 22 = Light Gray,23 = Dark Gray, the list goes on..."""

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = colors
        return pattern


class XmindToXsl(XlwtSeting):
    def __init__(self, name):
        """调用类时，读取xmind文件，并生成excel表格"""
        try:
            self.xm = xmind_to_dict(name)[0]['topic']
        except Exception as e:
            print(f"打开xmind文件失败:{e}")
        self.workbook = xlwt.Workbook(encoding='utf-8')  # 创建workbook对象
        self.worksheet = self.workbook.add_sheet(self.xm["title"], cell_overwrite_ok=True)  # 创建工作表

    def save(self, name):
        """保存表格"""
        self.workbook.save(name + ".xls")

    def write_excel(self):
        row0 = ["用例目录", '用例名称', '需求ID', '前置条件', '用例步骤', '预期结果', '用例类型', '用例状态', '创建人',
                '是否实现自动化',
                '是否上架', '自动化测试类型', '自动化测试平台', '实际结果']  # 写成excel表格用例的要素
        style2 = self.template_one(self.worksheet)
        for i in range(len(row0)):
            self.worksheet.write(0, i, row0[i],style2)
        x = 0  # 写入数据的当前行数
        style = self.template_two()
        # 6 layer
        try:
            if self.xm["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"]:
                for a in self.xm['topics']:  # 第一级 枪械
                    for b in a['topics']:  # 第二级 枪械》瞄准
                        for c in b['topics']:  # 第三级 枪械》瞄准》测试点（键位操作）
                            for d in c['topics']:  # 第四级 键位操作》前置条件
                                for e in d['topics']:  # 第五级  操作步骤
                                    x += 1
                                    # worksheet.write()
                                    self.heights(self.worksheet, x, size=2)
                                    self.worksheet.write(x, 0, a['title'], style)
                                    self.worksheet.write(x, 1, b['title'], style)
                                    # self.worksheet.write(x, 3, c['title'], style)
                                    self.worksheet.write(x, 3, d['title'], style)   # 前置条件
                                    self.worksheet.write(x, 4, e['title'], style)  # 写入操作步骤
                                    self.worksheet.write(x, 5, e["topics"][0]["title"], style)  # 写入预期结果

                print("6", self.xm["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"])
        except KeyError:
            if self.xm["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"][0]:
                for a in self.xm['topics']:  # 第一级 枪械
                    for b in a['topics']:  # 第三级 枪械》瞄准》测试点（键位操作）
                        for c in b['topics']:  # 第四级 键位操作》前置条件
                            for d in c['topics']:  # 第五级  操作步骤
                                x += 1
                                # worksheet.write()
                                self.heights(self.worksheet, x, size=2)
                                self.worksheet.write(x, 1, a['title'], style)
                                self.worksheet.write(x, 2, b['title'], style)
                                self.worksheet.write(x, 3, c['title'], style)
                                self.worksheet.write(x, 4, d['title'], style)  # 写入操作步骤
                                self.worksheet.write(x, 5, d["topics"][0]["title"], style)  # 写入预期结果

                print("5", self.xm["topics"][0]["topics"][0]["topics"][0]["topics"][0]["topics"])
        self.save(self.xm["title"])  # 保存


class MainUI(object):
    def __init__(self, title="Xmind to xlsx", geometrysize="500x400"):
        self.top = tkinter.Tk()  # 生成主窗口
        self.top.title(title)  # 设置窗口的标题
        self.window_width = self.top.winfo_screenwidth()  # 获取屏幕宽高
        self.window_height = self.top.winfo_screenheight()
        # 居中获取宽、高
        self.windowX = (self.window_width - 500) / 2
        self.windowY = (self.window_height - 400) / 2
        if (os.path.exists("test.png")):
            tkinter.Canvas(self.top)
            filename = tkinter.PhotoImage(file="test.png")
            background_label = tkinter.Label(self.top, image=filename)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.top.geometry(geometrysize)  # 设置窗口的大小
        self.top.geometry("+%d+%d" % (self.windowX, self.windowY))  # 设置窗口出现的位置
        self.top.resizable(0, 0)  # 将窗口大小设置为不可变
        self.url = tkinter.StringVar()  # 生成一个StringVar 对象，来保存下面输入框中的内容
        self.create_widgets()
        print("屏幕宽高", self.window_width, self.window_height)

    def quit(self):
        self.top.destroy()

    def get_value(self):
        """获取文本框中数据，并调用XmindToXsl类"""
        url = self.url.get()
        xmind = XmindToXsl(url)
        # try:
        xmind.write_excel()
        messagebox.showinfo('Xmind to xls', '转换成功')  # 弹出消息提示框
        self.quit()
        # except KeyError:
        #     messagebox.showerror('Xmind to xls', 'xmind结构错误')
        #     self.quit()

    def select_path(self):
        """选择要转换成excel的xmind地址"""
        url = askopenfilename(filetypes=(("xmind files", "*.xmind"),))
        self.url.set(url)

    def create_widgets(self):

        first_label = tkinter.Label(self.top, text='文件路径：')  # 生成一个标签
        first_label.grid(row=0, column=0)  # 使用grid布局，标签显示在第一行，第一列
        first_entry = tkinter.Entry(self.top, textvariable=self.url, width=53)  # 生成一个文本框，内容保存在上面变量中
        first_entry.grid(row=0, column=4)  # 使用grid布局，文本框显示在第一行，第二列
        way_button = tkinter.Button(self.top, text="选择文件 ", command=self.select_path)
        way_button.grid(row=0, column=5)  # 使用grid布局，按钮显示在第一行，第三列
        f_btn = tkinter.Frame(self.top)  # 设置一个frame框架，并设置背景颜色为红色
        f_btn.place(x=160, y=355, width=200, height=45)  # 设置框架的大小，及在top窗口显示位置
        submit_button = tkinter.Button(f_btn, text="提交", command=self.get_value, width=28, height=2,
                                       bg="#00FFFF")  # 设置按钮的文字，调用方法，大小，颜色，显示框架

        submit_button.grid(row=5, column=4)  # 使用grid布局，按钮显示在第一行，第一列

        # 进入消息循环（必需组件）
        self.top.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = MainUI(title="Xmind to xlsx")
    # names = "test.xmind"
    # xx = XmindToXsl(names)
    # xx.write_excel()
