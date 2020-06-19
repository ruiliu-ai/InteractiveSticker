# -*- coding: utf-8 -*-

import wx
from frame_func import *

APP_TITLE = 'Interactive Sticker'
class mainApp(wx.App):
    def OnInit(self, info='basic'):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show(True)
        return True

    def UpdateUI(self, info):
        self.Frame.Destroy()
        self.Frame = self.manager.GetFrame(info)
        print('info:', info)
        self.Frame.Show(True)
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()