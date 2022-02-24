from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from base.erp.forms import PayChecksForm
from base.erp.models import Paychecks, Business


class PayCheckListView(LoginRequiredMixin, ListView):
	model = Paychecks
	template_name = 'paycheck/list.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data = []
				for i in Paychecks.objects.all():
					data.append(i.toJSON())
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de Cheques'
		context['business'] = Business.objects.all().first()
		context['create_url'] = reverse_lazy('erp:paycheck_create')
		context['list_url'] = reverse_lazy('erp:paycheck_list')
		context['entity'] = 'Cheques'
		return context


class PayCheckCreateView(LoginRequiredMixin, CreateView):
	model = Paychecks
	form_class = PayChecksForm
	template_name = 'paycheck/create.html'
	success_url = reverse_lazy('erp:paycheck_list')
	url_redirect = success_url

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			numCheck = request.POST['numCheck']
			name = request.POST['name']
			valor = request.POST['valor']
			plus = request.POST['plus']
			place = request.POST['place']
			date = request.POST['date']
			payChoice = request.POST['payChoice']

			if action == 'add':
				paycheck = Paychecks()
				paycheck.numCheck = numCheck
				paycheck.name = name
				paycheck.valor = valor
				paycheck.plus = plus
				paycheck.place = place
				paycheck.date = date
				paycheck.payChoice = payChoice
				paycheck.save()
				data = {'id': paycheck.id}
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Creación un cheque'
		context['entity'] = 'Cheques'
		context['business'] = Business.objects.all().first()
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class PayCheckUpdateView(LoginRequiredMixin, UpdateView):
	model = Paychecks
	form_class = PayChecksForm
	template_name = 'paycheck/create.html'
	success_url = reverse_lazy('erp:paycheck_list')
	url_redirect = success_url

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			numCheck = request.POST['numCheck']
			name = request.POST['name']
			valor = request.POST['valor']
			plus = request.POST['plus']
			place = request.POST['place']
			date = request.POST['date']
			payChoice = request.POST['payChoice']

			if action == 'edit':
				paycheck = self.get_object()
				paycheck.numCheck = numCheck
				paycheck.name = name
				paycheck.valor = valor
				paycheck.plus = plus
				paycheck.place = place
				paycheck.date = date
				paycheck.payChoice = payChoice
				paycheck.save()
				data = {'id': paycheck.id}
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición un cheque'
		context['entity'] = 'Cheques'
		context['business'] = Business.objects.all().first()
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context


class PayCheckDeleteView(LoginRequiredMixin, DeleteView):
	model = Paychecks
	template_name = 'paycheck/delete.html'
	success_url = reverse_lazy('erp:paycheck_list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminación de un cheque'
		context['business'] = Paychecks.objects.all().first()
		context['entity'] = 'Cheques'
		context['list_url'] = self.success_url
		return context
