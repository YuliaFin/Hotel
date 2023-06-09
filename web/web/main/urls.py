from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms', views.rooms, name='rooms'),
    path('staf', views.staf, name='staf'),
    path('booking/', views.booking, name='booking'),
    path('about/', views.about, name='about'),
    path('occupancy_of_rooms', views.occupancy_edit, name='occupancy_of_rooms'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('check_room_availability/<str:date_of_arrival>/<str:date_of_departure>/',
         views.check_room_availability, name='check_room_availability'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('generate_report_1/', views.generate_report_1, name='generate_report_1'),
    path('now_book/', views.how_book, name='how_book'),
]