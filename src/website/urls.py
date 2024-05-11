from django.urls import path
from . import views

app_name="website"
urlpatterns = [
    path('', views.base, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard/image/', views.image_page, name='image_page'),
    path('dashboard/contact/', views.contact_page, name='contact_page'),
    path('dashboard/opening_hours/', views.opening_hours_page, name='opening_hours_page'),
    path('dashboard/gallery', views.gallery_page, name='gallery_page'),
    path('dashboard/add_image/', views.add_image, name='add_image'),
    path('dashboard/add_contact/', views.add_contact, name='add_contact'),
    path('dashboard/add_opening_hour/', views.add_opening_hour, name='add_opening_hour'),
    path('dashboard/add_gallery/', views.add_gallery, name='add_gallery'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('delete_opening_hours/<int:opening_hour_id>/', views.delete_opening_hour, name='delete_opening_hour'),
    path('delete_gallery/<int:gallery_id>/', views.delete_gallery, name='delete_gallery'),

    path('create_group/', views.create_group, name='create_group'),
    path('list_group/', views.group_list, name='list_group'),
    path('list_subscription/', views.subscription_list, name='list_subscription'),
]