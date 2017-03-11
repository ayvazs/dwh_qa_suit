from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import UpdateView

from .models import Connection, TestSet, Test


class IndexView(generic.ListView):
    template_name = 'dwh_qa_core/index.html'
# context_object_name = 'latest_test_list'

    def get_queryset(self):
        return TestSet.objects.all()


class SyncView(generic.ListView):
    template_name = 'dwh_qa_core/sync.html'

    def get_queryset(self):
        return TestSet.objects.all()


class ConnectionsView(generic.ListView):
    model = Connection


class ConnectionDetailView(generic.DetailView):
    model = Connection


class ConnectionUpdate(UpdateView):
    model = Connection
    fields = [
        'connection_name',
        'connection_string'
    ]
    template_name_suffix = '_update'


class SetsView(generic.ListView):
    model = TestSet
    template_name = 'dwh_qa_core/testset_list.html'


class SetDetailView(generic.DetailView):
    model = TestSet
    template_name = 'dwh_qa_core/testset_detail.html'


class TestSetUpdate(UpdateView):
    model = TestSet
    fields = ['set_name']
    template_name_suffix = '_update'


class TestsView(generic.ListView):
    model = Test


class TestDetailView(generic.DetailView):
    model = Test

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TestDetailView, self).get_context_data(**kwargs)
        return context


class TestUpdate(UpdateView):
    model = Test
    fields = [
        'test_set',
        'check_cnx',
        'right_cnx',
        'test_name',
        'check_query',
        'right_query',
    ]
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(TestUpdate, self).get_context_data(**kwargs)
        context['test_sets_list'] = TestSet.objects.all()
        return context


def TestExecute(request, testset_id, pk):
    test = get_object_or_404(Test, pk = pk)
    test.execute()
    test.save()
    return HttpResponseRedirect(reverse('dwh_qa_core:test_detail', args = (test.test_set.id, test.id)))
