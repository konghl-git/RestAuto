#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:kong
@file: restFrameWork.py
@time: 2019/09/08
搭建整个EXE框架
"""
import wx
import db
import menu_data



class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'RestFul流程操作',size=(800, 1000))
        panel = wx.Panel(self, -1)
        self.panel = panel
        panel.SetBackgroundColour("White")
        # icon = wx.Icon(name=path + "\\fish.ico", type=wx.BITMAP_TYPE_ICO)
        # self.SetIcon(icon)
        self.MenuTree = wx.TreeCtrl(self, size=(200, 1000), style=wx.TR_HAS_BUTTONS)
        self.root = self.MenuTree.AddRoot("Rest接口操作", data="root_id")  # 根目录
        self.MenuTree.Expand(self.root)   # 展开根目录
        self.tree()
        self.tree_action()
        self.create_menu()      # 菜单栏

    def OnCloseWindow(self, event):
        self.Destroy()
        quit()

    def Setting_base(self, event): #设置数据库
        app = wx.PySimpleApp()
        frame = Baseframe(parent=self.panel, id=-1)
        frame.Show()
        app.MainLoop()

    def create_menu(self):
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.AppendSeparator()
        menuItem1 = menu1.Append(wx.NewId(), "设置数据库", "只有Oracle现在")
        menu1.AppendSeparator()
        menuItem2 = menu1.Append(wx.NewId(), "退出", "退出")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, menuItem2)  # 退出
        self.Bind(wx.EVT_MENU, self.Setting_base, menuItem1)  # 设置数据库
        menubar.Append(menu1, "设置")

        self.SetMenuBar(menubar)

    def tree(self):
        """
        用来创建目录结构树的
        :return:
        """
        menu_id = []            # 用来存放上级id
        self.menu_all = {u"root_id": self.root}          # 使用字典将数据库id和目录标识id捆绑
        level = 1
        while True:
            menu_level = menu_data.show_menu(level)
            if menu_level == None:
                break
            for item2 in menu_data.show_menu(level-1):
                for item in menu_level:
                    if item[1] == item2[0]:
                        child = self.MenuTree.AppendItem(self.menu_all[item2[0]], item[2])
                        self.menu_all[item[0]] = child
            if len(menu_level) == 0:
                break
            level += 1
        self.MenuTree.Expand(self.root)

    def tree_action(self):
        """
        创建操作tree的弹出式菜单
        :return:
        """
        self.MenuTree.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

    def onexit(self, event):
        self.Close()

    def OnShowPopup(self,event):
        """
        用来弹出显示
        :param event:
        :return:
        """
        try:
            title = self.MenuTree.GetItemText(self.get_selcet_id()[0])
        except TypeError as e:             # 未选中目录
            return 0
        self.popupmenu = wx.Menu(title)
        item = self.popupmenu.Append(-1,"增加子菜单")
        self.Bind(wx.EVT_MENU, self.add_child, item)
        item2 = self.popupmenu.Append(-1,"删除菜单")
        self.Bind(wx.EVT_MENU, self.delete_menu, item2)
        item3 = self.popupmenu.Append(-1,"修改菜单")
        self.Bind(wx.EVT_MENU, self.change_menu, item3)
        pos = event.GetPosition()
        pos = self.panel.ScreenToClient(pos)
        self.panel.PopupMenu(self.popupmenu, pos)

    def menu_action_message(self):
        """
        菜单操作后的提示语句，同时刷新树机构
        :return:
        """
        wx.MessageBox("操作成功")
        self.MenuTree.DeleteAllItems()
        self.root = self.MenuTree.AddRoot("Rest接口操作", data="root_id")  # 根目录
        self.tree()


    def add_child(self, event):
        """
        用来反应选择的弹出框,增加子菜单
        :param event:
        :return:
        """
        menu = self.get_selcet_id()

        # 先弹出一个对话框
        dlg = wx.TextEntryDialog(None,"请输入目录名称：","创建目录")
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
        else:
            return 0
        add = menu_data.menu_data_add(menu[1],response)
        if add:
            self.menu_action_message()
        else:
            wx.MessageBox("当前目录下存在重复目录")

    def delete_menu(self,event):
        """
        用来删除菜单
        :param event:
        :return:
        """
        menu = self.get_selcet_id()

        # 先判断选中框是否为根目录
        if menu[1] == u"root_id":
            wx.MessageBox("根目录不可被删除！")
            return 0
        # 先弹出提示框
        dlg = wx.MessageDialog(None,"是否删除？","删除确认",style=wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            # 开始删除,先进行单个删除，如果存在下级目录再进行判断
            if menu_data.menu_delete_alone(menu[1]):
                self.menu_action_message()      # 成功删除
            else:
                dlg = wx.MessageDialog(None, "存在下级目录是否全部删除？", "删除确认", style=wx.OK | wx.CANCEL)
                result = dlg.ShowModal()
                dlg.Destroy()
                if result == wx.ID_OK:
                    menu_data.menu_delete_all(menu[1])
                    self.menu_action_message()

    def change_menu(self,event):
        """
        修改目录
        :param event:
        :return:
        """
        menu = self.get_selcet_id()

        # 先判断选中框是否为根目录
        if menu[1] == u"root_id":
            wx.MessageBox("根目录不可被修改！")
            return 0
        # 先弹出一个对话框
        dlg = wx.TextEntryDialog(None, "请输入新的目录名称：", "修改目录")
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()

        change = menu_data.change_menu(menu[1], response)
        if change:
            self.menu_action_message()
        else:
            wx.MessageBox("当前目录下已经存在此目录名")


    def get_selcet_id(self):
        """
        获取到鼠标右键对于树选择框的id
        :return:menu_id和数据库id
        """
        menu_id = self.MenuTree.GetSelection()
        menu_all = {k: v for v, k in self.menu_all.items()}   # 颠倒一下key和velue位置
        return menu_id, menu_all[menu_id]


# 设置数据的子窗口
class Baseframe(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '数据设置', size=(600, 500))
        panel = wx.Panel(self, -1)
        self.panel = panel
        # panel.SetBackgroundColour("White")
        self.create_text()
        self.selct_db_type()
        self.select_by_name()
        self.save_button()

    def create_text(self):
        """
        创建文本输入框
        :return:
        """
        ip_text = wx.StaticText(self.panel,-1,"ip:",pos=(40, 100))
        self.ip = wx.TextCtrl(self.panel, -1, "ip地址", pos=(100, 100),size=(200,-1))
        port_text = wx.StaticText(self.panel,-1,"port:",pos=(310, 100))
        self.port = wx.TextCtrl(self.panel, -1, "端口号", pos=(350,100),size=(50,-1))
        DB_name_text = wx.StaticText(self.panel, -1, "数据库名:", pos=(40, 130))
        self.DB_name = wx.TextCtrl(self.panel, -1, "数据库名称或者侦听", pos=(100, 130),size=(200,-1))
        user_name_text = wx.StaticText(self.panel, -1, "用户名:", pos=(40, 160))
        self.user_name = wx.TextCtrl(self.panel, -1, "数据库用户名称", pos=(100, 160),size=(200,-1))
        password_text = wx.StaticText(self.panel, -1, "密码:", pos=(40, 190))
        self.password = wx.TextCtrl(self.panel, -1, "数据库密码", pos=(100, 190),size=(200,-1))
        message_name_text = wx.StaticText(self.panel, -1, "数据名:", pos=(40, 220))
        self.message_name = wx.TextCtrl(self.panel, -1, "数据保存名", pos=(100, 220), size=(200, -1))

        # 状态栏
        state_text = wx.StaticText(self.panel, -1, "状态栏:", pos=(330, 160))
        self.state =wx.TextCtrl(self.panel, -1, "", pos=(380, 160), size=(150, 80),style=wx.TE_MULTILINE|wx.TE_READONLY)

    def selct_db_type(self):
        """
        创建下拉框用来选择数据库类型
        :return:
        """
        # 先获取数据库连接信息
        db_message = db.DB()
        message_all = db_message.get_message()

        # 根据修改时间判断最近修改的信息用来展示
        if message_all == None:
            type_name = u"Oracle"
        else:
            for message in message_all:
                if message[7] == max([x[7] for x in message_all]):
                    type_name = message[1]
                    break
        # 文本
        wx.StaticText(self.panel, -1, "数据库类型:", pos=(40, 60))
        self.DB_type = wx.ComboBox(self.panel, wx.NewId(),type_name, (110,60), wx.DefaultSize, [u"Oracle",u"MySQL"],
                                 wx.CB_DROPDOWN | wx.CB_READONLY)

    def select_by_name(self):
        """
        数据库连接的数据名下拉框
        :return:
        """
        # 文本
        wx.StaticText(self.panel, -1, "数据名:", pos=(300, 60))
        # 先获取数据库连接信息Oracle 的时候
        db_message = db.DB()
        db_type = self.DB_type.GetValue()
        message_all = db_message.get_message(db_type)
        # 根据修改时间判断最近修改的信息用来展示
        if message_all == None:
            name = ""
            name_list = []
        else:
            for message in message_all:
                if message[7] == max([x[7] for x in message_all]):
                    name = message[0]
                    name_list = [x[0] for x in message_all]
                    break
        self.name = wx.ComboBox(self.panel, wx.NewId(),name, (350,60), wx.DefaultSize, [],
                                 wx.CB_DROPDOWN | wx.CB_READONLY)


    def message_show(self):
        """
        对于输入的信息默认填写
        :return:
        """
        # 先获取数据库连接信息
        db_message = db.DB()
        db_type = self.DB_type.GetValue()
        message_all = db_message.get_message(db_type)
        if self.name.GetValue() == "":
            return 0
        else:
            for message in message_all:
                if message[0] == self.name.GetValue():
                    self.ip.SetLabel(message[6])
                    self.port.SetLabel(message[3])
                    self.DB_name.SetLabel(message[2])
                    self.user_name.SetLabel(message[4])
                    self.password.SetLabel(message[5])
                    self.message_name.SetLabel(message[0])

    def save_button(self):
        """
        测试按钮，连接成功会自动保存
        :return:
        """
        run = wx.Image("run.bmp", wx.BITMAP_TYPE_BMP,).ConvertToBitmap()
        # 文本
        wx.StaticText(self.panel, -1, "测试:", pos=(40, 320))
        self.button = wx.BitmapButton(self.panel, -1, run, pos=(100, 300))
        self.button.Bind(wx.EVT_BUTTON,self.test_link)
        # bmp1 = wx.Image("ye.bmp", wx.BITMAP_TYPE_BMP, ).ConvertToBitmap()
        # self.button.SetBitmap(bmp1)

    def test_link(self,event):
        """
        测试连接操作
        :return:
        """
        db_action = db.DB()
        ip = self.ip.GetValue()
        port = self.port.GetValue()
        DB_name = self.DB_name.GetValue()
        username = self.user_name.GetValue()
        password = self.password.GetValue()
        message = self.message_name.GetValue()
        DB_type = self.DB_type.GetValue()
        db_action.afferent_message(ip, username, password, DB_type, DB_name, port)
        if message == "":
            self.state.SetLabel("数据名不可为空")
            return 0
        result = db_action.connect(message)

        if result[0] == 0:
            fail = wx.Image("fail.bmp", wx.BITMAP_TYPE_BMP, ).ConvertToBitmap()
            self.button.SetBitmap(fail)
            self.state.SetLabel(str(result[1]))
        else:
            success = wx.Image("success.bmp", wx.BITMAP_TYPE_BMP, ).ConvertToBitmap()
            self.button.SetBitmap(success)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()