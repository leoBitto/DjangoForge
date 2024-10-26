from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .utils import *
import logging 


# this is the part of the website accessible only to admin
@login_required
def dashboard(request):
    context = {}
    return render(request, 'backoffice/backoffice_base.html', context)

logger = logging.getLogger('app')

class SelectReportTypeView(LoginRequiredMixin, TemplateView):
    template_name = 'backoffice/reports/select_report_type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiunge il form al contesto
        context['report_type_form'] = ReportTypeForm()
        return context

