from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer


class ProjectsListCreateView(generics.ListCreateAPIView):
    """
    View to list all projects or create a new project. This view handles two main functionalities:
    - **List all projects**: accessed with a GET request
    - **Create a new project**: accessed with a POST request
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()


class RetrieveProjectView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific project. This view provides functionalities to:
    - **Retrieve a project**: accessed with a GET request and a project ID (`pk`)
    - **Update a project**: accessed with a PUT or PATCH request
    - **Delete a project**: accessed with a DELETE request
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override get_object to ensure the correct project instance is fetched based on the request.
        """
        project_id = self.kwargs['pk']
        return generics.get_object_or_404(Project, id=project_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Project deleted successfully."}, status=status.HTTP_200_OK)


class TaskListCreateView(generics.ListCreateAPIView):
    """
    View to list all tasks under a specific project or create a new task.
    - **List all tasks**: accessed with a GET request under a specific project.
    - **Create a new task**: accessed with a POST request under a specific project.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Override get_queryset to filter tasks based on the project they belong to
        and ensure the tasks belong to projects owned by the authenticated user.
        """
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id, owner=self.request.user)
        except Project.DoesNotExist:
            raise NotFound("Project not found or you do not have permission.")
        return Task.objects.filter(project=project)

    def perform_create(self, serializer):
        """
        Override the default create behavior to associate the task with a specific project.
        - **Retrieve project**: Extracts the project ID from the URL parameters.
        - **Check permissions**: Ensures the project belongs to the authenticated user.
        - **Save task**: Associates the task with the retrieved project and saves it.
        """
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id, owner=self.request.user)
        except Project.DoesNotExist:
            raise NotFound("Project not found or you do not have permission.")
        serializer.save(project=project)


class RetrieveTaskView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific task.
    - **Retrieve a task**: accessed with a GET request and a task ID (`pk`).
    - **Update a task**: accessed with a PUT or PATCH request.
    - **Delete a task**: accessed with a DELETE request.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Override the default get_object method to ensure the correct task instance is fetched.
        """
        task_id = self.kwargs['pk']
        try:
            task = Task.objects.get(id=task_id, project__owner=self.request.user)
        except Task.DoesNotExist:
            raise NotFound("Task not found or you do not have permission.")
        return task

    def destroy(self, request, *args, **kwargs):
        """
        Override the default destroy behavior to delete a task instance.
        - **Retrieve task**: Fetches the task instance using `get_object()`.
        - **Delete task**: Performs the deletion and returns a success message.
        - **Response**: Returns a `200 OK` status with a success message after deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_200_OK)
    

class CommentsListCreateView(generics.ListCreateAPIView):
    """
    View to retrieve a list of all comments on a specific task or create a new comment.
    - **List all comments**: accessed with a GET request under a specific task.
    - **Create a new comment**: accessed with a POST request under a specific task.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id, project__owner=self.request.user)
        except Task.DoesNotExist:
            raise NotFound("Task not found or you do not have permission.")
        return Comment.objects.filter(task=task)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id, project__owner=self.request.user)
        except Task.DoesNotExist:
            raise NotFound("Task not found or you do not have permission.")
        serializer.save(user=self.request.user, task=task)


class RetrieveCommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific comment.
    - **Retrieve a comment**: accessed with a GET request and a comment ID (`id`).
    - **Update a comment**: accessed with a PUT or PATCH request.
    - **Delete a comment**: accessed with a DELETE request.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs.get('id')
        try:
            comment = Comment.objects.get(id=comment_id, task__project__owner=self.request.user)
        except Comment.DoesNotExist:
            raise NotFound("Comment not found or you do not have permission.")
        return comment

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_200_OK)
    