from django.shortcuts import render
from django.views.generic import TemplateView
from .service import get_data

class GetAPIData(TemplateView):

    template_name = 'data_view.html'

    def get_context_data(self, **kwargs):
        '''quey for twitter'''
        fields = 'created_at,public_metrics,attachments,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source,withheld'
        query_params = {'query': 'elden', 'tweet.fields': fields, 'max_results': 10}
        context = {
            'data': get_data(query_params),
        }
        return context
