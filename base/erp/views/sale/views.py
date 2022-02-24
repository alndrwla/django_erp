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

from base.erp.forms import SaleForm, ClientForm
from base.erp.models import Sale, SaleLocation, Product, DetSale, Client, Business

class SaleIndexView(LoginRequiredMixin, ListView):
	model = SaleLocation
	template_name = 'sale/index.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de locales'
		context['list_url'] = reverse_lazy('erp:sale_index')
		context['entity'] = 'Ventas-Locales'
		return context


class SaleListView(LoginRequiredMixin, ListView):
	model = Sale
	template_name = 'sale/list.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_query_set(self):
		object_list = Sale.objects.filter(way_to_pay='E')
		return object_list

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data = []
				for i in Sale.objects.all().filter(sale_location_id = self.kwargs.get('pk')).filter(way_to_pay = 'E'):
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
		context['title'] = 'Listado de Ventas'
		pk = self.kwargs.get('pk')
		context['create_url'] = "/erp/sale/add/"+str(pk)
		context['list_url'] = "/erp/sale/list/"+str(pk)
		context['sale_location'] = SaleLocation.objects.get(id=pk)
		context['entity'] = 'Ventas'
		return context


class SaleCreateView(LoginRequiredMixin, CreateView):
	model = Sale
	form_class = SaleForm
	template_name = 'sale/create.html'
	success_url = reverse_lazy('erp:sale_index')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'search_products':
				data = []
				ids_exclude = json.loads(request.POST['ids'])
				term = request.POST['term'].strip()
				products = Product.objects.filter(stock__gt=0)
				if len(term):
					products = products.filter(name__icontains=term).filter(sale_location_id = self.kwargs.get('pk'))
				for i in products.exclude(id__in=ids_exclude)[0:10]:
					item = i.toJSON()
					item['value'] = i.name
					data.append(item)
			elif action == 'search_autocomplete':
				data = []
				ids_exclude = json.loads(request.POST['ids'])
				term = request.POST['term'].strip()
				data.append({'id': term, 'text': term})
				products = Product.objects.filter(Q(code__icontains=term, stock__gt=0) | Q(name__icontains=term, stock__gt=0)).filter(sale_location_id = self.kwargs.get('pk'))
				for i in products.exclude(id__in=ids_exclude)[0:10]:
					item = i.toJSON()
					item['text'] = i.name
					data.append(item)
			elif action == 'add':
				with transaction.atomic():
					vents = json.loads(request.POST['vents'])
					sale = Sale()
					sale.user_id=request.user.id
					sale.sale_location_id = vents['sale_location_id']
					sale.first_pay = vents['first_pay']
					sale.total_first_pay = vents['total_first_pay']
					sale.way_to_pay = vents['way_to_pay']
					sale.date_joined = vents['date_joined']
					sale.cli_id = vents['cli']
					sale.subtotal = float(vents['subtotal'])
					sale.iva = float(vents['iva'])
					sale.total = float(vents['total'])
					sale.save()
					for i in vents['products']:
						det = DetSale()
						det.sale_id = sale.id
						det.prod_id = i['id']
						det.cant = int(i['cant'])
						det.discount = int(i['desc'])
						if(int(i['desc']) != 0):
							det.total_discount = float((float(i['sale_price']) * int(i['cant']))* (int(i['desc']) / 100))
						else:
							det.total_discount = 0
						det.price = float(i['sale_price'])
						det.subtotal = float(i['subtotal'])
						det.save()
						det.prod.stock -= det.cant
						det.prod.save()
					data = {'id': sale.id}
			elif action == 'search_clients':
				data = []
				term = request.POST['term']
				clients = Client.objects.filter(
					Q(names__icontains=term) | Q(surnames__icontains=term) | Q(ci__icontains=term))[0:10]
				for i in clients:
					item = i.toJSON()
					item['text'] = i.get_full_name()
					data.append(item)
			elif action == 'create_client':
				with transaction.atomic():
					frmClient = ClientForm(request.POST)
					data = frmClient.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Creación de una Venta'
		pk = self.kwargs.get('pk')
		context['entity'] = 'Ventas'
		context['list_url'] = "/erp/sale/list/"+str(pk)
		context['action'] = 'add'
		context['det'] = []
		context['sale_location_id'] = pk
		context['sale_location'] = SaleLocation.objects.get(id=pk)
		context['frmClient'] = ClientForm()
		return context

class SaleDeleteView(LoginRequiredMixin, DeleteView):
	model = Sale
	template_name = 'sale/delete.html'
	success_url = reverse_lazy('erp:sale_index')
	url_redirect = success_url


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminación de una Venta'
		context['entity'] = 'Ventas'
		context['list_url'] = self.success_url
		return context


class SaleInvoicePdfView(View):

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
			template = get_template('sale/invoice.html')
			context = {
				'sale': Sale.objects.get(pk=self.kwargs['pk']),
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
		return HttpResponseRedirect(reverse_lazy('erp:sale_index'))
