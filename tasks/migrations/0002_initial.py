# Generated by Django 5.1.5 on 2025-03-22 15:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="assigned_to",
            field=models.ManyToManyField(
                related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="tasks.project",
            ),
        ),
        migrations.AddField(
            model_name="taskdetail",
            name="task",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="details",
                to="tasks.task",
            ),
        ),
    ]
