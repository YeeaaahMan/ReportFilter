import wx
import wx.adv
import wx.html2
import sys, re, csv, json
import os

cfg_file_name = os.environ["USERPROFILE"] + "\\" "ReportFilter.json"
default_CFG = { "Departments": ["Вопросы технического характера", "Технические вопросы WGC"],
        "Exclusions": ["TWA ALPHA"],
        "Statuses": ["In Queue", "Info Given", "Reopened"], }

def write_cfg(cfg):
    json.dump(cfg, open(cfg_file_name, 'w', encoding="utf-8"), indent=4)

def read_cfg():
    try:
        return json.load(open(cfg_file_name, encoding="utf-8"))
    except:
        write_cfg(default_CFG)
        return default_CFG

CFG = read_cfg()

def filter2(fileName="D:/s_litvinchuk/Downloads/report_2017-05-24_09-21.csv",
            departmentsList=["Вопросы технического характера", "Технические вопросы WGC"],
            exclusionList = ["TWA ALPHA",],
            statusesList = ["In Queue", "Info Given", "Reopened",]):

    statusesList = [stts.lower() for stts in statusesList]

    with open(fileName, encoding="utf-8-sig") as csvfile: # UTF-8-BOM
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        data = [line for line in reader]

    data_filtred = list()
    for dep in departmentsList:
        for row in data:
            if dep.lower() in row[0].lower() and row[1].lower() in statusesList:
                data_filtred.append(row)
    data = data_filtred
    del data_filtred

    for exc in exclusionList:
        data_excluded = list()
        for row in data:
            if exc.lower() not in row[0].lower():
                data_excluded.append(row)
        data = data_excluded
        del data_excluded

    short_data = list()
    for row in data:
        p = row[0].split(' → ')[0] # project
        d = row[0].split(' → ')[1] # department
        sd= row[0].split(' → ')[-1] # sub-department
        stts = row[1] # status
        cnt = int(row[2]) # count

        r = re.findall("(\d+) days (\d+) hours (\d+) minutes", row[3])
        t = [int(i) for i in r[0]]
        m = t[0]*24*60 + t[1]*60 + t[2] # last activity in minutes

        short_data.append( (p, d, sd, stts, cnt, m) )

    data = short_data

    LA = dict() # LastActivity Dict
    for row in data:
        prj = row[0]
        stts = row[-3]
        c_m = row[-2:] # count and minutes

        LA.setdefault(prj, dict())
        LA[prj].setdefault(stts, [])
        LA[prj][stts].append(c_m)
    del data

    return LA

