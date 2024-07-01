from django.db import models
from django.utils.translation import gettext_lazy

from datetime import datetime

from worker.models import Worker

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
    creator = models.CharField(max_length=250) # want to be able to use this system with other systesm and therefore the creator can not be a worker
   # category = models.ForeignKey(Catergory, on_delete=models.SET_DEFAULT, default='')
    assigned_to =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    completed_by =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_tickets" )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def assign_ticket(self, worker: Worker):
        if self.status == self.TicketStatus.ASIGNED or self.status == self.TicketStatus.OPEN:
            self.status = self.TicketStatus.ASIGNED
            self.assigned_to = worker
            self.updated = datetime.now()
            return f"Ticket {self.id} has been assigned to {worker.full_name}"

    def close_ticket(self, worker: Worker):
        self.status = self.TicketStatus.Completed
        self.assigned_to = None
        self.completed_by = worker
        self.updated = datetime.now()
    
    def reject_ticket(self):
        self.status = self.TicketStatus.REJECTED
        self.assigned_to = None
        self.updated = datetime.now()
