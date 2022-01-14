#!/usr/bin/env python
# -- coding: utf-8 --

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from threading import Timer
#from kivymd.button import MDRaisedButton, MDIconButton, MDFlatButton, MDRectangleFlatIconButton, MDRoundFlatIconButton
import os
import subprocess
import jnius
from jnius import cast
from jnius import autoclass
import time
import paramiko
import cryptography
import bcrypt

#-----------------------------------------------------------------------
varstate = 0
varstateone = 0
progressval = 0
varprog = 0
vardoor = 0

#-----------------------------------------------------------------------

class CircularProgressBar(ProgressBar, FloatLayout):
    def _init_(self,**kwargs):
        super(CircularProgressBar,self)._init_(**kwargs)
        self.thickness = 70
        self.label = CoreLabel(text="0", font_size=self.thickness)
        self.texture_size = None
        self.refresh_text()
        self.draw()
    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.26,0.26,0.26)
            Ellipse(pos=self.pos, size=self.size)
            Color(1,0,0)
            Ellipse(pos=self.pos,size=self.size,angle_end=(self.value/100.0)*360)
            Color(0,0,0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            Color(1, 1, 1, 1)
            #Rectangle(texture=self._text_label.texture, size=self._label_size, pos=(self._widget_size / 2 - self._label_size[0] / 2 + self.pos[0], self._widget_size / 2 - self._label_size[1] / 2 + self.pos[1]))
            Rectangle(texture=self.label.texture,size=self.texture_size,pos=(self.pos[0]-self.texture_size[0],self.center[1] - self.texture_size[1]/2))
            self.label.text = str(int(self.value))

    def refresh_text(self):
        self.label.refresh()
        self.texture_size=list(self.label.texture.size)
    def set_value(self, value):
        self.value = value
        self.label.text = str(int(self.value))
        self.refresh_text()
        self.draw()

#-----------------------------------------------------------------------

class PopUpScreen(Screen, Widget):
    
    def show_popup_open(self):
        show = P1()
        popupWindow1 = Popup(
            title="Popup Window", content=show,
            size_hint=(None,None), size=(400,400))
        popupWindow1.open()

    def show_popup_close(self):
        show = P2()
        popupWindow2 = Popup(
            title="Popup Window", content=show,
            size_hint=(None,None), size=(400,400))
        popupWindow2.open()

    def show_popup_connect(self):
        show = P3()
        popupWindow3 = Popup(
            title="Popup Window", content=show,
            size_hint=(None, None), size=(400,400))
        popupWindow3.open()

    def open_instruc(self):
        show = P4()
        popupWindow4 = Popup(
            title="Popup Window", content=show,
            size_hint=(None, None), size=(400,400))
        popupWindow4.open(self)
    
    def close_instruc(self):
        show = P5()
        popupWindow5 = Popup(
            title="Popup Window", content=show,
            size_hint=(None, None), size=(400,400))
        popupWindow5.open()

    def notif(self):
        show = P6()
        popupWindow6 = Popup(
            title="Popup Window", content=show,
            size_hint=(None, None), size=(400,400))
        popupWindow6.open()

#-----------------------------------------------------------------------

class MainWindow(Screen, Widget):

    def btnconnect(self):
        show_popup_connect()

    def btn1(self):
        global varstate
        global varstateone
        if varstate == 0:
            if varstateone == 0:
                varstateone = varstateone + 1
                openmotors()
                #timermotors()
            else:
                pass
        else:
            pass

    def btn2(self):
        global varstate
        global varstateone
        if varstateone == 1:
            varstate = varstate + 1
            print(varstate)
            if varstate == 1:
                closemotors()
            else:
                pass
        else:
            pass

#-----------------------------------------------------------------------

class WindowManager(ScreenManager):
    pass

#-----------------------------------------------------------------------

def openmotors():
    sm.current = "popupscreen"
    t = Timer(5.0, open_instruc)
    t.start()
    
    t = Timer(10.0, ssh_notif)
    t.start()

def closemotors():
    sm.current = "popupscreen"
    t = Timer(5.0, close_instruc)
    t.start()
    t = Timer(10.0, ssh_notif_close)
    t.start()
    
def screenchange():
    sm.current = "popupscreen"    
    
def screenchangemain():
    sm.current = "main"

def screenchangemaindos():
    global varprog
    varprog = 1
    sm.current = "main"
    

def stop():
    screenchange()
    t = Timer(45.0, show_popup_open)
    t.start()
    resetvarprog()
    t = Timer(50.0, screenchangemain)
    t.start()


def varchangeprog():
    screenchange()
    t = Timer(45.0, show_popup_close)
    t.start()
    resetvarprog()
    t = Timer(50.0, screenchangemaindos)
    t.start()
    
    
def ssh_notif():
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    pm = autoclass('android.content.pm.PackageManager')
    activity = PythonActivity.mActivity
    pm_ = activity.getPackageManager()
    array_pkg = pm_.getInstalledApplications(pm.GET_META_DATA).toArray()
    selected_pkg = []
    list_existing = []
    for i in array_pkg:
        if "/data/app/" not in getattr(i, "publicSourceDir"):
            continue

        selected_pkg.append(i)
        list_existing.append(getattr(i, "packageName"))
    app_to_launch = "com.termux"	
    for i in selected_pkg:    
        if app_to_launch == getattr(i, "packageName"):
            app_intent = pm_.getLaunchIntentForPackage(getattr(i, "packageName"))
            app_intent.setAction(Intent.ACTION_VIEW)
            app_intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            activity.startActivity(app_intent)
    
    
    global varprog
    varprog = 2
    sm.current = "main"
    
def ssh_notif_close():
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    pm = autoclass('android.content.pm.PackageManager')
    activity = PythonActivity.mActivity
    pm_ = activity.getPackageManager()
    array_pkg = pm_.getInstalledApplications(pm.GET_META_DATA).toArray()
    selected_pkg = []
    list_existing = []
    for i in array_pkg:
        if "/data/app/" not in getattr(i, "publicSourceDir"):
            continue
        selected_pkg.append(i)
        list_existing.append(getattr(i, "packageName"))
    app_to_launch = "com.termux"	
    for i in selected_pkg:    
        if app_to_launch == getattr(i, "packageName"):
            app_intent = pm_.getLaunchIntentForPackage(getattr(i, "packageName"))
            app_intent.setAction(Intent.ACTION_VIEW)
            app_intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            activity.startActivity(app_intent)
    #t = Timer(45.0, varchangeprog)
    #t.start()

    global varprog
    varprog = 3
    sm.current = "main"
    
def finishedCicle():
    pop = Popup(title='Cicle finished',
                    content=Label(text='You can now open the door.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

def resetvar():
    global varstate
    global varstateone
    global progressval
    varstate = 0
    varstateone = 0
    progressval = 0
    
def resetvarprog():
    global varprog
    varprog = 0

#-----------------------------------------------------------------------

kv = Builder.load_file("main.kv")
sm = WindowManager()
screens = [MainWindow(name="main"), PopUpScreen(name="popupscreen")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

#-----------------------------------------------------------------------

class P1(FloatLayout):
    pass

#-----------------------------------------------------------------------

class P2(FloatLayout):
    pass

#-----------------------------------------------------------------------

class P3(FloatLayout):
    pass

#-----------------------------------------------------------------------

class P4(FloatLayout):
    pass

#-----------------------------------------------------------------------

class P5(FloatLayout):
    pass
    
#-----------------------------------------------------------------------

class P6(FloatLayout):
    pass

#-----------------------------------------------------------------------

class Main(App, FloatLayout):
                                                                                
    def animate(self,dt):
        global progressval
        global varprog
        
        circProgressBar = self.root.get_screen('main').ids.cp
        if varprog == 1:
            #stop_close()
            circProgressBar.set_value(circProgressBar.value+1)
            progressval = 1
            if circProgressBar.value == 100:
                resetvar()
                resetvarprog()
                finishedCicle()
                #stop_close()
                #sm.current = "popupscreen"
            else:
                pass
        elif varprog == 2:
            stop()
            #t = Timer(45.0, stop)
            #t.start()
            resetvarprog()
            circProgressBar.set_value(0)
        elif varprog == 3:
            varchangeprog()
            resetvarprog()
            circProgressBar.set_value(0)
        else:
            circProgressBar.set_value(0)

    def build(self):
        Clock.schedule_interval(self.animate, 0.015) 
        
        return sm
    
#-----------------------------------------------------------------------

def show_popup_open():
    show = P1()
    popupWindow1 = Popup(
        title="Popup Window", content=show,
        size_hint=(None,None), size=(400,400))
    popupWindow1.open()
    t = Timer(45.0, screenchangemain)
    t.start()
    
    

def show_popup_close():
    show = P2()
    popupWindow2 = Popup(
        title="Popup Window", content=show,
        size_hint=(None,None), size=(400,400))
    popupWindow2.open()

def show_popup_connect():
    show = P3()
    popupWindow3 = Popup(
        title="Popup Window", content=show,
        size_hint=(None, None), size=(400,400))
    popupWindow3.open()

def open_instruc():
    show = P4()
    popupWindow4 = Popup(
        title="Popup Window", content=show,
        size_hint=(None, None), size=(400,400))
    popupWindow4.open()
    
def close_instruc():
    show = P5()
    popupWindow5 = Popup(
        title="Popup Window", content=show,
        size_hint=(None, None), size=(400,400))
    popupWindow5.open()

def notif():
    show = P6()
    popupWindow6 = Popup(
        title="Popup Window", content=show,
        size_hint=(None, None), size=(400,400))
    popupWindow6.open()


#-----------------------------------------------------------------------

if _name_ == "_main_":
    Main().run()
