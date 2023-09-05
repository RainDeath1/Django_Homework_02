from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView, DetailView, ArchiveIndexView
from django.http import JsonResponse, HttpResponseRedirect
from .models import Task, IceCream
from .forms import TaskForm, IceCreamForm, ProductForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('request_data.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class TaskListView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        tasks = Task.objects.all()
        paginator = Paginator(tasks, 10)
        page = request.GET.get('page')
        task_on_page = paginator.get_page(page)
        logger.info('GET request data: %s', request.GET)
        return render(request, 'tasks/task_list.html', {'tasks': task_on_page})
        # logger.info('GET request data: %s', request.GET)
        # return render(request, 'tasks/task_list.html', {'tasks': tasks})


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


class UserListView(ListView):
    model = User
    template_name = "tasks/users_list.html"


class UserDetailView(DetailView):
    model = User
    template_name = "tasks/user_detail.html"
    context_object_name = 'user'

    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(User, id=user_id)


class UserRedirectView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id', None)
        if user_id is not None and user_id != '':
            return HttpResponseRedirect(reverse('tasks:user_detail', kwargs={'user_id': user_id}))
        else:
            return HttpResponseRedirect(reverse('tasks:users'))


class TaskDetailView(View):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        history = task.change_set.all()
        print(history)
        return render(request, 'tasks/task_detail.html', {'task': task, 'history': history})


class TaskArchiveIndexView(ArchiveIndexView):
    model = Task
    date_field = "due_date"
    template_name = "tasks/task_archive.html"
    context_object_name = "tasks"
    allow_future = True


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


def create_icecream(request):
    if request.method == 'POST':
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('icecream_list')
    else:
        form = IceCreamForm()

    return render(request, 'Icecream/create_icecream.html', {'form': form})



class IceCreamListView(ListView):
    model = IceCream
    template_name = 'Icecream/icecream_list.html'

#26
def product_create_view(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Продукт успешно добавлен в каталог'
            form = ProductForm()
        else:
            error_message = 'Что-то пошло не так. Пожалуйста, проверьте введенные данные'
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    })


