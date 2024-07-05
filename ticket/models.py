from django.db import models
from django.utils.translation import gettext_lazy

from datetime import datetime

from worker.models import Worker, Team

class Catergory(models.Model):
    category_name = models.CharField(max_length=250)
    duration = models.DurationField()

class Ticket(models.Model):

    class TicketStatus(models.TextChoices):
        OPEN = "OP", gettext_lazy("Open")
        ASIGNED = "AS", gettext_lazy("Asigned")
        REJECTED = "RE", gettext_lazy("Rejected")
        COMPLETED = "CO", gettext_lazy("Completed")

    summary = models.TextField()
    details = models.TextField()
    status = models.CharField(max_length=2, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    creator = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tickets")
   # category = models.ForeignKey(Catergory, on_delete=models.SET_DEFAULT, default='')
    assigned_to =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    completed_by =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_tickets" )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name="tickets")



    def update(self, task, **kwargs):
        task_to_method = {
            'assign': self.assign_ticket,
            'close': self.close_ticket,
            'reject': self.reject_ticket,
        }
        if task == 'reject':
            task_to_method[task]()
        else:
            task_to_method[task](kwargs['worker'])


    def assign_ticket(self, worker: Worker):
        if self.status == self.TicketStatus.ASIGNED or self.status == self.TicketStatus.OPEN:
            self.status = self.TicketStatus.ASIGNED
            self.assigned_to = worker
            self.updated = datetime.now()
            self.save()


    def close_ticket(self, worker: Worker):
        self.status = self.TicketStatus.COMPLETED
        self.assigned_to = None
        self.completed_by = worker
        self.updated = datetime.now()
        self.save()
    
    def reject_ticket(self):
        self.status = self.TicketStatus.REJECTED
        self.assigned_to = None
        self.updated = datetime.now()
        self.save()