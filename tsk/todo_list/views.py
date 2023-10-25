import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.core.paginator import Paginator
from django.core.signing import Signer
from django.db import transaction
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, DetailView, ArchiveIndexView
from .forms import TaskForm, IceCreamForm, ProductForm, TaskFormSet, PlaylistForm, SongForm, FeedbackForm, ProfileForm, \
    SendingForm, RegisterForm
from .models import Task, IceCream, Playlist, Song, Product, FeedbackMessage, Profile, Sending, Documents
from django.conf import settings
from .services import send_reset_password_emails
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from .mixins import LoginRequiredMixin, HomePageView
import os

logger = logging.getLogger(__name__)
handler = logging.FileHandler('request_data.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


# home_28
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    print(f'Пользователь {user.username} вошел в систему.')


def compute_etag(request):
    total_tasks = Task.objects.count()
    return str(total_tasks)


# @method_decorator(condition(etag_func=compute_etag), name='dispatch')
class TaskListView(LoginRequiredMixin, HomePageView, View):
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
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            # home_41
            signer = Signer()
            task = form.save(commit=False)
            signed_title = signer.sign(task.title)
            task.title = signed_title
            task.save()
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


# home_41
def verify_task_title(task):
    signer = Signer()
    try:
        original_task = signer.unsign(task.title)
        return original_task
    except:
        raise ValueError('Название задачи сфальсифицировано')


class TaskDetailView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        try:
            verified_title = verify_task_title(task)
        except ValueError:
            return HttpResponse("Ошибка: заголовок задачи был изменен")
        history = task.change_set.all()
        print(history)
        context = {
            'task': task,
            'history': history,
            'verified_title': verified_title
        }
        return render(request, 'tasks/task_detail.html', context)


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


# 26
def product_create_view(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
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


# 27 home_27
def create_multiple_tasks(request):
    formset = TaskFormSet(queryset=Task.objects.none())

    if request.method == 'POST':
        formset = TaskFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('tasks:task-list')

    context = {'formset': formset}
    return render(request, 'tasks/multiple_task_create.html', context)


# @cache_page(60 * 2)
def playlist_list(request):
    playlists = Playlist.objects.all()
    print(playlists)
    return render(request, 'playlist/playlist_list.html', {'playlists': playlists})


def playlist_detail(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    return render(request, 'playlist/playlist_detail.html', {'playlist': playlist})


def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:playlist_list')
    else:
        form = PlaylistForm()
    return render(request, 'playlist/playlist_form.html', {'form': form})


def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:playlist_list')
    else:
        form = SongForm
    return render(request, 'playlist/song_form.html', {'form': form})


def create_product_and_playlist(name, song_title, artist):
    with transaction.atomic():
        playlist = Playlist(name=name)
        playlist.save()

        song = Song(title=song_title, artist=artist)
        song.save()

        playlist.songs.add(song)

        if Playlist.objects.filter(songs__title=song_title).exists():
            raise ValueError(
                f"Песня с названием {song_title} уже существует в другом плейлисте. Транзакция будет отменена.")

        product = Product(name=f"Товар для {name}", description=f"Официальный товар для плейлиста {name}", price=29.99)
        product.save()


# @cache_page(60 * 2)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def create_product_and_playlist_view(request):
    try:
        create_product_and_playlist("Мой плейлист", "Моя песня", "Мой исполнитель")
        return HttpResponse("Товар и плейлист успешно созданы!")
    except ValueError as e:
        return HttpResponse(str(e))


def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = FeedbackMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            feedback.save()
            return redirect('tasks:playlist_list')
    else:
        form = FeedbackForm()

    return render(request, 'playlist/feedback.html', {'form': form})


# home_33
@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('tasks:playlist_list')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'playlist/profile_edit.html', {'form': form})


# 34
def create_post(request):
    if request.method == 'POST':
        form = SendingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:playlist_list')
    else:
        form = SendingForm()
    return render(request, 'products/comment_product.html', {'form': form})


class SendingDetailView(DetailView):
    model = Sending
    template_name = 'products/view_post_bb.html'
    context_object_name = 'post'


# 35
def show_accordion(request):
    return render(request, 'django_bootstrap_example/accordion.html')


def show_alert(request):
    return render(request, 'django_bootstrap_example/alert.html')


def document_list_view(request):
    documents = Documents.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})


def upload_file_view(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        document = Documents(title=file_name, file=file_name)
        document.save()
        # home_41
        messages.success(request, "Файл успешно загружен!")
        return redirect('tasks:document-list')
    else:
        return render(request, 'documents/document_create.html', {})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:login')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def send_reset_password_on_emails(request):
    success_count = send_reset_password_emails(request)
    return HttpResponse(f"Успешно отправлено {success_count} писем.")


#home_44_for_test
# def tasks_view(request):
#     tasks = cache.get('all_tasks')
#     if not tasks:
#         tasks = Task.objects.all()
#         cache.set('all_tasks', tasks, 300)
#     return JsonResponse({'tasks': list(tasks.values())})

#end_44

def user_list(request):
    users = User.objects.all()
    return render(request, 'profile/user_list.html', {'users': users})


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile= user.profile
    context = {'user': user,
               'profile': profile}
    return render(request, 'profile/user_detail.html', context)
