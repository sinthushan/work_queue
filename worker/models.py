from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    team_name = models.CharField(max_length=250)

    def rank_workers_by_availability(self) -> list[str]:
        worker_availability = {}
        for worker in self.workers:
            worker_availability[worker.fullname] =  worker.get_availability()
        return  list(dict(sorted(worker_availability.items(), key=lambda item: item[1], reverse=True)).keys()) #is there a more readable way of doing this????

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker")
    logged_in = models.BooleanField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="workers")
    work_hours = models.IntegerField()

    def get_availability(self):
        hours_allocated = 0
        for ticket in self.assigned_tickets:
            hours_allocated  += ticket.category.duration
        return self.work_hours - hours_allocated
    