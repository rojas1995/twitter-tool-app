from api import models
from api import service


def scheduled_job():
    job = service.JobService.get_next_job()
    message = service.ApiService.do_request(job)
    service.PubService().create_topic()
    service.PubService().publish(message)

