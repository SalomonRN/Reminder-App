import customtkinter as ctk

class SecondWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        self.master_ = master
        super().__init__(master)
        self.title(kwargs.get("title", "Ventana secundaria"))
        self.geometry(kwargs.get("size", "500x400"))
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3), weight=1)

        
        self.frames = {} 

        for frame_dict in kwargs.get("frames", None):
            FrameClass = frame_dict.get("frame_obj")
            options = frame_dict.get("options")

            frame_instance = FrameClass(self)
            frame_instance.grid(**options)
            self.frames[FrameClass.__name__] = frame_instance
