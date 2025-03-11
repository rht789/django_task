import os
import django
from faker import Faker
import random
from django.contrib.auth.models import User
from django.utils import timezone
from tasks.models import Project, Task, TaskDetail

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

# Function to populate the database
def populate_db():
    # Initialize Faker
    fake = Faker()

    # Clear existing data to avoid conflicts
    TaskDetail.objects.all().delete()
    Task.objects.all().delete()
    Project.objects.all().delete()
    User.objects.all().delete()
    print("Cleared existing data.")

    # Create Projects
    projects = [Project.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph(),
        start_date=fake.date_this_year()
    ) for _ in range(5)]
    print(f"Created {len(projects)} projects.")

    # Create Users
    employees = [User.objects.create_user(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
        last_login=timezone.make_aware(fake.date_time_this_year()),
        is_superuser=False,
        is_staff=False,
        is_active=True,
        date_joined=timezone.make_aware(fake.date_time_this_year())
    ) for _ in range(5)]
    print(f"Created {len(employees)} employees.")

    # Create Tasks
    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED'])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)
    print(f"Created {len(tasks)} tasks.")

    # Create Task Details
    task_details_count = 0
    for task in tasks:
        try:
            TaskDetail.objects.create(
                task=task,
                priority=random.choice(['H', 'M', 'L']),
                notes=fake.paragraph()
            )
            task_details_count += 1
        except Exception as e:
            print(f"Failed to create TaskDetail for task {task.title}: {str(e)}")
    print(f"Created {task_details_count} TaskDetails out of {len(tasks)} tasks.")

    # Verify TaskDetail creation
    created_task_details = TaskDetail.objects.count()
    print(f"Total TaskDetails in database: {created_task_details}")
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()