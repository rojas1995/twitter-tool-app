import os
import time

import requests
import json
from django.contrib.auth.models import User
from . import models
from google import pubsub_v1


class ApiService():
    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {os.getenv('BEARER_TOKEN')}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def get_data(params):
        url = "https://api.twitter.com/2/tweets/search/recent"

        response = requests.get(url, auth=ApiService.bearer_oauth, params=params)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        ''' write response json on file to debug'''
        response_json = json.dumps(response.json(), indent=4, sort_keys=True)
        
        with open('response.txt', 'w') as handle:
            handle.write(response_json)
            handle.write('===========================================')
            handle.write('\n')
        return response

    def do_request(job):

        lang = 'lang:' + job.lang
        country = 'country:' + job.country
        source = 'source,' if job.source else ''
        referenced_tweets = 'referenced_tweets,' if job.referenced_tweets else ''
        num_tw = job.num_tw
        query = '(' + job.term + ')' + lang
        place_info = 'contained_within,country,country_code,full_name,geo,id,name,place_type' if job.place else ''
        fields = 'created_at,public_metrics,attachments,entities,in_reply_to_user_id,lang,possibly_sensitive,' + referenced_tweets + source + 'withheld'

        query_params = {'query': query,
                        # entity:"estados unidos"' adicionar para saber a que lugar o persona hace referencia el tweet
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': fields,
                        'place.fields': place_info,
                        'max_results': num_tw}

        response = ApiService.get_data(query_params)
        if response.status_code == 200:
            LoggingService.update_job_log(job, True)
            JobService.delete(job.id)
            return response.json()

        else:
            LoggingService.update_job_log(job, False)

    def schedule_request(params, user):
        num_request_with_max_results = int(params['num_tw']) // 100
        rest_request = int(params['num_tw']) % 100
        for i in range(num_request_with_max_results):
            job = JobService.instance_job_without_results(params, user)
            job.num_tw = 100
            JobService.create(job)

        if rest_request !=0:
            job_rest = JobService.instance_job_without_results(params, user)
            job_rest.num_tw = rest_request
            JobService.create(job_rest)
    def schedule_request_job(job):
        print(job.num_tw)
        num_request_with_max_results = int(job.num_tw) // 100
        rest_request = int(job.num_tw) % 100
        for i in range(num_request_with_max_results):
            job_aux = models.Job(user=job.user, term=job.term, country=job.country, lang=job.lang,
                         place=job.place, priority=job.priority,
                         referenced_tweets=job.referenced_tweets, source=job.source)
            job_aux.num_tw = 100
            JobService.create(job_aux)

        if rest_request !=0:
            job_rest = models.Job(user=job.user, term=job.term, country=job.country, lang=job.lang,
                         place=job.place, priority=job.priority,
                         referenced_tweets=job.referenced_tweets, source=job.source)
            job_rest.num_tw = rest_request
            JobService.create(job_rest)



class JobService():
    def create(job: models.Job):
        job.full_clean()
        job.save()


    def instance_job_without_results(params, user):
        job = models.Job(user=user, term=params['term'], country=params['country'], lang=params['lang'],
                         place=params['place'], priority=params['priority'],
                         referenced_tweets=params['referenced_tweets'], source=params['source'])
        return job

    def delete(id):
        job = models.Job.objects.get(id=id)
        job.full_clean()
        job.delete()

    def get_next_job():
        job = models.Job.objects.order_by('priority', 'create_at').first()
        return job


class LoggingService():

    def update_job_log(job: models.Job, success):
        log = models.JobLog(user=job.user, term=job.term, country=job.country, lang=job.lang,
                            place=job.place, priority=job.priority,
                            referenced_tweets=job.referenced_tweets, source=job.source, job_id=job.id,
                            execution_success=success, num_tw=job.num_tw, create_at=job.create_at)

        LoggingService.create(log)

    def create(log: models.JobLog):
        log.full_clean()
        log.save()


class PubSubService():

    def create_topic():
        project_id = os.getenv('APPLICATION_ID')
        print("project_id: "+project_id)
        publisher = pubsub_v1.PublisherClient()
        project_path = f"projects/{project_id}"
        exists = False
        for topic in publisher.list_topics(request={"project": project_path}):
            print(topic)
            if topic.name == 'twitter_messages':
                exists = True

        if not exists:
            topic_path = publisher.topic_path(project_id, 'twitter_messages')
            topic = publisher.create_topic(request={"name": topic_path})
            #print(f"created topic: "+topic.name)

    def publish(message):
        project_id = os.getenv('APPLICATION_ID')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, 'twitter_messages')
        future = publisher.publish(topic_path, message)
        #print("messages published: "+future.result())

