from builtins import print

from django.contrib import admin
from api.models import Job, JobLog
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

@admin.register(JobLog)
class JobLogAdmin(admin.ModelAdmin):
    list_display = ("term","user", "create_at", "execution_time", "execution_success")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)