import os
import time

import requests
import json
from django.contrib.auth.models import User
from . import models


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
        print(response.request.url)
        print(response.request.headers)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        # return response.json()
        response_json = json.dumps(response.json(), indent=4, sort_keys=True)
        with open('response.txt', 'w') as handle:
            handle.write(response_json)
            handle.write('===========================================')
            handle.write('\n')
        return response

    def do_request(self):

        job = models.Job.objects.order_by('priority')[0]

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
            JobService.delete(job.id)
        else:
            return 'For now the requests are not working'
    def schedule_request(params, user):
        num_request_with_max_results = int(params['num_tw']) // 180
        rest_request = int(params['num_tw']) % 180

        for i in range(num_request_with_max_results):
            job = JobService.instance_job_without_results(params, user)
            job.num_tw = 180
            JobService.create(job)
            # time.sleep((15 * 60) + 1)

        job_rest = JobService.instance_job_without_results(params, user)
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