from django.db import models
from django.utils.translation import gettext_lazy

from datetime import datetime

from worker.models import Worker, Team

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
    assigned_to =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    completed_by =  models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_tickets" )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name="tickets")


    def update(self, view, request):
        task_to_method = {
            'assign': self.assign_ticket,
            'close': self.close_ticket,
            'reject': self.reject_ticket,
        }
        task = request.data.pop('task', None)
        worker_id = request.data.pop('worker_id', request.user.worker.id)
        if task == 'reject':
            updated_serializer = task_to_method[task](view)
        else:
            updated_serializer = task_to_method[task](view, worker_id)
        self.updated = datetime.now()
        return updated_serializer

    def assign_ticket(self,view, worker_id):
        if self.status == self.TicketStatus.ASIGNED or self.status == self.TicketStatus.OPEN:
            data = {
                'status': self.TicketStatus.ASIGNED,
                'assigned_to':  worker_id,
            }
            updated_serializer = self.perform_update(view, data, True)
            return updated_serializer

    def close_ticket(self, view, worker_id):
        if self.status == self.TicketStatus.ASIGNED:
            data= {
                'status': self.TicketStatus.COMPLETED,
                'assigned_to':  None,
                'completed_by':  worker_id,
            }
            updated_serializer = self.perform_update(view, data, True)
            return updated_serializer

    def reject_ticket(self, view):
        if self.status == self.TicketStatus.ASIGNED or self.status == self.TicketStatus.OPEN:
            data= {
                'status': self.TicketStatus.REJECTED,
                'assigned_to':  None,
            }
            updated_serializer = self.perform_update(view, data, True)
            return updated_serializer
    
    def add_comment(self, view, request):
        data= {
            'creator': request.user.worker.id,
            'created': datetime.now(),
            'comment': request.data['comment'],
            'ticket': self.pk,
        }
        updated_serializer = self.perform_update(view, data)
        return updated_serializer

    def perform_update(self, view, data, partial=False):
        serializer = view.get_serializer(self, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
        return serializer

class Comment(models.Model):
    # comments allow ticket creator and ticket asignee to communicate in case 
    # any descrepency with what the ticket is asking. You should not be able to remove a comment
    # or modify it. When a worker leave the company the comment should persist but no longer have a creator.
    # These measures are to ensure that the work that the asignee has done matches exactly what was requested
    creator = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments") 
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")