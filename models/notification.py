from typing import Callable
from schedule import Job
import schedule
import winotify
from winotify import Notification as WinNotification, Registry, Notifier
import jobs.job_notification as jobs
from utils.globals_var import USER_ICONS_PATH
import os

registry = Registry(app_id="aaaa", script_path=__file__)
notifier = Notifier(registry)

class Notification:
    def __init__(self, time: int, title: str, message: str, icon: str = None, repeat=True, actions: list[dict]= None):
        """_summary_

        Args:
            time (int): _description_
            title (str): _description_
            message (str): _description_
            icon (str, optional): _description_. Defaults to None.
            repeat (bool, optional): _description_. Defaults to True.
        """
        self.time = time  # Cada cuanto, se guarda en segundos
        self.title = title
        self.message = message
        self.icon = icon
        self.repeat = repeat
        self.actions = actions
        self.job: Job = None
    
    def show_notify(self):
        icon = (
            USER_ICONS_PATH.joinpath(self.icon)
            if self.icon
            and os.path.exists(USER_ICONS_PATH.joinpath(self.icon))
            else ""
        )

        toast = WinNotification(
            app_id="Mis recordatorios",
            title=self.title,
            msg=self.message,
            icon=icon,
            # duration="",
            launch=""
        )

        if self.actions:
            for action in self.actions:
                label = action.get("label", None)
                launch = action.get("launch", None)
                if not label or not launch:
                    raise KeyError("Ey, como que faltan ")
                
                toast.add_actions(label=label, launch=launch)
        
        toast.set_audio(winotify.audio.Default, loop=False)
        
        toast.show()

        if not self.repeat:
            jobs.delete_job(self)
            return schedule.CancelJob
    
    @notifier.register_callback
    def call_back_url(self, url):
        pass
    
    def __str__(self):
        return f"{self.title} -> {self.message} cada {self.time}"

if __name__ == "__main__":
    pass
