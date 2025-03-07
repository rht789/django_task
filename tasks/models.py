from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH , 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    # std_id = models.CharField(max_length=200, primary_key=True)
    task = models.OneToOneField(Task, on_delete=models.DO_NOTHING,related_name='details')
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=1,choices=PRIORITY_OPTIONS,default=LOW
    )
    notes = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"Details from Task {self.task}"
    
class Project(models.Model):
    name  = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name
    
@receiver(pre_save,sender = Task)
def notify_task_creation(sender,instance, **kwargs):
    print("sender", sender)
    print("instance", instance)
    instance.is_completed = True
    
@receiver(post_save,sender = Task)
def notify_task_creation(sender,instance,created, **kwargs):
    print("sender", sender)
    print("instance", instance)
    print(created)
    if created:
        instance.is_completed = True
        instance.save()

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance, instance.assigned_to.all())
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print("Checking....", assigned_emails)
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}",
            "rahatrezaulkarim@gmail.com",
            assigned_emails,
            fail_silently=False,
        )