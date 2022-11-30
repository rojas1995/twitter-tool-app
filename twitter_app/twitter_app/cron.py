from logging import log

from api import models
from api import service


def scheduled_job():
    i = 0
    for i in range(0,180):
        job = service.JobService.get_next_job()
        if job != None:
            print('existe')

            service.ApiService.do_request(job)
            '''service.PubService().create_topic()
            service.PubService().publish(message)'''
        else:
            print('no existe')
            break
