from django.shortcuts import render
from django.views.generic import TemplateView
from .service import get_data

class GetAPIData(TemplateView):

    template_name = 'data_view.html'

    def get_context_data(self, **kwargs):
        '''quey for twitter'''
        fields = 'created_at,public_metrics,attachments,entities,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source,withheld'
        query_params = {'query': 'spain', 'expansions': 'author_id,in_reply_to_user_id,geo.place_id', 'tweet.fields': fields, 'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type', 'max_results': 50}
        context = {
            'data': get_data(query_params),
        }
        return context
