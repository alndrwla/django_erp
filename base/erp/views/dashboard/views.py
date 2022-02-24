from datetime import datetime
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from base.erp.models import Sale, Product, DetSale


class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard.html'

	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'get_graph_sales_year_month':
				data = {
					'name': 'Porcentaje de venta',
					'showInLegend': False,
					'colorByPoint': True,
					'data': self.get_graph_sales_year_month()
				}
			elif action == 'get_graph_sales_products_year_month':
				data = {
					'name': 'Porcentaje',
					'colorByPoint': True,
					'data': self.get_graph_sales_products_year_month(),
				}
			elif action == 'get_graph_online':
				data = {'y': randint(1, 100)}
				print(data)
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_graph_sales_year_month(self):
		data = []
		try:
			year = datetime.now().year
			for m in range(1, 13):
				total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
					r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
				data.append(float(total))
		except:
			pass
		return data

	def get_graph_sales_products_year_month(self):
		data = []
		year = datetime.now().year
		month = datetime.now().month
		try:
			for p in Product.objects.filter():
				total = DetSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
												prod_id=p.id).aggregate(
					r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
				if total > 0:
					data.append({
						'name': p.name,
						'y': float(total)
					})
		except:
			pass
		return data

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['panel'] = 'Panel de administrador'
		context['graph_sales_year_month'] = self.get_graph_sales_year_month()
		return context


def page_not_found404(request, exception):
	return render(request, '404.html')
