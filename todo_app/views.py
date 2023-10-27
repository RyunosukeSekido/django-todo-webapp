from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from todo_app.models import Task

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        searchInputText = self.request.GET.get("search") or ""
        if searchInputText:
            context["tasks"] = context["tasks"].filter(title__icontains=searchInputText)

        context["search"] = searchInputText
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    fields = "__all__"
    success_url = reverse_lazy("tasks")

class TaskListLoginView(LoginView):
    fields = "__all__"
    template_name = "todo_app/login.html"

    def get_success_url(self):
        return reverse_lazy("tasks")
    
class RegisterTodoApp(FormView):
    template_name = "todo_app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)