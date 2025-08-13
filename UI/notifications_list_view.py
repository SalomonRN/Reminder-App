from PIL import Image
import customtkinter as ctk
from models.notification import Notification
from jobs.job_notification import get_jobs, delete_job
from utils.globals_var import USER_ICONS_PATH, APP_ICONS_PATH

class NotificationsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.icons: ctk.CTkImage = []
        self.draw_notifications()

    def draw_notifications(self):
        notis = get_jobs()
        for key, noti in enumerate(notis):
            miniFrame = NotificationRow(self, noti)
            miniFrame.grid(row=key, column=1)

IMG_DELETE = ctk.CTkImage(Image.open(APP_ICONS_PATH.joinpath("delete.png")))

# INTENTA HACER ESTO PERO SIN CREAR UN OBJETO NotificationRow, a ver como es el rendimiento
class NotificationRow(ctk.CTkFrame):
    def __init__(self, master, notification: Notification, **kwargs):
        super().__init__(master)
        self.notification = notification

        self.grid_columnconfigure((1,2,3), weight=1)
        self.__post_init__()
    
    def __post_init__(self):
        icon_path = USER_ICONS_PATH.joinpath(self.notification.icon) if self.notification.icon else None
        if icon_path:
            img = Image.open(USER_ICONS_PATH.joinpath(icon_path))
            image = ctk.CTkLabel(self, image=ctk.CTkImage(light_image=img, size=(20, 20)), text="")
            image.grid(row=0, column=0, sticky="w", padx=(10,0))

        max_title_len = 10
        max_msg_len = 33

        title = self.notification.title
        message = self.notification.message

        short_title = title if len(title) <= max_title_len else title[:max_title_len - 3] + "..."
        short_msg = message if len(message) <= max_msg_len else message[:max_msg_len - 3] + "... "

        msg = f"{short_title} --- {short_msg}"
        
        lbl_title = ctk.CTkLabel(self, text=msg, anchor="w", width=250)  # Fija el ancho
        lbl_title.grid(row=0, column=1, padx=(15, 0), sticky="ew")
        
        btn_delete = ctk.CTkButton(self, text="", width=25, image=IMG_DELETE,
                                   command=lambda x=self.notification: self.delete_and_redraw(x))   
        btn_delete.grid(row=0, column=2, sticky="e", padx=(10, 0))

    def delete_and_redraw(self, notification: Notification):
        delete_job(notification)
        self.grid_forget()
