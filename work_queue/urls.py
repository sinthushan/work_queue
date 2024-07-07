"""
URL configuration for work_queue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from ticket.views import TicketsList, TicketDetail, AssignedTickets, CreateTicket, UpdateTicket, AddComment
from worker.views import TeamsList, TeamDetail, WorkersList, WorkerDetail, CreateWorker


urlpatterns = [
    path('teams/', TeamsList.as_view()),
    path('teams/<int:pk>/', TeamDetail.as_view()),
    path('workers/', WorkersList.as_view()),
    path('workers/<int:pk>/', WorkerDetail.as_view()),
    path('tickets/', TicketsList.as_view()),
    path('tickets/<int:pk>/', TicketDetail.as_view()),
    path('tickets/assigned', AssignedTickets.as_view()),
    path('tickets/create', CreateTicket.as_view()),
    path('tickets/<int:pk>/update', UpdateTicket.as_view()),
    path('tickets/<int:pk>/comment', AddComment.as_view()),
    path('teams/<int:pk>/addworker', CreateWorker.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('admin/', admin.site.urls),
]
