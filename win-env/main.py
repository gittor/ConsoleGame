#encoding=utf-8

import wx, getpass, sys, time
import _winreg as win
import json
import zcmd

# 配置文件操作
#####################################
def read_config():
    try:
        with open('win-env-config.json') as fin:
            return json.load(fin)
    except:
        return {'show_help':True, 'records':[]}
def add_modify(rd):
    config = read_config()
    config['records'].append(rd)
    with open('win-env-config.json', 'w') as fout:
        json.dump(config, fout, indent=4)
def set_config(key, value):
    config = read_config()
    config[key] = value
    with open('win-env-config.json', 'w') as fout:
        json.dump(config, fout, indent=4)
#####################################

# 注册表操作
#####################################
# ret: { name:value }
def get_reg(key):
    assert key!=None
    ret = {}
    val_num = win.QueryInfoKey(key)[1]
    for i in range(val_num):
        name, data, _ = win.EnumValue(key, i)
        ret[ name ] = data
    return ret

def judge_type(value):
    return win.REG_EXPAND_SZ if '%' in value else win.REG_SZ
    
# data: { key:data }
def set_reg(key, data):
    org = get_reg(key)
    record = []
    for k in set(org)-set(data):
        record.append([k, None, None])
        win.DeleteValue(key, k)
    for k, v in data.items():
        if org.get(k)==v: continue
        record.append([k, org.get(k), v])
        win.SetValueEx(key, k, 0, judge_type(v), v)
    if record:
        add_modify(record)

def user_key():
    return win.OpenKey(win.HKEY_CURRENT_USER, 'Environment', 0, win.KEY_ALL_ACCESS)
def all_key():
    return win.OpenKey(win.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 0, win.KEY_ALL_ACCESS)
def env_user():
    return get_reg(user_key())
def env_all():
    return get_reg(all_key())
#####################################

class AboutDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='About-Warning')
        
        ok = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((60, 20), 0, wx.EXPAND)
        sizer.Add( wx.StaticText(self, label='请确保以管理员身份运行，操作方式如下图'), 0, wx.ALIGN_CENTER )
        sizer.Add((60, 20), 0, wx.EXPAND)
        tex = wx.Bitmap(zcmd.where('help.png'))
        bmp = wx.StaticBitmap(self, -1, tex)
        sizer.Add(bmp, 0, wx.ALIGN_CENTER)
        sizer.Add((60, 20), 0, wx.EXPAND)
        
        sizer.Add(ok, 0, wx.ALIGN_CENTER)
        sizer.Add(cancel, 0, wx.ALIGN_CENTER)
        ok.Bind(wx.EVT_BUTTON, self.onNoHelp)
        
        self.SetSizer(sizer)
        self.Fit()
        self.CenterOnParent()
    def onNoHelp(self, evt):
        set_config('show_help', False)
        self.EndModal(wx.ID_OK)
