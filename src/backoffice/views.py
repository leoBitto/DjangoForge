from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, FormView
from inventory.models.aggregated import *
from crm.models.aggregated import *
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

class SelectReportTypeView(LoginRequiredMixin, FormView):
    template_name = 'backoffice/reports/select_report_type.html'
    form_class = ReportTypeForm

    def form_valid(self, form):
        report_type = form.cleaned_data['report_type']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        app_name = self.request.POST.get('app_name')

        # Costruzione dell'URL dinamico per l'applicazione specifica
        url = reverse(f'{app_name}:generate_report') + f'?report_type={report_type}&start_date={start_date}&end_date={end_date}'

        logger.info(f'url : {url}')
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type_form'] = self.get_form()  # Passa il form come report_type_form
        return context


