# -*- coding: utf-8 -*-
__author__ = 'Sergei'

import wx
import wx.xrc
from report import filter

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Report Filter", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_filePicker1 = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"report*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer2.Add( self.m_filePicker1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"Choose  'report_YYYY-MM-DD_HH-MM.csv'  file!", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        bSizer2.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.startFilter )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def startFilter( self, event ):
        self.m_textCtrl1.Clear()
        self.m_textCtrl1.AppendText( filter( self.m_filePicker1.GetTextCtrlValue(), ["cybersports", "по премиум", "свободный", "по внутриигровому", "случайно продал", "пропало", "внутриигровые", "игровая", "кланы"] ).decode('utf-8')  )

class App(wx.App):
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.frame = MyFrame1(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    # (1) Text redirection starts here
    app = App(redirect=True)
    # (2) The main event loop is entered here
    app.MainLoop()