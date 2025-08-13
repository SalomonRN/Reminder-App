from UI.form_view import FormView
from models.notification import Notification
from .notifications_list_view import NotificationsFrame
from PIL import Image
import customtkinter as ctk
from utils.globals_var import APP_ICONS_PATH

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("🔔 Centro de Notificaciones")
        self.geometry("450x450")
        self.resizable(False, False)
        self.frame_obj: ctk.CTkFrame = None
        self.home()
    
    def home(self): 
        self.grid_rowconfigure((1,2,3,4,5,6), weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="Centro de Notificaciones", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky="e")
        
        self.btn_form = ctk.CTkButton(self, text="Crea tus recordatorios", command=lambda x=FormView: self.draw_frame(x))
        self.btn_form.grid(row=2, column=0, columnspan=3, padx=20)
        
        self.btn_list_jobs = ctk.CTkButton(self, text="Listado de Recordatorios", command=lambda x=NotificationsFrame: self.draw_frame(x))
        self.btn_list_jobs.grid(row=3, column=0, columnspan=3, padx=20)
        
        github_img = ctk.CTkImage(Image.open(APP_ICONS_PATH.joinpath(f"github_{ctk.get_appearance_mode().lower()}.png")))
        
        self.btn_github = ctk.CTkButton(self, width=100, text="GitHub", command=self.github_link, image=github_img, 
                                        fg_color="transparent", text_color="white" if ctk.get_appearance_mode()=="Dark" else "black", 
                                        hover_color="gray")
        
        self.btn_github.grid(row=6, column=2)
        
        if self.frame_obj:
            self.img_back.grid_forget()
            self.frame_obj.grid_forget()
    
    def draw_frame(self, new_frame: ctk.CTkFrame):

        img = ctk.CTkImage(light_image=Image.open(APP_ICONS_PATH.joinpath("back_dark.png")))
        self.img_back = ctk.CTkButton(self, width=50, image=img, fg_color="transparent", text="", command=self.home)
        self.img_back.grid(row=0, column=0, sticky="nw")
        
        if self.frame_obj and self.frame_obj == new_frame:
            self.frame_obj.grid(row=1, column=0, sticky="nsew")
            self.btn_form.destroy()
            return
        
        self.new_frame = new_frame(self)
        self.frame_obj = self.new_frame
        self.new_frame.grid(row=1, column=0, sticky="nsew")
    
        self.destroy_home()
    
    def github_link(self):
        noti = Notification(
            1,
            "GitHub",
            "Puedes observar y apoyar el proyecto en el repositorio en GitHub.",
            repeat=False,
            actions=[
                {
                    "label": "Abrir GitHub",
                    "launch": "https://github.com/SalomonRN/Reminder-App",
                }
            ],
        )
        noti.show_notify()

    def destroy_home(self):
        self.title_label.destroy()
        self.btn_form.destroy()
        self.btn_github.destroy()
        self.btn_list_jobs.destroy()

if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure((0,1,2,3,4), weight=1)
    app.mainloop()
