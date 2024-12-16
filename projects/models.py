from django.db import models
from config import settings

# Models to point to the custom user model
User = settings.AUTH_USER_MODEL

class Project(models.Model):
    '''
    This model representing a project in the project management application.
    Attributes:
    - id: The unique identifier for each project.
    - name: The name of the project.
    - description: A brief description of the project.
    - owner: The user who owns the project (a foreign key reference to the `User` model).
    - created_at: The timestamp when the project was created.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    '''
    A model representing a member of a project.
    Attributes:
    - id: The unique identifier for each project member.
    - project: The project this member is associated with (a foreign key reference to the `Project` model).
    - user: The user who is a member of the project (a foreign key reference to the `User` model).
    - role: The role of the member within the project (Admin or Member).
    '''
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_members')
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Member', 'Member')])

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class Task(models.Model):
    '''
    A model representing a task within a project.
    Attributes:
    - id: The unique identifier for each task.
    - title: The title of the task.
    - description: A description of the task.
    - status: The current status of the task (To Do, In Progress, or Done).
    - priority: The priority level of the task (Low, Medium, or High).
    - assigned_to: The user assigned to the task (foreign key to the `User` model, nullable).
    - project: The project this task belongs to (foreign key to the `Project` model).
    - created_at: The timestamp when the task was created.
    - due_date: The due date for the task.
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], default='To Do')
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''
    A model representing a comment on a task.
    Attributes:
    - id: The unique identifier for each comment.
    - content: The content of the comment.
    - user: The user who created the comment (a foreign key reference to the `User` model).
    - task: The task this comment is associated with (a foreign key reference to the `Task` model).
    - created_at: The timestamp when the comment was created.
    '''
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''
        Returns the first 50 characters of the comment content.
        '''
        return self.content[:50]  # Return the first 50 characters of the comment