def median(array):
    array.sort()
    if len(array)%2 == 1:
        return array[len(array)//2]
    else:
        return round((array[len(array)//2] + array[len(array)//2 - 1])/2)

def table(project, LA):
    statuses = sorted(LA[project].keys())
    result = """<table class="brd">
    <tr>
        <th width="80">&nbsp;</th>   <th width="80">Status </th>    <th width="60">Count </th>    <th>Last Activity </th>
    </tr>
    """
    count = 0

    for i, stts in enumerate(statuses):
        if i == 0:
            result += """<tr>
        <th rowspan="{0}">{1}</th>""".format(len(statuses), project)
        else:
            result += "<tr>\n"

        c = sum([o[0] for o in LA[project][stts]])  # count
        count += c
        m = max([o[1] for o in LA[project][stts]])  # m
        la = " {0} days {1:0>2} hours {2:0>2} minutes".format(m // 1440, (m % 1440) // 60, m % 60)

        result += """<td>{0}</td>    <td>{1}</td>    <td>{2}</td>
    </tr>\n""".format(stts, c, la)

    result += "</table>\n"
    result += "<p>Общее количество заявок:  <b> -- | {0}</b></p><br>\n".format(count)

    return result

def create_page(LA):
    Style = """<style type="text/css">
    table { border-collapse: collapse;
    font-family: 'Calibri'; font-size: 11pt}
    table th {text-align: "left" },
    table tr {text-align: "right"},
    table td { padding: 0 3px; },
    table.brd th,
    table.brd td { border: 1px solid #000; }
    b { font-family: 'Calibri'; font-size: 11pt }
    p { font-family: 'Calibri'; font-size: 11pt; margin: 0 }
</style>"""

    count_list = list()
    #la_list = list()
    la_list = [0] # добавляю в список 0 для того, чтобы в случае пустого списка LA была возможность рассчитать mx и mdn
    for prj in LA:
        for stts in LA[prj]:
            count_list.extend([i[0] for i in LA[prj][stts]])
            la_list.extend([i[1] for i in LA[prj][stts]])
    mx = max(la_list)
    mx = " {0} days {1:0>2} hours {2:0>2} minutes".format(mx // 1440, (mx % 1440) // 60, mx % 60)
    mdn = median(la_list)
    mdn = " {0} days {1:0>2} hours {2:0>2} minutes".format(mdn // 1440, (mdn % 1440) // 60, mdn % 60)

    Common = """<p><b>Общее количество заявок во всех проектах:  -- | {0}</b><br>
Максимальное время ответа: &nbsp; <b>{1}</b><br>
Среднее время ответа (медианное): &nbsp; <b>{2}</b></p><br>""".format(sum(count_list), mx, mdn)
    """Common += <b>Критические ситуации</b>
<p>1.</p><br>
<b>Ситуации, требующие внимания</b><br>
<p>1.</p><br>
<b>Проблемы в работе</b>
<p>1.</p><br>
<b>Прочее</b><br>
<p>1.</p><br>"""

    Tables = ""
    sorted_tuple = sorted([(key.lower(), key) for key in LA.keys()])
    for prj in [t[1] for t in sorted_tuple]:
        Tables += table(prj, LA)

    return Style + Common + Tables

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Report Filter 2.6", pos=wx.DefaultPosition,
                          size=wx.Size(600, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizerMain = wx.BoxSizer(wx.VERTICAL)
        bSizerHor = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker = wx.FilePickerCtrl(self, wx.ID_ANY, "Выберите report_YYYY-MM-DD_HH-MM.csv файл!",
                                               "Выберите файл",
                                               "report*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        if wx.Platform == '__WXMSW__':
            # wxMSW is one of the platforms where the generic implementation
            # of wx.FilePickerCtrl is used...
            pButt = self.m_filePicker.GetPickerCtrl()
            if pButt is not None:
                pButt.SetLabel('Открыть')

        self.m_buttonSettings = wx.Button(self, wx.ID_ANY, "Настройки", wx.DefaultPosition, wx.DefaultSize, 0)

        #bSizerHor.Add(self.m_buttonSettings, 0, wx.ALL, 5)
        bSizerHor.Add(self.m_filePicker, 1, wx.ALL | wx.EXPAND, 5)
        bSizerHor.Add(self.m_buttonSettings, 0, wx.ALL, 5)

        bSizerMain.Add(bSizerHor, 0, wx.EXPAND, 5)

        drop_target = FileDropTarget(self.m_filePicker)  # adding DropTarget properties
        self.m_filePicker.SetDropTarget(drop_target)

        self.browser = wx.html2.WebView.New(self)
        bSizerMain.Add(self.browser, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_filePicker.Bind(wx.EVT_FILEPICKER_CHANGED, self.startFilter)
        self.m_buttonSettings.Bind(wx.EVT_BUTTON, self.openSettings)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def startFilter( self, event ):
        #global LA
        #print(self.m_filePicker1.GetPath())

        LA = filter2(self.m_filePicker.GetPath(),
                     departmentsList=CFG["Departments"],
                     exclusionList=CFG["Exclusions"],
                     statusesList=CFG["Statuses"])
        page = create_page(LA)
        self.browser.SetPage(page, "Report")

    def openSettings(self, event):
        myApp.settings.m_listBoxDeps.SetStrings( CFG["Departments"] )
        myApp.settings.m_listBoxExcl.SetStrings( CFG["Exclusions"] )
        myApp.settings.m_listBoxStts.SetStrings( CFG["Statuses"] )
        myApp.settings.Show()

class SettingsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Report Filter | Настройки", pos=wx.DefaultPosition,
                          size=wx.Size(548, 400), style=wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP)

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

        self.m_buttonSave = wx.Button(self, wx.ID_ANY, "Сохранить", wx.DefaultPosition, wx.DefaultSize, 0)
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
        self.Hide()

    def SaveSettings(self, event):
        # Использую особенный генератор списка, который отбрасывает пробелы и фильтрует пустые строки
        CFG["Departments"] = [dep.strip()  for dep  in self.m_listBoxDeps.GetStrings() if len(dep.strip()) > 0]
        CFG["Exclusions"]  = [excl.strip() for excl in self.m_listBoxExcl.GetStrings() if len(excl.strip()) > 0]
        CFG["Statuses"]    = [stts.strip() for stts in self.m_listBoxStts.GetStrings() if len(stts.strip()) > 0]
        write_cfg(CFG)
        self.Hide()

class FileDropTarget(wx.FileDropTarget):
    """ This object implements Drop Target functionality for Files """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
          indicate what should receive the dropped files """
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        # Store the Object Reference for dropped files
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        """ Implement File Drop """
        myApp.frame.m_filePicker.SetPath(filenames[0])
        LA = filter2(myApp.frame.m_filePicker.GetPath())
        page = create_page(LA)
        myApp.frame.browser.SetPage(page, "Report")
        return 0

class myApp(wx.App):
    """ app"""
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.frame = MainFrame(parent=None)
        self.frame.Show()
        self.settings = SettingsFrame(parent=self.frame)

        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    myApp = myApp(redirect=True)
    args = sys.argv
    if len(args) > 1:
        #print( args[1] )
        myApp.frame.m_filePicker.SetPath(args[1])
        LA = filter2(myApp.frame.m_filePicker.GetPath())
        page = create_page(LA)
        myApp.frame.browser.SetPage(page, "Report")
    myApp.MainLoop()