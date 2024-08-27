from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from inventory.models.aggregated import *
from crm.models.aggregated import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .utils import *
from django.contrib import messages



# this is the part of the website accessible only to admin
@login_required
def dashboard(request):
    

    context = {
        
    }

    return render(request, 'backoffice/backoffice_base.html', context)



class ReportView(LoginRequiredMixin, ListView):
    template_name = 'inventory/reports/view_inventory_report.html'
    context_object_name = 'aggregations'

    def get_queryset(self):
        report_type = self.request.POST.get('report_type')
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')

        model_map = {
            'daily': InventoryDailyAggregation,
            'weekly': InventoryWeeklyAggregation,
            'monthly': InventoryMonthlyAggregation,
            'quarterly': InventoryQuarterlyAggregation,
            'yearly': InventoryYearlyAggregation,
        }

        model = model_map.get(report_type)
        if model:
            return model.objects.filter(date__range=[start_date, end_date]).order_by('-date')
        return model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = self.request.POST.get('report_type')
        context['start_date'] = self.request.POST.get('start_date')
        context['end_date'] = self.request.POST.get('end_date')
        return context