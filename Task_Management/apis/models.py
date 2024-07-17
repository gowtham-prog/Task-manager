from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid;

def ten_digit_unique_id():
    return str(uuid.uuid4().int)[-1:-11:-1]

class TenDigitPK(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=ten_digit_unique_id,
        editable=False,
    )
    created_on = models.DateTimeField(
        'Date and Time of creation',
        default=timezone.now,
    )

    class Meta:
        abstract = True
        ordering = ['-created_on']

class User(TenDigitPK, AbstractUser):
    user_type = models.CharField(max_length=50, null=False, blank=True, default= "employee",
                                 choices=( ('admin', 'Admin'), ('employee', 'Employee'), ('manager', 'Manager') ))
    organization = models.CharField(max_length=50, null=True, blank=True, default = "NA")
    def __str__(self):
        return self.username

class Task(TenDigitPK):
    task_name = models.CharField(max_length=40,null=False, blank=False)
    task_description = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(User,related_name="created_tasks", on_delete=models.CASCADE,null=False, blank=False)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, null=False, blank=False, default="pending", choices=(("pending", "Pending"), ("started", "Started"), ("completed", "Completed")))
    assigned_to = models.ManyToManyField(User,related_name="assigned_tasks", blank=True)
    priority = models.CharField(max_length=20, null=False, blank=False, default="low", choices=(("low", "Low"), ("medium", "Medium"), ("high", "High")))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.task_name} by {self.created_by} on {self.created_on}"