from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect
from xhtml2pdf import pisa
from django.template.loader import get_template

from base.erp.models import Product, Dealer, Category
from base.erp.forms import ProductForm, ProductUpdateForm

import json
import os
class ProductListView(LoginRequiredMixin, ListView):
	model = Product
	template_name = 'product/list.html'

	def get_queryset(self):
		return self.model.objects.all().filter(state=True).filter(dealer__state=True).filter(category__state=True).filter(sale_location__state=True)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Productos de la empresa'
		context['all_dealer'] = Dealer.objects.all()
		context['create_url'] = reverse_lazy('erp:product_create')
		context['entity'] = 'Productos'
		return context


class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	form_class = ProductForm
	template_name = 'product/create.html'
	success_url = reverse_lazy('erp:product_list')
	url_redirect = success_url

	def get_queryset(self):
		return self.model.objects.all().filter(state=True).filter(dealer__state=True).filter(category__state=True).filter(sale_location__state=True)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ingrese los datos del producto'
		context['entity'] = 'Productos'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
	model = Product
	form_class = ProductUpdateForm
	template_name = 'product/create.html'
	success_url = reverse_lazy('erp:product_list')
	url_redirect = success_url

	def get_queryset(self):
		return self.model.objects.all().filter(state=True).filter(dealer__state=True).filter(category__state=True).filter(sale_location__state=True)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de un producto'
		context['entity'] = 'Producto'
		context['id'] = self.kwargs.get('pk')
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
	model = Product
	form_class = ProductForm
	template_name = 'product/delete.html'
	success_url = reverse_lazy('erp:product_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar un producto'
		context['entity'] = 'Producto'
		context['list_url'] = self.success_url
		context['action'] = 'delete'
		return context


class ProductPrintView(View):
	
	def link_callback(self, uri, rel):
		"""
		Convert HTML URIs to absolute system paths so xhtml2pdf can access those
		resources
		"""
		# use short variable names
		sUrl = settings.STATIC_URL  # Typically /static/
		sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
		mUrl = settings.MEDIA_URL  # Typically /static/media/
		mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

		# convert URIs to absolute system paths
		if uri.startswith(mUrl):
			path = os.path.join(mRoot, uri.replace(mUrl, ""))
		elif uri.startswith(sUrl):
			path = os.path.join(sRoot, uri.replace(sUrl, ""))
		else:
			return uri  # handle absolute uri (ie: http://some.tld/foo.png)

		# make sure that file exists
		if not os.path.isfile(path):
			raise Exception(
				'media URI must start with %s or %s' % (sUrl, mUrl)
			)
		return path

	def get(self, request, *args, **kwargs):
		try:
			template = get_template('product/stock.html')
			context = {
				'products': Product.objects.all().filter(dealer_id=self.kwargs.get('pk')),
				'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
			}
			html = template.render(context)
			response = HttpResponse(content_type='application/pdf')
			# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			pisaStatus = pisa.CreatePDF(
				html, dest=response,
				link_callback=self.link_callback
			)
			return response
		except:
			pass
		return HttpResponseRedirect(reverse_lazy('erp:product_list'))
