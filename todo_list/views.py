from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
from django.views import View


class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'tasks/task_list.html', {'tasks': tasks})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:task-list')

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task-list')
        else:
            print(form.errors)
        return render(request, 'tasks/task_create.html', {'form': form})


class TaskDetailView(View):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_detail.html', {'task': task})


class TaskUpdateView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_update.html', {'form': form, 'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task-list')
        return render(request, 'tasks/task_update.html', {'form': form, 'task': task})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:task-list')


def comprehension(request):
    data = [i for i in range(10)]
    return JsonResponse({'data': data})
