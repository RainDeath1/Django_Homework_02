from bboard.models import Rubric
from bboard.views import count_bb
from django.contrib.auth.models import User


def rubrics(request):
    return {'rubrics': Rubric.objects.all(),
            'count_bb': count_bb(),
            }


def all_users(request):
    users = User.objects.all()
    users_group = []
    if request.user.is_authenticated:
        users_group = request.user.groups.all()
    return {'all_users': users, 'users_group': users_group}

