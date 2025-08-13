from PIL import Image
import customtkinter as ctk
from UI.icons_scroll_frame import IconsFrame
from UI.search_icon_frame import SearchIconFrame
from UI.second_view import SecondWindow
from jobs.job_error import JobCreationError
from jobs.job_notification import create_job
from models.notification import Notification
from utils.globals_var import APP_ICONS_PATH
from asyncio import sleep

class FormView(ctk.CTkFrame):

    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        
        # Titulo :smile:
        ctk.CTkLabel(self, text="Formulario de Recordatorios", font=("Arial", 20, "bold")) \
        .grid(row=0, column=0, columnspan=2, pady=(20, 0), padx=(45, 0), sticky="we")
        
        # Label para errores  text_color="red
        self.lbl_message = ctk.CTkLabel(self, width=200, text="", wraplength=150, justify="left", text_color="white", 
                                        fg_color="transparent", corner_radius=10)
        self.lbl_message.grid(row=1, column=1, pady=(20, 0))
        
        # Inputs and error message
        self.in_title = ctk.CTkEntry(self, placeholder_text="Titulo")
        self.in_title.grid(row=1, column=0, pady=(20, 0), padx=(20, 0), sticky="w")
        self.title_error = ctk.CTkLabel(self, text="", height=5, text_color="red")
        self.title_error.grid(row=1, column=0, pady=(65, 0), padx=(30, 0), sticky="w")
        
        # 
        self.in_message = ctk.CTkEntry(self, placeholder_text="Mensaje",)
        self.in_message.grid(row=2, column=0, pady=(5, 0), padx=(20, 0), sticky="nw")
        self.message_error = ctk.CTkLabel(self, text="", height=5, text_color="red")
        self.message_error.grid(row=2, column=0, pady=(35, 0), padx=(30, 0), sticky="nw")
        
        # Icono
        self.my_image = ctk.CTkImage(light_image=Image.open(APP_ICONS_PATH.joinpath("default.png")), size=(80, 80))
        self.image_button = ctk.CTkButton(self, width = 80, image=self.my_image, text="", command=self.show_icons_view, fg_color="transparent")
        self.image_button.grid(row=3, column=0, sticky="w", padx=(20, 0), pady=(5, 5))
       
        # Time
        self.options = {"Segundos": 1, "Minutos": 60, "Horas": 3600, "Dias": 86400, "Mes": 2592000}

        self.countdown = ctk.CTkEntry(self, placeholder_text="Intervalo",)
        self.countdown.grid(row=4, column=0, padx=(20, 0), sticky="nw")
        self.countdown_error = ctk.CTkLabel(self, text="", height=5, text_color="red")
        self.countdown_error.grid(row=4, column=0, pady=(30, 0), padx=(30, 0), sticky="nw")
        
        self.countdown_option = ctk.CTkOptionMenu(self, values=list(self.options.keys()), width=100)
        self.countdown_option.grid(row=4, column=0, columnspan=2, padx=(170, 0), pady=(0, 0), sticky="nw",)

        # Repetir
        self.check = ctk.CTkCheckBox(self, text="¿Notificación recurrente?",)
        self.check.grid(row=5, column=0, pady=(10, 0), padx=(20, 0), sticky="w")

        # Crear
        btn_create_noti = ctk.CTkButton(self, text=f"Crear recordatorio", command=self.validate_inputs)
        btn_create_noti.grid(row=6, column=0, columnspan=2, padx=(30, 0), pady=(10, 10))

        # Variables de control
        self.popup = None 
        self.in_icon_name = None

    def change_temp_icon(self, icon_name=APP_ICONS_PATH.joinpath("default.png")):
        self.in_icon_name = icon_name
        self.my_image.configure(light_image=Image.open(icon_name))

    def show_icons_view(self):
        if self.popup is None or not self.popup.winfo_exists():
            frames = [{"frame_obj": IconsFrame, "options": {"row":0, "column":0, "padx":10, "pady":(10, 0),"sticky":"nsew"}},
                    {"frame_obj": SearchIconFrame, "options": {"row":3, "column":0, "padx":10, "pady":(10, 0),"sticky":"nsew"}}
                      ]
            
            self.popup = SecondWindow(self, frames=frames)
            self.popup.lift()
            self.popup.focus_force()
            self.popup.attributes("-topmost", True)
        else:
            self.popup.focus()

    def validate_inputs(self):
        self.clean_messages()
        errors = False
        title = self.in_title.get()
        message = self.in_message.get()
        icon_path = self.in_icon_name if self.in_icon_name and self.in_icon_name!= "default.png" else None
        
        if not title or title.isspace():
            errors = True
            self.title_error.configure(text="* Campo requerido.")
        
        if not message or title.isspace():
            errors = True
            self.message_error.configure(text="* Campo requerido.")
    
        try:
            input_time = int(self.countdown.get())
            type_time = self.options.get(self.countdown_option.get(), None)
            
            if input_time <= 0 or not input_time:
                errors = True
                self.countdown_error.configure(text="* Debe ser mayor o igual a 1")
            total_seconds = input_time * type_time      
            if total_seconds > 2592000:
                self.countdown_error.configure(text="* Max permitido 1 Mes")
                errors = True
        except ValueError:
            self.countdown_error.configure(text="* Solo numeros mayores a 0")
            errors = True
        
        if errors:
            return
        self.create_notifications(total_seconds, title, message, icon_path)
    
    def create_notifications(self, total_seconds, title, mensaje, icon_path):
        try:
            create_job(Notification(total_seconds, title, mensaje, icon_path, self.check.get()))
        except JobCreationError as e:
            self.countdown_error.configure(text="* Numero muy grande")
            return
        except Exception as e:
            print("Error inesperado al crear la notificación:", e)
            return
        
        self.set_message("✅ Notificacion creada!")
        self.clean_inputs()

    def clean_inputs(self):
        self.in_title.delete(0, ctk.END)
        self.in_message.delete(0, ctk.END)
        self.countdown.delete(0, ctk.END)
        self.check.deselect()
        self.change_temp_icon()

    def clean_messages(self):
        self.title_error.configure(text="")
        self.message_error.configure(text="")
        self.countdown_error.configure(text="")

    def set_message(self, msg: str):
        self.lbl_message.configure(text=msg, fg_color="green4")
        self.after(3500, lambda: self.lbl_message.configure(text="", fg_color="transparent"))
