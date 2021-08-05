from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from main.forms import SchemaForm, SchemaDetailsFormSet, DatasetForm
from main.models import Schema, Dataset
from main.tasks import generate_data


class SchemaList(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'main/list_schemas.html'
    fields = ['pk', 'name', 'updated_at']


class SchemaCreate(CreateView):
    model = Schema
    template_name = 'main/schema_form.html'
    form_class = SchemaForm

    def get_context_data(self, **kwargs):
        context = super(SchemaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = SchemaForm(self.request.POST, instance=self.object)
            context['schema_details_form'] = SchemaDetailsFormSet(self.request.POST, instance=self.object)
        else:
            context['form'] = SchemaForm(instance=self.object)
            context['schema_details_form'] = SchemaDetailsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        schema_details_form = context['schema_details_form']
        with transaction.atomic():
            self.object = form.save()
            if schema_details_form.is_valid():
                schema_details_form.instance = self.object
                schema_details_form.save()
        return super(SchemaCreate, self).form_valid(form)


class SchemaEdit(LoginRequiredMixin, UpdateView):
    model = Schema
    template_name = 'main/schema_form.html'
    form_class = SchemaForm

    def get_context_data(self, **kwargs):
        context = super(SchemaEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = SchemaForm(self.request.POST, instance=self.object)
            context['schema_details_form'] = SchemaDetailsFormSet(self.request.POST, instance=self.object)
        else:
            context['form'] = SchemaForm(instance=self.object)
            context['schema_details_form'] = SchemaDetailsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        schema_details_form = context['schema_details_form']
        with transaction.atomic():
            self.object = form.save()
            if schema_details_form.is_valid():
                schema_details_form.instance = self.object
                schema_details_form.save()
        return super(SchemaEdit, self).form_valid(form)


class SchemaDelete(LoginRequiredMixin, DeleteView):
    model = Schema
    template_name = 'main/delete_confirm_schema.html'
    success_url = reverse_lazy('main:list_schemas')


class DatasetList(LoginRequiredMixin, ListView):
    model = Dataset
    template_name = 'main/list_datasets.html'
    fields = ['created_at', ]

    def get_queryset(self):
        self.schema = get_object_or_404(Schema, id=self.kwargs['pk'])
        return Dataset.objects.filter(schema=self.schema)

    def get_context_data(self, **kwargs):
        context = super(DatasetList, self).get_context_data(**kwargs)
        for item in context['object_list']:
            item.status = AsyncResult(item.task_id).state
        context['schema_id'] = self.kwargs['pk']
        return context


@login_required
def create_dataset(request):
    print(request.POST)
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            generate_data.delay(request.POST['schema_id'], request.POST['rows'])
            # return redirect(f'/schemas/list_datasets/{request.POST["schema_id"]}/',)
            return redirect('main:list_schemas')
    else:
        form = DatasetForm()
    return render(request, 'main/list_datasets.html', {'form': form})
