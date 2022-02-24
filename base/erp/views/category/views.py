from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from base.erp.models import Category
from base.erp.forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'category/list.html'

	def get_queryset(self):
		return self.model.objects.all().filter(state=True)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Categorías de la empresa'
		context['create_url'] = reverse_lazy('erp:category_create')
		context['entity'] = 'Categoría'
		return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	form_class = CategoryForm
	template_name = 'category/create.html'
	success_url = reverse_lazy('erp:category_list')
	url_redirect = success_url

	def get_queryset(self):
		return self.model.objects.all().filter(state=True).filter(dealer__state=True)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ingrese los datos de la categoría'
		context['entity'] = 'Categorías'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	form_class = CategoryForm
	template_name = 'category/create.html'
	success_url = reverse_lazy('erp:category_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de una categoría'
		context['entity'] = 'Categoría'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
	model = Category
	form_class = CategoryForm
	template_name = 'category/delete.html'
	success_url = reverse_lazy('erp:category_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar una categoría'
		context['entity'] = 'Categoría'
		context['list_url'] = self.success_url
		context['action'] = 'delete'
		return context

