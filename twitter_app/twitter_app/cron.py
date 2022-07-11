from api import models
from api import service


def scheduled_job():
    job = service.JobService.get_next_job()
    service.ApiService.do_request(job)

