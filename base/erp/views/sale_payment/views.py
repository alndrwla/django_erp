import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from xhtml2pdf import pisa

from django.shortcuts import redirect


from base.erp.forms import SaleForm, ClientForm, SalePaymentForm
from base.erp.models import Sale, SaleLocation, Product, DetSale, Client, Business, SalePayment

class SalePaymentIndexView(LoginRequiredMixin, ListView):
	model = SaleLocation
	template_name = 'sale_payment/index.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de locales Créditos'
		context['list_url'] = reverse_lazy('erp:sale_payment_index')
		context['entity'] = 'Ventas-Locales Créditos'
		return context


class SalePaymentListView(LoginRequiredMixin, ListView):
	model = Sale
	template_name = 'sale_payment/list.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_query_set(self):
		object_list = Sale.objects.filter(way_to_pay='C')
		return object_list

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data = []
				for i in Sale.objects.all().filter(sale_location_id = self.kwargs.get('pk')).filter(way_to_pay = 'C'):
					data.append(i.toJSON())
			elif action == 'search_details_prod':
				data = []
				for i in DetSale.objects.filter(sale_id=request.POST['id']):
					data.append(i.toJSON())
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de Ventas Crédito'
		pk = self.kwargs.get('pk')
		context['list_url'] = "/erp/sale_payment/list/"+str(pk)
		context['sale_location'] = SaleLocation.objects.get(id=pk)
		context['entity'] = 'Ventas - Crédito'
		return context


class SalePaymentCreateView(LoginRequiredMixin, CreateView):
	model = SalePayment
	form_class = SalePaymentForm
	template_name = 'sale_payment/create.html'
	success_url = reverse_lazy('erp:sale_payment_index')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			with transaction.atomic():
				vents = json.loads(request.POST['vents_payment'])
				sale_payment = SalePayment()
				sale_payment.payment = vents['payment']
				sale_payment.detail = vents['detail']
				sale_payment.subtotal = vents['subtotal']
				sale_payment.sale_id = vents['sale']
				sale_payment.user_id = request.user.id
				sale_payment.save()
				data = {'id': sale_payment.id}
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk = self.kwargs.get('pk')
		context['title'] = 'Creación de una Pago'
		sales_payments = SalePayment.objects.filter(sale_id=pk)
		try:
			sales_last_payment = SalePayment.objects.filter(sale_id=pk).order_by('-id')[0]
		except IndexError:
			sales_last_payment = None
		context['entity'] = 'Pagos'
		context['list_url'] = "/erp/sale_payment/index/"
		context['action'] = 'add'
		context['sale'] = Sale.objects.get(id=pk)
		context['sale_payments'] = sales_payments
		context['sale_last_payment'] = sales_last_payment
		context['sale_location_id'] = pk
		return context

class SalePaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_payment_index')
    permission_required = 'delete_sale'
    url_redirect = success_url


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class SalePaymentInvoicePdfView(View):

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
		business = Business.objects.first()
		try:
			template = get_template('sale_payment/invoice.html')
			context = {
				'sale_payment': SalePayment.objects.get(pk=self.kwargs['pk']),
				'comp': {'name': str(business.name), 'ruc': str(business.ruc)},
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
		return HttpResponseRedirect(reverse_lazy('erp:sale_payment_index'))
