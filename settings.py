import wx
import wx.adv

class SettingsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Report Filter | Настройки", pos=wx.DefaultPosition,
                          size=wx.Size(548, 400), style=wx.CAPTION|wx.CLOSE_BOX)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerVert = wx.BoxSizer(wx.VERTICAL)

        self.m_listBoxDeps = wx.adv.EditableListBox(self, wx.ID_ANY, label="Департаменты", )
        bSizerVert.Add(self.m_listBoxDeps, 1, wx.ALL | wx.EXPAND, 5)

        bSizerHor = wx.BoxSizer(wx.HORIZONTAL)

        self.m_listBoxExcl = wx.adv.EditableListBox(self, wx.ID_ANY, label="Исключения", )
        bSizerHor.Add(self.m_listBoxExcl, 1, wx.ALL | wx.EXPAND, 5)

        self.m_listBoxStts = wx.adv.EditableListBox(self, wx.ID_ANY, label="Статусы", )
        bSizerHor.Add(self.m_listBoxStts, 1, wx.ALL | wx.EXPAND, 5)

        bSizerVert.Add(bSizerHor, 1, wx.EXPAND, 5)

        bSizerMain.Add(bSizerVert, 1, wx.EXPAND, 5)

        self.m_buttonSave = wx.Button(self, wx.ID_ANY, u"Сохранить", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerMain.Add(self.m_buttonSave, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.m_buttonSave.Bind(wx.EVT_BUTTON, self.SaveSettings)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def onClose(self, event):
        print("Hide")

    def SaveSettings(self, event):
        self.m_listBoxDeps.SetStrings([u"Вопросы технического характера", u"Технические вопросы WGC"])
        self.m_listBoxExcl.SetStrings( [u"TWA ALPHA"] )
        self.m_listBoxStts.SetStrings( [u"In Queue", u"Info Given", u"Reopened"] )

        #print(self.m_listBoxDeps.GetStrings())
        #print(self.m_listBoxExcl.GetStrings())
        #print(self.m_listBoxStts.GetStrings())

class myApp(wx.App):
    """ app"""
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.frame = SettingsFrame(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    myApp = myApp(redirect=True)
    myApp.MainLoop()