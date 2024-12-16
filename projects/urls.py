from django.urls import path
from .views import (
    ProjectsListCreateView,
    RetrieveProjectView,
    TaskListCreateView,
    RetrieveTaskView,
    CommentsListCreateView,
    RetrieveCommentView
)

urlpatterns = [
    path('projects/', ProjectsListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', RetrieveProjectView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/tasks/', TaskListCreateView.as_view(), name='project-tasks'),
    path('tasks/<int:pk>/', RetrieveTaskView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/comments/', CommentsListCreateView.as_view(), name='comments-list'),
    path('comments/<int:id>/', RetrieveCommentView.as_view(), name='comment-details'),
]
