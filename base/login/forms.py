from datetime import datetime

from django.forms import *
from django import forms

from base.user.models import User


class UserForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["is_superuser"].label = "Es Administrador "
		self.fields["first_name"].label = "Nombres"
		self.fields['username'].widget.attrs['autofocus'] = True

	class Meta:
		model = User
		fields = ('username', 'ci', 'first_name', 'last_name', 'phone', 'password', 'is_superuser',)
		widgets = {
		'username': TextInput(
			attrs={
			'placeholder': 'Ingrese un usuario',
			}
		),
		'ci': TextInput(
			attrs={
				'placeholder':'Ingrese un número de cédula',
				'required': True,
			}
		),
		'first_name': TextInput(
			attrs={
				'placeholder': 'Ingrese un nombre',
				'required': True,
			}
		),
		'last_name': TextInput(
			attrs={
				'placeholder': 'Ingrese apellidos',
				'required': True,
			}
		),
		'phone': TextInput(
			attrs={
				'placeholder': 'Ingrese un número de teléfono/celular',
				'required': False,
			}
		),
		'password': TextInput(
			attrs={
				'placeholder':'Ingrese una contraseña',
				'type': 'password',
			}
		),
		'is_superuser':  CheckboxInput(
			attrs={
				'required': False,
			}
		),
		}
	
	def save(self, commit=True):
		data = {}
		form = super()
		try:
			if form.is_valid():
				pwd = self.cleaned_data['password']
				u = form.save(commit=False)
				if u.pk is None:
					u.set_password(pwd)
				else:
					user = User.objects.get(pk=u.pk)
					if user.password != pwd:
						u.set_password(pwd)
				u.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)

		return data
