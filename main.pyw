# -*- coding: utf-8 -*-
__author__ = 'Sergei'

import wx
import wx.xrc

def removeQuotes(line):
    while line.find('"') != -1:
        line = line.replace('"', '')
    return line

def filter(fileName="report.csv", departmentsList=["Технические"], statusesList = ["In Queue", "Info Given", "Reopened"]):
    fh = open(fileName,'r')
    report = list()

    for line in fh:
        line = removeQuotes(line)
        for dep in departmentsList:
            if dep.lower() in line.lower():
                if line.split(',')[1] in statusesList:
                    report.append(line.strip())
    fh.close()
    #report.sort()

    count = 0
    totalCount = 0
    department = None
    result =  'Department\tStatus\tTotal\tLast Activity\n'

    for l in report:
        if department is None:
            department = l[:l.find(',')]
            count = int(l.split(',')[2])
            result = result + "\t".join(l.split(',')) + '\n'
            continue

        elif department == l[:l.find(',')]:
            count += int(l.split(',')[2])
            result = result + "\t".join(l.split(',')) + '\n'

        elif department != l[:l.find(',')]:
            totalCount += count
            result = result + "\t\t" + str(count) + "\t" + '\n'
            result = result + "\t".join(l.split(',')) + '\n'
            department = l[:l.find(',')]
            count = int(l.split(',')[2])

    result = result + "\t\t" + str(count) + "\t" + '\n'
    totalCount += count
    result = result + "\tAbsolute count:\t" + str(totalCount) + "\t" + '\n'

    return result

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Report Filter", pos = wx.DefaultPosition, size = wx.Size( 700,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_filePicker1 = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"report*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer2.Add( self.m_filePicker1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"Choose report_YYYY-MM-DD_HH-MM.csv file!", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
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
        self.m_textCtrl1.AppendText( filter( self.m_filePicker1.GetTextCtrlValue() ).decode('utf-8') )

class myApp(wx.App):
    """ app"""
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.frame = MyFrame1(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    # (1) Text redirection starts here
    myApp = myApp(redirect=True)
    # (2) The main event loop is entered here
    myApp.MainLoop()
