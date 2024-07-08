from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()

class Team(models.Model):
    team_name = models.CharField(max_length=250)

    def rank_workers_by_availability(self) -> list[str]:
        worker_availability = {}
        for worker in self.workers:
            worker_availability[worker.fullname] =  worker.get_availability()
        return  list(dict(sorted(worker_availability.items(), key=lambda item: item[1], reverse=True)).keys()) #is there a more readable way of doing this????

    def add_worker(self, view, request):
        serializer = view.get_serializer(self, data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user_data.pop('confirm_password')
            user = User.objects.create(**user_data)
            serializer.validated_data['team'] = self
            new_worker = Worker.objects.create(user=user, **serializer.validated_data)
            updated_serializer = view.get_serializer(new_worker)
            return updated_serializer
        return serializer


class Worker(models.Model):
    class PositionType(models.TextChoices):
        FULL_TIME = "FT", gettext_lazy("FullTime")
        PART_TIME = "PT", gettext_lazy("PartTime")

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker")
    logged_in = models.BooleanField(default = False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="workers")
    position_type = models.CharField(max_length=2, choices=PositionType.choices, default=PositionType.FULL_TIME)
    work_hours = models.FloatField()
    permission_group = models.IntegerField(default=1)
    def get_availability(self):
        hours_allocated = 0
        for ticket in self.assigned_tickets:
            hours_allocated  += ticket.category.duration
        return self.work_hours - hours_allocated
    