from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseNotFound, Http404, StreamingHttpResponse, FileResponse, \
    JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


class CountBbView(TemplateView):
    def get(self, request, *args, **kwargs):
        result = dict()
        for r in Rubric.objects.annotate(num_bbs=Count('bb')):
            result.update({r.pk: r.num_bbs})

        return result


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class IndexView(TemplateView):
    template_name = 'bboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        return context


class IndexOldView(ListView):
    template_name = 'bboard/index.html'
    queryset = Bb.objects.order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class ByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        context['count_bb'] = count_bb()
        return context


def count_bb():
    result = dict()
    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class AddAndSaveView(CreateView):
    form_class = BbForm
    template_name = 'bboard/create.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('by_rubric',
                                            kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk}))

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, 'bboard/create.html', context)


class DetailView(DetailView):
    model = Bb
    template_name = 'bboard/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bb = get_object_or_404(Bb, pk=self.kwargs['pk'])
        context['bbs'] = get_list_or_404(Bb, rubric=bb.rubric.pk)
        return context


