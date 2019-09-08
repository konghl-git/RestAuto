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
        frame = Baseframe(parent=None, id=-1)
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
        title = self.MenuTree.GetItemText(self.get_selcet_id()[0])
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
        panel.SetBackgroundColour("White")



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()