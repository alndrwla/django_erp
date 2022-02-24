from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from base.erp.models import Dealer
from base.erp.forms import DealerForm


class DealerListView(LoginRequiredMixin, ListView):
	model = Dealer
	template_name = 'dealer/list.html'

	def get_queryset(self):
		return self.model.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Distribuidoras de la empresa'
		context['business'] = Dealer.objects.all().first()
		context['create_url'] = reverse_lazy('erp:dealer_create')
		context['entity'] = 'Empresa'
		return context


class DealerCreateView(LoginRequiredMixin, CreateView):
	model = Dealer
	form_class = DealerForm
	template_name = 'dealer/create.html'
	success_url = reverse_lazy('erp:dealer_list')
	url_redirect = success_url
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ingrese los datos de la distribuidora'
		context['entity'] = 'Distribuidoras'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class DealerUpdateView(LoginRequiredMixin, UpdateView):
	model = Dealer
	form_class = DealerForm
	template_name = 'dealer/create.html'
	success_url = reverse_lazy('erp:dealer_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de un distribuidor'
		context['entity'] = 'Distribuidor'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context

class DealerDeleteView(LoginRequiredMixin, DeleteView):
	model = Dealer
	form_class = DealerForm
	template_name = 'dealer/delete.html'
	success_url = reverse_lazy('erp:dealer_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar un distribuidor'
		context['entity'] = 'Distribuidor'
		context['list_url'] = self.success_url
		context['action'] = 'delete'
		return context
