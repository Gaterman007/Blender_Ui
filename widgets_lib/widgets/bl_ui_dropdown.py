import os

import blf
import bpy
import gpu

from .bl_ui_widget import BL_UI_Widget
from .bl_ui_label import BL_UI_Label
from .bl_ui_button import BL_UI_Button

class BL_UI_DropDown(BL_UI_Label):
    def __init__(self, *args , **kwargs):
        super().__init__( *args , **kwargs)
        self.className = "DropDown"
        self.__state = 0
        self.__opClass = None
        self.index = None
        self.type = None
        self.items = None
        self.itemSelected = None
        self.newbuttons = None
        self.childHeight = 24
        
    def set_propinfo(self,prop_info):
        super().set_propinfo(prop_info)
        if self.prop_info is not None:
            if 'items' in prop_info.keywords:
                self.items = prop_info.keywords['items']
                listDropDown = [item[1] for item in self.items]
                if len(listDropDown) > 0:
                    self.newbuttons = []
                    y2 = 20
                    data = 0
                    for text in listDropDown:
                        newbutton = BL_UI_Button(self.width + 10, y2, self.width, self.childHeight, text = text)
                        newbutton.setMouseClicCallBack(self.buttonClick,data)
                        self.newbuttons.append(newbutton)
                        newbutton.visible = False
                        self.add_widget(newbutton)
                        y2 += self.childHeight
                        data += 1
                if self.getter is not None:
                    self.itemSelected = self.getter(self.element)
                    result = next((item for item in self.items if item[-1] == self.itemSelected), None)
                    self._text = result[1]

    def buttonClick(self,data, context):
        self.showDropDown(False)
        self.itemSelected = data
        result = next((item for item in self.items if item[-1] == self.itemSelected), None)
        if self._text != result[1]:
            self._text = result[1]
        self.element.align = result[0]
        return ({"RUNNING_MODAL"},True)

    def draw(self,context):
        if not self._is_visible:
            return
        super().draw(context)
        
    def setOpClass(self,opClass):
        self.__opClass = opClass

    def setIndex(self,index):
        self.index = index
    
    def setType(self,type):
        self.type = type

    def is_in_rect(self, x, y):
        return BL_UI_Widget.is_in_rect(self,x, y)

    def mouse_down(self, x, y, context):
        if self.is_in_rect(x, y):
            self.__state = 1
            return ({"RUNNING_MODAL"},True)

        return ({"PASS_THROUGH"},False)

    def mouse_move(self, x, y, context):
        if self.is_in_rect(x, y):
            if self.__state != 1:
                # hover state
                self.__state = 2
        else:
            self.__state = 0
        return ({"PASS_THROUGH"},False)

    def showDropDown(self,show = True):
        if self.newbuttons is not None:
            for newbutton in self.newbuttons:
                newbutton.visible = show
            bpy.context.region.tag_redraw()
        

    def mouse_up(self, x, y, context):
        result = ({"PASS_THROUGH"},False)
        if self.is_in_rect(x, y):
            if self.__state == 1:
                # call drop down
                self.showDropDown(True)
            self.__state = 2
            return ({"RUNNING_MODAL"},True)
        else:
            self.__state = 0
        return result