import wx
import wx.adv
import wx.lib.buttons as buttons
import sys, os

APP_ICON = 'sticker.ico'
APP_TITLE = 'Interactive Sticker'
img_dir = 'images/'
class mainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, 0, APP_TITLE, style=wx.FRAME_TOOL_WINDOW|wx.STAY_ON_TOP|wx.SYSTEM_MENU\
                                                             |wx.CAPTION|wx.RESIZE_BORDER|wx.CLOSE_BOX)
        self.SetBackgroundColour(wx.WHITE)
        fr_size = 600
        self.SetSize((112, fr_size))
        self.Center()
        self.SetPosition((1400, 100))
        self.tbIcon = CustomTaskBarIcon(self)

        copy_image = wx.Image(img_dir+"copy_image.jpg", wx.BITMAP_TYPE_ANY).Scale(64, 64).ConvertToBitmap()
        self.cp_im = wx.BitmapButton(self, 1, copy_image, pos=[10, 10])
        copy_text1 = wx.Image(img_dir+"copy_text1.png", wx.BITMAP_TYPE_PNG).Scale(64, 64).ConvertToBitmap()
        self.cp_tx1 = wx.BitmapButton(self, 2, copy_text1, pos=[10, 85])
        copy_text2 = wx.Image(img_dir+"copy_text2.png", wx.BITMAP_TYPE_PNG).Scale(64, 64).ConvertToBitmap()
        self.cp_tx2 = wx.BitmapButton(self, 3, copy_text2, pos=[10, 160])
        copy_text3 = wx.Image(img_dir+"copy_text3.png", wx.BITMAP_TYPE_PNG).Scale(64, 64).ConvertToBitmap()
        self.cp_tx3 = wx.BitmapButton(self, 4, copy_text3, pos=[10, 235])
        clearall = wx.Image(img_dir+"clear_all.jpg", wx.BITMAP_TYPE_JPEG).Scale(64, 64).ConvertToBitmap()
        self.clr = wx.BitmapButton(self, 5, clearall, pos=[10, 310])
        im_zoom_in = wx.Image(img_dir+"zoom_in.png", wx.BITMAP_TYPE_PNG).Scale(32, 32).ConvertToBitmap()
        self.zoomin = wx.BitmapButton(self, 6, im_zoom_in, pos=[10, 395], style=wx.NO_BORDER)
        im_zoom_out = wx.Image(img_dir+"zoom_out.png", wx.BITMAP_TYPE_PNG).Scale(32, 32).ConvertToBitmap()
        self.zoomout = wx.BitmapButton(self, 7, im_zoom_out, pos=[48, 395], style=wx.NO_BORDER)

        self.emoji_bank = os.listdir('emoji_apple')
        self.bag_of_emoji_pos = [[10, 445], [35, 445], [60, 445], [10, 470],
                                 [35, 470], [60, 470], [10, 495], [35, 495],
                                 [60, 495], [10, 520], [35, 520], [60, 520]]
        self.bag_of_emoji_code = ['1f600', '1f601', '1f606', '1f605', '1f602', '1f643',
                                  '1f609', '1f60b', '1f914', '1f92b', '1f60f', '1f614']
        for i, bag_emoji in enumerate(zip(self.bag_of_emoji_code, self.bag_of_emoji_pos)):
            code, pos = bag_emoji
            #code = int(code, base=16)
            #emoji_lb = wx.Button(self, i+12, chr(code), size=(24,24), pos=pos)
            selected = list(filter(lambda x: x if code in x else None, self.emoji_bank))
            em_im = wx.Image(os.path.join('emoji_apple', selected[0]), wx.BITMAP_TYPE_ANY).Scale(24,24).ConvertToBitmap()
            wx.BitmapButton(self, i+12, em_im, size=(24, 24), pos=pos, style=wx.NO_BORDER)

        self.zh_sgn = '！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】' \
                      + '〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘‛“”„‟…‧﹏.'

        self.Bind(wx.EVT_BUTTON, self.OnPasteImage, self.cp_im)
        self.Bind(wx.EVT_BUTTON, self.OnPasteText1, self.cp_tx1)
        self.Bind(wx.EVT_BUTTON, self.OnPasteText2, self.cp_tx2)
        self.Bind(wx.EVT_BUTTON, self.OnPasteText3, self.cp_tx3)
        #self.Bind(wx.EVT_BUTTON, self.OnPaste, self.paste)
        self.Bind(wx.EVT_BUTTON, self.OnZoomIn, self.zoomin)
        self.Bind(wx.EVT_BUTTON, self.OnZoomOut, self.zoomout)
        #self.Bind(wx.EVT_BUTTON, self.OnCloseCurrent, self.close)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.clr)
        for i in range(len(self.bag_of_emoji_code)):
            self.Bind(wx.EVT_BUTTON,
                      lambda evt, mark=self.bag_of_emoji_code[i]: self.OnPasteEmoji(evt, mark),
                      wx.FindWindowById(i+12))
        #self.bag_of_buttons = [self.cp_im, self.cp_tx1, self.cp_tx2, self.cp_tx3]
        #self.dict_of_modes = {self.cp_im: 'cp_im', self.cp_tx1: 'cp_tx1',
        #                      self.cp_tx2: 'cp_tx2', self.cp_tx3: 'cp_tx3'}
        self.mode = 'none'
        self.id_start = 101
        self.id_end = 101
        #self.bag_of_cpimages = {}
        #self.bag_of_cpimsizes = {}
        #for i, j in enumerate(list(range(1, 5))):
        #    self.Bind(wx.EVT_BUTTON,  lambda evt, mark=j: self.OnButtonOnly(evt, mark),
        #              self.bag_of_buttons[i])
        #self.text_size = 15

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnButtonOnly(self, event, mark):
        btn = wx.FindWindowById(mark)
        if btn.GetValue() == True:
            for button in self.bag_of_buttons:
                button.SetValue(False)
            btn.SetValue(True)
            self.mode = self.dict_of_modes[btn]

    def OnPaste(self, event):
        if self.mode == 'cp_im':
            self.paste_image()
        elif self.mode == 'cp_tx1':
            self.paste_text1()
        elif self.mode == 'cp_tx2':
            self.paste_text2()
        elif self.mode == 'cp_tx3':
            self.paste_text3()

    def OnPasteImage(self, evt):
        self.paste_image()

    def OnPasteText1(self, evt):
        self.paste_text1()

    def OnPasteText2(self, evt):
        self.paste_text2()

    def OnPasteText3(self, evt):
        self.paste_text3()

    def OnPasteEmoji(self, event, mark):
        self.paste_emoji(mark)

    def add_emoji(self, message):
        emoji_code_list = message.split(';')
        for j in range(len(emoji_code_list)):
            self.bag_of_emoji_code.pop()
        for code in emoji_code_list:
            self.bag_of_emoji_code.insert(0, code)
        for i, bag_emoji in enumerate(zip(self.bag_of_emoji_code, self.bag_of_emoji_pos)):
            wx.FindWindowById(i+12).Destroy()
            code, pos = bag_emoji
            #code = int(code, base=16)
            #emoji_lb = wx.Button(self, i + 12, chr(code), size=(24, 24), pos=pos)
            selected = list(filter(lambda x: x if code in x else None, self.emoji_bank))
            em_im = wx.Image(os.path.join('emoji_apple', selected[0]), wx.BITMAP_TYPE_ANY).Scale(24, 24).ConvertToBitmap()
            wx.BitmapButton(self, i + 12, em_im, size=(24, 24), pos=pos, style=wx.NO_BORDER)
        for i in range(len(self.bag_of_emoji_code)):
            self.Bind(wx.EVT_BUTTON,
                      lambda evt, mark=self.bag_of_emoji_code[i]: self.OnPasteEmoji(evt, mark),
                      wx.FindWindowById(i + 12))

    def paste_emoji(self, message):
        selected = list(filter(lambda x: x if message in x else None, self.emoji_bank))
        if len(selected) == 0:
            dlg = wx.MessageDialog(None, 'Please enter a corrent unicode for emoji',
                                   'Message', wx.OK)
            answer = dlg.ShowModal()
            dlg.Destroy()
        else:
            im = wx.Image(os.path.join('emoji_apple', selected[0]), wx.BITMAP_TYPE_ANY)
            frame = EmojiFrame(self, self.id_end, im)
            frame.Show(True)
            self.Bind(wx.EVT_BUTTON,
                      lambda evt, mode=self.id_end: self.SwitchOnClick(evt, mode),
                      frame.display)
            self.mode = self.id_end
            self.id_end += 1

    def paste_image(self):
        file_obj = wx.FileDataObject()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(file_obj):
                filename = file_obj.GetFilenames()
                print(filename[0], type(filename[0]))
                im = wx.Image(filename[0], wx.BITMAP_TYPE_ANY)
                frame = SingleFrame(self, self.id_end, im)
                frame.Show(True)
                self.Bind(wx.EVT_BUTTON,
                          lambda evt, mode=self.id_end: self.SwitchOnClick(evt, mode),
                          frame.display)
                frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                frame.display.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                self.mode = self.id_end
                self.id_end += 1

    def count_word_length(self, word):
        base_len = len(word)
        for c in word:
            if '\u4e00' <= c <= '\u9fa5' or c in self.zh_sgn:
                base_len += 1
        if base_len > 192:
            dlg = wx.MessageDialog(None, 'Do not copy more than 192 characters\n'
                                         +'请不要复制超过96个中文符号', 'Message', wx.OK)
            answer = dlg.ShowModal()
            dlg.Destroy()
            return False
        else:
            return True

    def reconstruct_word(self, word):
        all_list = ''
        oneline = ''
        count_oneline = 0
        for c in word:
            if '\u4e00' <= c <= '\u9fff' or c in self.zh_sgn:
                oneline += c
                count_oneline += 2
            else:
                oneline += c
                count_oneline += 1
            if c == '\n':
                all_list += oneline
                oneline = ''
                count_oneline = 0
            elif count_oneline >=23:
                all_list += oneline+'\n'
                oneline = ''
                count_oneline = 0
        return all_list

    def paste_text1(self):
        text_obj = wx.TextDataObject()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                word = text_obj.GetText()
                whether_paste = self.count_word_length(word)
                if whether_paste:
                    word = self.reconstruct_word(word)
                    forecolor = wx.Colour(255, 0, 0)
                    backcolor = wx.Colour(189, 215, 238)
                    frame = TextFrame(self, self.id_end, word, forecolor, backcolor)
                    frame.Show(True)
                    self.Bind(wx.EVT_BUTTON,
                              lambda evt, mode=self.id_end: self.SwitchOnClick(evt, mode),
                              frame.text)
                    frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    frame.text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    self.mode = self.id_end
                    self.id_end += 1

    def paste_text2(self):
        text_obj = wx.TextDataObject()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                word = text_obj.GetText()
                whether_paste = self.count_word_length(word)
                if whether_paste:
                    word = self.reconstruct_word(word)
                    forecolor = wx.Colour(0, 176, 240)
                    backcolor = wx.Colour(240, 195, 188)
                    frame = TextFrame(self, self.id_end, word, forecolor, backcolor)
                    frame.Show(True)
                    self.Bind(wx.EVT_BUTTON,
                              lambda evt, mode=self.id_end: self.SwitchOnClick(evt, mode),
                              frame.text)
                    frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    frame.text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    self.mode = self.id_end
                    self.id_end += 1

    def paste_text3(self):
        text_obj = wx.TextDataObject()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                word = text_obj.GetText()
                whether_paste = self.count_word_length(word)
                if whether_paste:
                    word = self.reconstruct_word(word)
                    forecolor = wx.Colour(0, 0, 0)
                    backcolor = wx.Colour(255, 242, 204)
                    frame = TextFrame(self, self.id_end, word, forecolor, backcolor)
                    frame.Show(True)
                    self.Bind(wx.EVT_BUTTON,
                              lambda evt, mode=self.id_end: self.SwitchOnClick(evt, mode),
                              frame.text)
                    frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    frame.text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                    self.mode = self.id_end
                    self.id_end += 1

    def SwitchOnClick(self, event, mode):
        btn = wx.FindWindowById(mode)
        #self.panel.Bind(wx.EVT_MOUSE_EVENTS,
        #                lambda evt, mark=btn: self.dragEVT(evt, mark))
        self.mode = mode

    def dragEVT(self, event, mark):
        try:
            panel = mark
            if event.ButtonDown():
                panel.SetPosition(event.GetPosition())
            elif event.Dragging():
                panel.SetPosition(event.GetPosition())
            elif event.ButtonUp():
                panel.SetPosition(event.GetPosition())
        except:
            pass

    def OnClear(self, evt):
        self.clear_all()

    def clear_all(self):
        if self.mode != 'none':
            for i in range(self.id_start, self.id_end):
                try:
                    panel = wx.FindWindowById(i)
                    panel.Destroy()
                except:
                    pass
            self.id_start = 101
            self.id_end = 101
            self.bag_of_cpimages = {}
            self.bag_of_cpimsizes = {}
            self.mode = 'none'

    def OnCloseCurrent(self, evt):
        self.close_single()

    def close_single(self):
        if self.mode != 'none':
            panel = wx.FindWindowById(self.mode)
            panel.Destroy()

    def OnClose(self, evt):
        self.on_exit()

    def on_exit(self):
        dlg = wx.MessageDialog(None, 'Are you sure to quit?', 'Message', wx.YES_NO | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            self.tbIcon.Destroy()
            self.Destroy()

    def OnKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        print(keycode)
        if evt.ControlDown():
            if keycode == 49:
                self.paste_image()
                #elif self.mode == 'cp_tx1':
            elif keycode == 50:
                self.paste_text1()
                #elif self.mode == 'cp_tx2':
            elif keycode == 51:
                self.paste_text2()
                #elif self.mode == 'cp_tx3':
            elif keycode == 52:
                self.paste_text3()
            if keycode == ord('Z'):  # zoom in
                self.zoom_in()
            if keycode == ord('X'):  # zoom out
                self.zoom_out()
            if keycode == ord('D'):
                self.close_single()
            if keycode == ord('A'):
                self.close_all()

    def OnMouseWheel(self, evt):
        vector = evt.GetWheelRotation()
        print(vector)
        if vector > 0:
            self.zoom_in()
        elif vector < 0:
            self.zoom_out()

    def OnZoomIn(self, evt):
        self.zoom_in()

    def zoom_in(self):
        if self.mode != 'none':
            panel = wx.FindWindowById(self.mode)
            size = panel.GetSize()
            pos = panel.GetPosition()
            panel.zoom_in()

    def OnZoomOut(self, evt):
        self.zoom_out()

    def zoom_out(self):
        if self.mode != 'none':
            panel = wx.FindWindowById(self.mode)
            size = panel.GetSize()
            pos = panel.GetPosition()
            panel.zoom_out()

class SingleFrame(wx.Frame):
    def __init__(self, parent, id, im):
        wx.Frame.__init__(self, parent=parent, id=id,
                          style=wx.STAY_ON_TOP|wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_TOOL_WINDOW)
                          #style=wx.FRAME_SHAPED|wx.STAY_ON_TOP|wx.CAPTION|wx.CLOSE_BOX)
        self.parent = parent
        self.id = id
        self.img = im
        height = im.GetHeight()
        width = im.GetWidth()
        self.height = 256
        self.width = 256 / height * width
        bitmap = wx.Bitmap(self.img.Scale(self.height, self.width))
        #r = wx.Region(bitmap)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display = wx.BitmapButton(self, id+5000, bitmap, style=wx.NO_BORDER)

    def zoom_in(self):
        self.height *= 1.1
        self.width *= 1.1
        scaled_im = self.img.Scale(self.width, self.height)
        scaled_bmp = scaled_im.ConvertToBitmap()
        #r = wx.Region(scaled_bmp)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display.SetBitmap(wx.Bitmap(scaled_bmp))

    def zoom_out(self):
        self.height *= 0.9
        self.width *= 0.9
        scaled_im = self.img.Scale(self.width, self.height)
        scaled_bmp = scaled_im.ConvertToBitmap()
        #r = wx.Region(scaled_bmp)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display.SetBitmap(wx.Bitmap(scaled_bmp))

class EmojiFrame(wx.Frame):
    def __init__(self, parent, id, im):
        wx.Frame.__init__(self, parent=parent, id=id,
                          style=wx.STAY_ON_TOP|wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_TOOL_WINDOW)
                          #style=wx.FRAME_SHAPED|wx.STAY_ON_TOP|wx.CAPTION|wx.CLOSE_BOX)
        self.SetBackgroundColour(wx.WHITE)
        self.parent = parent
        self.id = id
        self.img = im
        self.height = 64
        self.width = 64
        bitmap = wx.Bitmap(self.img.Scale(self.width, self.height))
        #r = wx.Region(bitmap)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display = wx.BitmapButton(self, id+5000, bitmap, style=wx.NO_BORDER)

    def zoom_in(self):
        self.height *= 1.1
        self.width *= 1.1
        scaled_im = self.img.Scale(self.width, self.height)
        scaled_bmp = scaled_im.ConvertToBitmap()
        #r = wx.Region(scaled_bmp)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display.SetBitmap(wx.Bitmap(scaled_bmp))

    def zoom_out(self):
        self.height *= 0.9
        self.width *= 0.9
        scaled_im = self.img.Scale(self.width, self.height)
        scaled_bmp = scaled_im.ConvertToBitmap()
        #r = wx.Region(scaled_bmp)
        #self.SetShape(r)
        self.SetSize((self.width+16, self.height+39))
        self.display.SetBitmap(wx.Bitmap(scaled_bmp))

class TextFrame(wx.Frame):
    def __init__(self, parent, id, word, forecolor, backcolor):
        wx.Frame.__init__(self, parent=parent, id=id,
                          style=wx.STAY_ON_TOP | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_TOOL_WINDOW)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.size = 256
        self.SetSize((self.size+16, self.size+39))
        self.parent = parent
        self.id = id
        self.text_size = 15
        self.text = wx.Button(self, id=id, label=word, size=[self.size, self.size], style=wx.NO_BORDER)
        self.fontname = '微软雅黑'
        font = wx.Font(pointSize=self.text_size, family=wx.DECORATIVE, style=wx.NORMAL,
                       weight=wx.NORMAL, underline=False, faceName=self.fontname)
        self.text.SetFont(font)
        self.text.SetForegroundColour(forecolor)
        self.text.SetBackgroundColour(backcolor)

    def zoom_in(self):
        self.text_size += 1
        self.size *= 1.1
        font = wx.Font(pointSize=self.text_size, family=wx.DECORATIVE, style=wx.NORMAL,
                       weight=wx.NORMAL, underline=False, faceName=self.fontname)
        self.text.SetFont(font)
        self.SetSize((int(self.size)+16, int(self.size)+39))

    def zoom_out(self):
        self.text_size -= 1
        self.size *= 0.9
        font = wx.Font(pointSize=self.text_size, family=wx.DECORATIVE, style=wx.NORMAL,
                       weight=wx.NORMAL, underline=False, faceName=self.fontname)
        self.text.SetFont(font)
        self.SetSize((int(self.size)+16, int(self.size)+39))


def create_menu_item(menu, id, label, func):
    item = wx.MenuItem(menu, id, label)
    menu.Bind(wx.EVT_MENU, func, item)
    menu.Append(item)
    return item

class CustomTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        #self.SetIcon(icon)
        self.SetIcon(icon, "Interactive Sticker")

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 50, 'Paste Image (Ctrl+1)', self.copy_image0)
        create_menu_item(menu, 51, 'Paste Text1 (Ctrl+2)', self.copy_text10)
        create_menu_item(menu, 52, 'Paste Text2 (Ctrl+3)', self.copy_text20)
        create_menu_item(menu, 53, 'Paste Text3 (ctrl+4)', self.copy_text30)
        menu.AppendSeparator()
        #create_menu_item(menu, 55, 'Paste (Ctrl+V)', self.paste0)
        create_menu_item(menu, 56, 'Zoom In (Ctrl+Z)', self.zoom_in0)
        create_menu_item(menu, 57, 'Zoom Out (Ctrl+X)', self.zoom_out0)
        create_menu_item(menu, 58, 'Close Single (Ctrl+D)', self.close0)
        create_menu_item(menu, 59, 'Clear All (Ctrl+A)', self.clear0)
        menu.AppendSeparator()
        create_menu_item(menu, 54, 'Input Emoji Unicode', self.input_emoji)
        create_menu_item(menu, 61, 'Exit', self.on_exit0)
        return menu

    def copy_image0(self, evt):
        #btn = wx.FindWindowById(1)
        #for button in self.parent.bag_of_buttons:
        #    button.SetValue(False)
        #btn.SetValue(True)
        #self.parent.mode = self.parent.dict_of_modes[btn]
        self.parent.paste_image()

    def copy_text10(self, evt):
        #btn = wx.FindWindowById(2)
        #for button in self.parent.bag_of_buttons:
        #    button.SetValue(False)
        #btn.SetValue(True)
        #self.parent.mode = self.parent.dict_of_modes[btn]
        self.parent.paste_text1()

    def copy_text20(self, evt):
        #btn = wx.FindWindowById(3)
        #for button in self.parent.bag_of_buttons:
        #    button.SetValue(False)
        #btn.SetValue(True)
        #self.parent.mode = self.parent.dict_of_modes[btn]
        self.parent.paste_text2()

    def copy_text30(self, evt):
        #btn = wx.FindWindowById(4)
        #for button in self.parent.bag_of_buttons:
        #    button.SetValue(False)
        #btn.SetValue(True)
        #self.parent.mode = self.parent.dict_of_modes[btn]
        self.parent.paste_text3()

    def input_emoji(self, evt):
        dlg = wx.TextEntryDialog(None, "Please input an emoji unicode", "Emoji Input Window", "1f600")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue().lower()
            self.parent.add_emoji(message)
            #self.parent.paste_emoji(message)

    def paste0(self, evt):
        if self.parent.mode == 'cp_im':
            self.parent.paste_image()
        elif self.parent.mode == 'cp_tx1':
            self.parent.paste_text1()
        elif self.parent.mode == 'cp_tx2':
            self.parent.paste_text2()
        elif self.parent.mode == 'cp_tx3':
            self.parent.paste_text3()

    def zoom_in0(self, evt):
        self.parent.zoom_in()

    def zoom_out0(self, evt):
        self.parent.zoom_out()

    def close0(self, evt):
        self.parent.close_single()

    def clear0(self, evt):
        self.parent.clear_all()

    def on_exit0(self, evt):
        self.parent.on_exit()
        self.Destroy()
