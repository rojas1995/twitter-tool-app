from builtins import print

from django.contrib import admin
from api.models import Job, JobLog
from api.service import ApiService, JobService
from api.forms import APIForm
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):


    list_display = ("term","user", "create_at")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def save_model(self, request,   *args, **kwargs):
        form_class = APIForm
        params ={}
        params.update([('term', request.POST['term'])])
        params.update([('lang',request.POST['lang'])])
        params.update([('country',request.POST['country'])])

        params.update([('num_tw',request.POST['num_tw'])])
        params.update([('priority',request.POST['priority'])])
        if 'place' not in request.POST:
            params.update([('place', False)])
        else:
            params.update([('place', True)])
        if 'place' not in request.POST:
            params.update([('referenced_tweets', False)])
        else:
            params.update([('referenced_tweets', True)])
        if 'source' not in request.POST:
            params.update([('source', False)])
        else:
            params.update([('source', True)])
        form = form_class(params)
        form.is_valid()
        print(params)
        job = JobService.instance_job_without_results(params, request.user)
        job.num_tw=params['num_tw']
        print(job)
        ApiService.schedule_request_job(job)



@admin.register(JobLog)
class JobLogAdmin(admin.ModelAdmin):
    list_display = ("term","user", "create_at", "execution_time", "execution_success")
    readonly_fields = ("term","user", "create_at", "execution_time", "execution_success", "job_id", "lang", "country", "referenced_tweets", "place", "source", "num_tw")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)