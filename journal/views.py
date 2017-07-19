
from django import http
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView

from . import models


# Create your views here.

class ModuleList(ListView):
    model = models.Module

class ModuleDetails(generic.DetailView):
    model = models.Module

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()

        theseruns = obj.journalentry_set.all()
        related_toolruns = models.ToolRun.objects.filter(inputRuns__in=theseruns)
        context.update({'related_toolruns': related_toolruns})
        return context


# class JsonModuleList(ListView):
#     """ We can do something like this to output JSON if we want to
#         use JS on the frontend. """
#     model = models.Module

#     def get(self, request, *args, **kwargs):
#         def get_dict(module: models.Module):
#             return {
#                 'id': module.pk,
#                 'name': module.name,
#                 'produced': module.produced,
#             }

#         data = [get_dict(x) for x in self.get_queryset()]

#         resp = http.JsonResponse({'data': data})
#         resp["Access-Control-Allow-Origin"] = "*"
#         return resp
