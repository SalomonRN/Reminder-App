from jobs.job_error import JobCreationError
from models import Notification
import schedule
from utils.globals_var import NOTIFICATIONS

def get_jobs() -> list[Notification]:
    return NOTIFICATIONS

def create_job(notification: Notification):
    try:
        job = schedule.every(notification.time).seconds.do(notification.show_notify)
    except OverflowError as error:
        print(error)
        raise JobCreationError("Error al crear el job: " + str(error))
    
    notification.job = job
    NOTIFICATIONS.append(notification)

def edit_job():
    raise NotImplementedError()

def delete_job(notification: Notification):
    schedule.cancel_job(notification.job)
    try:
        NOTIFICATIONS.remove(notification)
    except Exception:
        pass
    

if __name__ == "__main__":
    pass
