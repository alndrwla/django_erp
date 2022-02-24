from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from base.erp.models import Business
from base.erp.forms import BusinessForm


class BusinessListView(LoginRequiredMixin, ListView):
	model = Business
	template_name = 'business/list.html'

	def get_queryset(self):
		return self.model.objects.all().first()

	def get_context_data(self, **kwargs):
		flag = self.model.objects.all().first()
		context = super().get_context_data(**kwargs)
		context['title'] = 'Datos de la empresa'
		context['business'] = Business.objects.all().first()
		if flag is None:
			context['create_url'] = reverse_lazy('erp:business_create')
		context['entity'] = 'Empresa'
		return context


class BusinessCreateView(LoginRequiredMixin, CreateView):
	model = Business
	form_class = BusinessForm
	template_name = 'business/create.html'
	success_url = reverse_lazy('erp:business_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ingrese los datos de la empresa'
		context['entity'] = 'Empresa'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class BusinessUpdateView(LoginRequiredMixin, UpdateView):
	model = Business
	form_class = BusinessForm
	template_name = 'business/create.html'
	success_url = reverse_lazy('erp:business_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de datos de la empresa'
		context['entity'] = 'Empresa'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context
