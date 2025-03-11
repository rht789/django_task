from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *

    
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

# @receiver(post_delete,sender=Task)
# def delete_associate_details(sender,instance,**kwargs):
#     if instance.details:
#         print(instance)
#         instance.details.delete()
#         print("Task Deleted Successfully")