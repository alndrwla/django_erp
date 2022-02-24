from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView, CreateView, ListView, UpdateView, DeleteView
from base.user.models import User
from base.erp.models import Business

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserForm

# Create your views here.
def home(request):
	context = {
		'bussiness' : Business.objects.first()
	}
	return render(request, 'login/index.html', context)


class LoginFormView(LoginView):
	template_name = 'login/login.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_superuser:
				return redirect('erp:business_list')
			else:
				return redirect('erp:category_list')
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Iniciar sesión' 
		return context
	
class LogoutFormView(RedirectView):
	pattern_name = 'session:login'

	def dispatch(self, request, *args, **kwargs):
		logout(request)
		return super().dispatch(request, *args, **kwargs)
	
class ListUserFormView(LoginRequiredMixin, ListView):
	model = User
	template_name = 'login/list.html'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data = []
				for i in User.objects.all():
					data.append(i.toJSON())
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de Usuarios'
		context['create_url'] = reverse_lazy('session:register')
		context['list_url'] = reverse_lazy('session:list')
		context['entity'] = 'Usuarios'
		return context


class RegisterFormView(LoginRequiredMixin,CreateView):
	model = User
	template_name = 'login/register.html'
	form_class = UserForm
	success_url = reverse_lazy('session:list')
	url_redirect = success_url
	permission_required = 'add_user'

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'add':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			print(data)
			data['error'] = str(e)
		print(data)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Creación de un Usuario'
		context['entity'] = 'Usuarios'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
	model = User
	form_class = UserForm
	template_name = 'login/register.html'
	success_url = reverse_lazy('session:list')
	permission_required = 'change_user'
	url_redirect = success_url

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edición de un Usuario'
		context['entity'] = 'Usuarios'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
	model = User
	form_class = UserForm
	template_name = 'login/delete.html'
	success_url = reverse_lazy('session:list')
	url_redirect = success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar un usuario'
		context['entity'] = 'Usuarios'
		context['list_url'] = self.success_url
		context['action'] = 'delete'
		return context

	def post(self, request, *args, **kwargs):
		id_data = self.kwargs.get('pk')
		User.objects.filter(id=id_data).delete()
		return redirect('/user/list/')