class ChangeDlg(wx.Dialog):
    def __init__(self, parent, key, value):
        wx.Dialog.__init__(self, parent, title = u'修改', style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.key = wx.TextCtrl(self, style=wx.TE_READONLY if key else 0)
        self.value = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.ok = wx.Button(self, wx.ID_OK, label='确定')
        self.cancel = wx.Button(self, wx.ID_CANCEL, label='取消')
        
        if key:
            self.key.SetValue(key)
        if value:
            txts = [line for line in value.split(';') if line.strip()]
            self.value.AppendText('\n'.join(txts))

        a = wx.BoxSizer(wx.HORIZONTAL)
        a.Add( wx.StaticText(self, label='变量名(&N)：'), 0, wx.ALIGN_CENTER )
        a.Add( self.key, 1 )
        
        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add( wx.StaticText(self, label='变量值(&V)：'), 0, wx.ALIGN_TOP )
        b.Add( self.value, 1, wx.EXPAND )
        
        c = wx.BoxSizer(wx.HORIZONTAL)
        c.Add( self.ok )
        c.Add( self.cancel )
        
        x = wx.BoxSizer(wx.VERTICAL)
        x.Add( a, 0, wx.EXPAND|wx.ALL, 10 )
        x.Add( b, 1, wx.EXPAND|wx.ALL, 10 )
        x.Add( c, 0, wx.ALL|wx.ALIGN_RIGHT, 10 )
        self.SetSizer(x)
        
        self.key.Bind(wx.EVT_TEXT, self.onTextChanged)
        self.value.Bind(wx.EVT_TEXT, self.onTextChanged)
        
        self.onTextChanged(None)

    def onTextChanged(self, evt):
        k, v = self.key.GetValue().strip(), self.value.GetValue().strip()
        self.ok.Enable( bool(k and v) )
        return

    def GetInput(self):
        lines = self.value.GetValue().split('\n')
        lines = [ln for ln in lines if ln.strip()]
        return (self.key.GetValue().strip(), ';'.join(lines))
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u'环境变量')
        
        self.Maximize(True)
        
        panel = wx.Panel(self)
        
        #整体布局
        root = wx.BoxSizer(wx.VERTICAL)        
        
        splitter = wx.SplitterWindow(panel, style = wx.SP_LIVE_UPDATE)
        # splitter.SetBackgroundColour("pink")
        s1 = wx.StaticBox(splitter, label=u'%s 的用户变量(&U)'%getpass.getuser())
        s2 = wx.StaticBox(splitter, label=u'系统变量(&S)')
        splitter.SplitHorizontally(s1, s2)
        splitter.SetSashGravity(0.5)
        
        root_2 = wx.BoxSizer(wx.HORIZONTAL)
        b1 = wx.Button(panel, wx.ID_OK, label=u'确定')
        b2 = wx.Button(panel, wx.ID_CANCEL, label=u'取消')
        root_2.Add(b1)
        root_2.Add(b2)
        
        root.Add(splitter, 1, wx.EXPAND|wx.ALL, 10)
        root.Add(root_2, 0, wx.ALIGN_RIGHT)
        
        #splitter内部布局
        t = wx.BoxSizer(wx.VERTICAL)
        m = wx.BoxSizer(wx.HORIZONTAL)
        un = wx.Button(s1,label=u'新建(&N)...'); m.Add( un )
        ue = wx.Button(s1,label=u'编辑(&E)...'); m.Add( ue )
        ur = wx.Button(s1,label=u'删除(&D)'); m.Add(ur)
        t.Add((60, 20), 0, wx.EXPAND)
        self.user = wx.ListCtrl(s1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.user.InsertColumn(0, u"变量")
        self.user.InsertColumn(1, u"值", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.user_org = env_user()
        for k, v in self.user_org.items():
            idx = self.user.InsertItem( sys.maxint, k )
            self.user.SetItem(idx, 1, v)
        self.user.Select(0)
        t.Add(self.user, 1, wx.EXPAND|wx.ALL, 10)
        t.Add( m , 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT, 10)
        s1.SetSizer(t)
        t.Fit(s1)
        
        t = wx.BoxSizer(wx.VERTICAL)
        m = wx.BoxSizer(wx.HORIZONTAL)
        an = wx.Button(s2,label=u'新建(&W)...'); m.Add( an )
        ae = wx.Button(s2,label=u'编辑(&I)...'); m.Add( ae )
        ar = wx.Button(s2,label=u'删除(&L)'); m.Add( ar )
        t.Add((60, 20), 0, wx.EXPAND)
        self.all = wx.ListCtrl(s2, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.all.InsertColumn(0, u"变量")
        self.all.InsertColumn(1, u"值", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.all_org = env_all()
        for k, v in self.all_org.items():
            idx = self.all.InsertItem( sys.maxint, k )
            self.all.SetItem(idx, 1, v)
        self.all.Select(0)
        t.Add(self.all, 1, wx.EXPAND|wx.ALL, 10)
        t.Add( m , 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT, 10)
        s2.SetSizer(t)
        t.Fit(s2)

        panel.SetSizer(root)
        root.Fit(panel)
        self.CentreOnParent(wx.BOTH)
        
        un.Bind(wx.EVT_BUTTON, self.onNewUser)
        ue.Bind(wx.EVT_BUTTON, self.onEditUser)
        ur.Bind(wx.EVT_BUTTON, self.onRemoveUser)
        self.user.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDbClickUser)
        an.Bind(wx.EVT_BUTTON, self.onNewAll)
        ae.Bind(wx.EVT_BUTTON, self.onEditAll)
        ar.Bind(wx.EVT_BUTTON, self.onRemoveAll)
        self.all.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDbClickAll)

        b1.Bind(wx.EVT_BUTTON, self.onOk)
        b2.Bind(wx.EVT_BUTTON, self.onCancel)
        
        if read_config().get('show_help') and zcmd.where('help.png'):
            dlg = AboutDlg(self)
            dlg.ShowModal()
            dlg.Destroy()
    def newEnvItem(self, listctrl, org):
        dlg = ChangeDlg(self, None, None)
        if wx.ID_OK == dlg.ShowModal():
            k, v = dlg.GetInput()
            listctrl.FindItem(-1, k)
            idx = listctrl.InsertItem( sys.maxint, k )
            self.user.SetItem(idx, 0, k)
            self.user.SetItem(idx, 1, v)
            self.user.Select(idx)
            self.user.EnsureVisible(idx)
            org[k] = v
    def editEnvItem(self, listctrl, org):
        idx = listctrl.GetFirstSelected()
        if idx==-1: return
        dlg = ChangeDlg(self, listctrl.GetItemText(idx, 0), listctrl.GetItemText(idx, 1))
        if wx.ID_OK == dlg.ShowModal():
            k, v = dlg.GetInput()
            listctrl.SetItem(idx, 1, v)
            org[k] = v
    def removeEnvItem(self, listctrl, org):
        idx = listctrl.GetFirstSelected()
        if idx==-1: return
        k = listctrl.GetItemText(idx, 0)
        del org[k]
        listctrl.DeleteItem(idx)
        if idx>0: listctrl.Select(idx-1)
        else: listctrl.Select(0)
    #####################################
    def onNewUser(self, evt):
        self.newEnvItem(self.user, self.user_org)
    def onEditUser(self, evt):
        self.editEnvItem(self.user, self.user_org)
    def onRemoveUser(self, evt):
        self.removeEnvItem(self.user, self.user_org)
    def onDbClickUser(self, evt):
        self.editEnvItem(self.user, self.user_org)
    #####################################
    def onNewAll(self, evt):
        self.newEnvItem(self.all, self.all_org)
    def onEditAll(self, evt):
        self.editEnvItem(self.all, self.all_org)
    def onRemoveAll(self, evt):
        self.removeEnvItem(self.all, self.all_org)
    def onDbClickAll(self, evt):
        self.editEnvItem(self.all, self.all_org)
    ################################################
    def onOk(self, evt):
        set_reg(user_key(), self.user_org)
        set_reg(all_key(), self.all_org)
        self.Destroy()
    def onCancel(self, evt):
        self.Destroy()
    
if __name__=="__main__":
    app = wx.App()
    f = MainFrame()
    f.Show()
    app.MainLoop()
    
    