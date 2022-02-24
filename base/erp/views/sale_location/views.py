from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from base.erp.models import SaleLocation
from base.erp.forms import SaleLocationForm


class SaleLocationListView(LoginRequiredMixin, ListView):
	model = SaleLocation
	template_name = 'sale_location/list.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Locales de la empresa'
		context['business'] = SaleLocation.objects.all().first()
		context['create_url'] = reverse_lazy('erp:sale_location_create')
		context['entity'] = 'Empresa'
		return context


class SaleLocationCreateView(LoginRequiredMixin, CreateView):
	model = SaleLocation
	form_class = SaleLocationForm
	template_name = 'sale_location/create.html'
	success_url = reverse_lazy('erp:sale_location_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ingrese los datos del local'
		context['entity'] = 'Locales'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class SaleLocationUpdateView(LoginRequiredMixin, UpdateView):
	model = SaleLocation
	form_class = SaleLocationForm
	template_name = 'sale_location/create.html'
	success_url = reverse_lazy('erp:sale_location_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de un local'
		context['entity'] = 'Local'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context

class SaleLocationDeleteView(LoginRequiredMixin, DeleteView):
	model = SaleLocation
	form_class = SaleLocationForm
	template_name = 'sale_location/delete.html'
	success_url = reverse_lazy('erp:sale_location_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar un local'
		context['entity'] = 'Local'
		context['list_url'] = self.success_url
		context['action'] = 'delete'
		return context
