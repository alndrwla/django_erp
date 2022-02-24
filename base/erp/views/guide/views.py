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

from base.erp.forms import GuideForm, ClientForm
from base.erp.models import Guide, SaleLocation, Product, DetGuide, Client, Business

class GuideIndexView(LoginRequiredMixin, ListView):
	model = SaleLocation
	template_name = 'guide/index.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de locales - Guías'
		context['list_url'] = reverse_lazy('erp:guide_index')
		context['entity'] = 'Guías-Locales'
		return context


class GuideCreateView(LoginRequiredMixin, CreateView):
	model = Guide
	form_class = GuideForm
	template_name = 'guide/create.html'
	success_url = reverse_lazy('erp:guide_create')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'search_autocomplete':
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
					guide = Guide()
					guide.user_id=request.user.id
					guide.sale_location_id = vents['sale_location_id']
					guide.subtotal = vents['subtotal']
					guide.save()
					for i in vents['products']:
						det = DetGuide()
						det.guide_id = guide.id
						det.prod_id = i['id']
						det.cant = int(i['cant'])
						det.price = float(i['sale_price'])
						det.subtotal = float(i['subtotal'])
						det.save()
					data = {'id': guide.id}
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Creación de una Guía'
		pk = self.kwargs.get('pk')
		context['entity'] = 'Guías'
		context['action'] = 'add'
		context['det'] = []
		context['list_url'] = reverse_lazy('erp:guide_index')
		context['sale_location_id'] = pk
		context['sale_location'] = SaleLocation.objects.get(id=pk)
		return context


class GuideInvoicePdfView(View):

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
			template = get_template('guide/invoice.html')
			context = {
				'guide': Guide.objects.get(pk=self.kwargs['pk']),
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
		return HttpResponseRedirect(reverse_lazy('erp:guide_index'))
