"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from transactions import views
#from django.contrib.auth import views as auth_views

app_name = 'transactions'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('summary/', views.financial_summary, name='financial_summary'),
    path('register_income/', views.income_registration, name='income_registration'),
    path('register_expense/', views.expense_registration, name='expense_registration'),
    path('bank/<int:pk>/', views.bank_detail, name='bank_detail'), 
    path('add_bank/', views.add_bank, name='add_bank'), 
    path('cash/<int:pk>/', views.cash_detail, name='cash_detail'), 
    path('add_cash_amount/', views.add_cash_amount, name='add_cash_amount'), 
    path('create_recurring_transaction/', views.create_recurring_transaction, name='recurring_transaction'),
    
    path('portfolio_details/<int:pk>/', views.portfolio_details, name="portfolio_details"),
    path('manage_stock/<int:pk>/', views.manage_stock, name='manage_stock'),
    path('create_portfolio/', views.create_portfolio, name="create_portfolio"),
    path('eliminate_portfolio/<int:pk>/', views.eliminate_portfolio, name="eliminate_portfolio"),
    path('portfolio/<int:pk>/manage_cash/', views.manage_cash, name='manage_cash'),


    #add the next two on main url file
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
