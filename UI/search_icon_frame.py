import os
import shutil
from time import time
import customtkinter as ctk
from utils.globals_var import USER_ICONS_PATH

class SearchIconFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.master_ = master
        self.icons_frame = kwargs.get("icon_frame", None)
        
        btn_image = ctk.CTkButton(self, text=f"Buscar imagen", command=self.search_image)
        btn_image.grid(row=3, column=0)
    
    def search_image(self):
        icon = ctk.filedialog.askopenfile(filetypes=[('Imagenes','*.jpg *.jpeg *.png')])

        if not icon:
            return
        
        icon.close()

        file_name = os.path.basename(icon.name)
        
        file_name, extension = os.path.splitext(file_name) 
        file_name += str(time()) + extension
        self.in_icon_name = file_name
        final_path = USER_ICONS_PATH.joinpath(file_name)
        shutil.copyfile(icon.name, final_path)
        self.re_draw_icons(file_name)
    
    def re_draw_icons(self, file_name):
        icon_frame = self.master_.frames.get("IconsFrame")
        icon_frame.show_icons()
        icon_frame.select_icon_master(USER_ICONS_PATH.joinpath(file_name))
