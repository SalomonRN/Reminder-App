import customtkinter as ctk
from utils.globals_var import USER_ICONS_PATH
from PIL import Image
import os

class IconsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, *args,**kwargs):
        self.masterr = master
        super().__init__(master)
        self.icons: ctk.CTkImage = []
        self.show_icons()
                
    def show_icons(self):
        EXTENSION = ('.jpg', '.jpeg', '.png')
        if self.icons:
            self.icons.clear()
        
        for file in os.listdir(USER_ICONS_PATH):
            if not file.lower().endswith(EXTENSION):
                continue
            self.icons.append(ctk.CTkImage(light_image=Image.open(USER_ICONS_PATH.joinpath(file)), size=(50, 50)))
        
        row = 0
        colum = 0
        temp_icon = None
        
        for icon in self.icons:
            image_label = ctk.CTkButton(self,width=50, height=50, image=icon, text="", fg_color="transparent", command=lambda i=icon: self.select_icon(i))
            if colum >= 5:
                colum = 0
                row+=1        
            
            image_label.grid(row=row, column=colum, padx=14, pady=(10, 0))
            
            colum+=1
            if colum >= 6:
                colum = 0
                row+=1

    def select_icon(self, image):
        self.select_icon_master(image.cget("light_image").filename)
        
    def select_icon_master(self, icon_name):   
        self.masterr.master_.change_temp_icon(icon_name)
        self.masterr.destroy()
