from django.shortcuts import render
from django.views.generic import TemplateView
from .service import ApiService
from django.views import generic
from django.views import View
from . import forms
import requests
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class GetAPIData(TemplateView):
    template_name = 'data_view.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        '''quey for twitter'''
        fields = 'created_at,public_metrics,attachments,entities,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source,withheld'
        query_params = {'query': '(spain) lang:es', 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': fields,
                        'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
                        'max_results': 200}
        context = {
            'data': ApiService.schedule_request(query_params, user),
        }
        return context


@method_decorator(login_required, name='dispatch')
class GetForm(generic.FormView):
    template_name = 'request_form.html'
    form_class = forms.APIForm

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        lang = 'lang:' + data['lang']
        country = 'country:' + data['country']
        source = 'source,' if data['source'] else ''
        referenced_tweets = 'referenced_tweets,' if data['referenced_tweets'] else ''
        num_tw = data['num_tw']
        priority = data['priority']
        query = '(' + data['term'] + ')' + lang

        place_info = 'contained_within,country,country_code,full_name,geo,id,name,place_type' if data['place'] else ''
        fields = 'created_at,public_metrics,attachments,entities,in_reply_to_user_id,lang,possibly_sensitive,' + referenced_tweets + source + 'withheld'
        query_params = {'query': query,
                        # entity:"estados unidos"' adicionar para saber a que lugar o persona hace referencia el tweet
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': fields,
                        'place.fields': place_info,
                        'max_results': num_tw}
        api_data = ApiService.schedule_request(data, user)
        print(data)
        return redirect('success')


class Success(generic.TemplateView):
    template_name = 'success_form.html'
