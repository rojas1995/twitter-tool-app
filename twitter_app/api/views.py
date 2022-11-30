from django.shortcuts import render
from django.views.generic import TemplateView
from .service import ApiService, JobService
from django.views import generic
from django.views import View
from . import forms
import requests
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def error_404_view(request, exception):
    return render(request,'404.html')


class HomeView(TemplateView):

    template_name = 'home.html'

@method_decorator(login_required, name='dispatch')
class GetForm(generic.FormView):
    template_name = 'request_form.html'
    form_class = forms.APIForm

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        ApiService.schedule_request(data, user)

        return redirect('../admin/api/job/')



