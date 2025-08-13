import asyncio
import threading
import schedule
import sys
from UI import App
from jobs.job_notification import *
from pystray import Icon as TrayIcon, MenuItem as TrayMenuItem
from PIL import Image
from models.notification import Notification
from utils.globals_var import APP_ICONS_PATH
from customtkinter import CTk


class SystemTray:
    def __init__(self, app: CTk):
        self.app = app
        self.icon = TrayIcon(
            "Centro de Notificaciones",
            Image.open(APP_ICONS_PATH.joinpath("noti_ico.png")),
            "Centro Notificaciones",
            (
                TrayMenuItem("Mostrar", self.show_window, default=True, visible=False),
                TrayMenuItem("Salir", self.quit_app),
            ),
        )

    def show_window(self, icon, item):
        self.icon.visible = False
        self.app.after(0, self.app.deiconify)

    def quit_app(self, icon, item):
        self.icon.stop()
        self.app.quit()
        sys.exit()

    def hide_window(self):
        self.app.withdraw()

        Notification(
            time=1,
            title="App en segundo plano",
            message="La app se encuentra corriendo en segundo plano. Para volver a ver la interfaz usa tu menú de apps!",
        ).show_notify()

        threading.Thread(target=self.icon.run, daemon=True).start()


# Async scheduler loop
async def run_async_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

def main():
    app = App()
    app.grid_columnconfigure(0, weight=1)
    
    threading.Thread(
        target=lambda: asyncio.run(run_async_schedule()), daemon=True
    ).start()

    tray = SystemTray(app)

    app.wm_protocol("WM_DELETE_WINDOW", tray.hide_window)

    app.mainloop()


def test_notifications():

    for i in range(5):
        create_job(
            Notification(
                time=20 * (i + 1),
                title=f"Numero {i + 1}",
                message=f"Probando notificaciones asd s {i + 1}.",
                icon="default.png",
                repeat=True,
            )
        )


if __name__ == "__main__":
    if "-noti" in sys.argv or "--notifications" in sys.argv:
        test_notifications()
    
    main()
