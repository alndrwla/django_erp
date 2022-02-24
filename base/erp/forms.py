# python
from datetime import datetime

# django
from django.forms import *
from django import forms

# models
from base.erp.models import Business, SaleLocation, Dealer, Category, Product, Client, DetSale, Sale, SalePayment, Paychecks


class BusinessForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['autofocus'] = True

	class Meta:
		model = Business
		fields = 'name', 'ruc', 'facebook', 'whatsapp'
		widgets = {
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre de la empresa',
			}
		),
		'ruc': TextInput(
			attrs={
			'placeholder': 'Ingrese el ruc de la empresa',
			}
		),
		'facebook': TextInput(
			attrs={
			'placeholder': 'Ingrese la dirección de facebook de la empresa',
			}
		),
		'whatsapp': TextInput(
			attrs={
			'placeholder': 'Ingrese la dirección de whatsapp de la empresa',
			}
		),
		}


class SaleLocationForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['autofocus'] = True

	class Meta:
		model = SaleLocation
		fields = 'name', 'direction', 'business'
		widgets = {
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre del local',
			}
		),
		'direction': TextInput(
			attrs={
			'placeholder': 'Ingrese la dirección del local',
			}
		),
		}


class DealerForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['autofocus'] = True

	class Meta:
		model = Dealer
		fields = 'name', 'ruc'
		widgets = {
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre del distribuidor',
			}
		),
		'ruc': TextInput(
			attrs={
			'placeholder': 'Ingrese el ruc del distribuidor',
			}
		),
		}


class CategoryForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['autofocus'] = True


	class Meta:
		model = Category
		fields = 'name',
		widgets = {
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre de la categoría',
			}
		),
		}


class ProductForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['code'].widget.attrs['autofocus'] = True

	class Meta:
		model = Product
		fields = 'code', 'name', 'description', 'stock', 'unit_price', 'sale_price', 'dealer', 'category' ,'sale_location'
		widgets = {
		'code': TextInput(
			attrs={
			'placeholder': 'Ingrese el código del producto',
			}
		),
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre del producto',
			}
		),
		'description': TextInput(
			attrs={
			'placeholder': 'Ingrese una descripción',
			}
		),
		'stock': TextInput(
			attrs={
			'placeholder': 'Ingrese la cantidad',
			}
		),
		'unit_price': TextInput(
			attrs={
			'placeholder': 'Ingrese el precio unitario',
			}
		),
		'sale_price': TextInput(
			attrs={
			'placeholder': 'Ingrese el precio de venta',
			}
		),
		}


class ProductUpdateForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['code'].widget.attrs['autofocus'] = True

	class Meta:
		model = Product
		fields = 'code', 'name', 'description', 'stock', 'unit_price', 'sale_price', 'dealer', 'category' ,'sale_location'
		widgets = {
		'code': TextInput(
			attrs={
			'placeholder': 'Ingrese el código del producto',
			}
		),
		'name': TextInput(
			attrs={
			'placeholder': 'Ingrese el nombre del producto',
			}
		),
		'description': TextInput(
			attrs={
			'placeholder': 'Ingrese una descripción',
			}
		),
		'stock': TextInput(
			attrs={
			'placeholder': 'Ingrese la cantidad',
			}
		),
		'unit_price': TextInput(
			attrs={
			'placeholder': 'Ingrese el precio unitario',
			}
		),
		'sale_price': TextInput(
			attrs={
			'placeholder': 'Ingrese el precio de venta',
			}
		),
		}


class ClientForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['names'].widget.attrs['autofocus'] = True

	class Meta:
		model = Client
		fields = '__all__'
		widgets = {
			'names': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese sus nombres',
				}
			),
			'surnames': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese sus apellidos',
				}
			),
			'ci': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese su cédula',
				}
			),
			'address': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese su dirección',
				}
			),
			'phone': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese un teléfono celular o convencional',
				}
			),
			'score': forms.TextInput(
				attrs={
					'placeholder': 'Ingrese un puntaje',
				}
			),
			'gender': forms.Select()
		}

	def save(self, commit=True):
		data = {}
		form = super()
		try:
			if form.is_valid():
				instance = form.save()
				data = instance.toJSON()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data


class SaleForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['cli'].queryset = Client.objects.none()

	class Meta:
		model = Sale
		fields = '__all__'
		widgets = {
			'cli': forms.Select(attrs={
				'class': 'custom-select select2',
			}),
			'date_joined': forms.DateInput(
				format='%Y-%m-%d',
				attrs={
					'value': datetime.now().strftime('%Y-%m-%d'),
					'autocomplete': 'off',
					'class': 'form-control datetimepicker-input',
					'id': 'date_joined',
					'data-target': '#date_joined',
					'data-toggle': 'datetimepicker'
				}
			),
			'iva': forms.TextInput(attrs={
				'class': 'form-control',
			}),
			'subtotal': forms.TextInput(attrs={
				'readonly': True,
				'class': 'form-control',
			}),
			'total': forms.TextInput(attrs={
				'readonly': True,
				'class': 'form-control',
			}),
			'way_to_pay': forms.Select(attrs={
				'class': 'form-control way_to_pay',
			}),
			'first_pay': forms.TextInput(attrs={
				'class': 'form-control',
			}),
			'total_first_pay': forms.TextInput(attrs={
				'readonly': True,
				'class': 'form-control',
			})
		}


class PayChecksForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['numCheck'].widget.attrs['autofocus'] = True

	class Meta:
		model = Paychecks
		fields = '__all__'
		widgets = {
			'numCheck': TextInput(
			attrs={
				'autocomplete': 'off',
				'placeholder': 'Ingrese número de cheque',
			}
			),
			'name': TextInput(
			attrs={
				'autocomplete': 'off',
				'placeholder': 'Orden',
			}
			),
			'valor': TextInput(
			attrs={
				'autocomplete': 'off',
				'placeholder': 'US $',
			}
			),
			'plus': TextInput(
			attrs={
				'autocomplete': 'off',
				'placeholder': 'La suma de',
			}
			),
			'place': TextInput(attrs={
			'autocomplete': 'off',
			'placeholder': 'Ciudad',
			}),
			'date': DateInput(
			format='%Y-%m-%d',
			attrs={
				'value': datetime.now().strftime('%Y-%m-%d'),
				'autocomplete': 'off',
				'id': 'paycheckId',
				'class': 'form-control datetimepicker-input',
				'data-target': '#paycheckId',
				'data-toggle': 'datetimepicker'
			}
			),
		}

	def save(self, commit=True):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data


class GuideForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	class Meta:
		model = Sale
		fields = '__all__'
		widgets = {
			'date_joined': forms.DateInput(
				format='%Y-%m-%d',
				attrs={
					'value': datetime.now().strftime('%Y-%m-%d'),
					'autocomplete': 'off',
					'class': 'form-control datetimepicker-input',
					'id': 'date_joined',
					'data-target': '#date_joined',
					'data-toggle': 'datetimepicker'
				}
			),
			'subtotal': forms.TextInput(attrs={
				'readonly': True,
				'class': 'form-control',
			}),
		}


class SalePaymentForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	class Meta:
		model = SalePayment
		fields = 'user','sale','payment', 'detail', 'subtotal'
		widgets = {
			'payment': forms.TextInput(attrs={
				'class': 'form-control',
			}),
			'detail': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder':'Ingrese un detalle ...',
			}),
			'subtotal': forms.TextInput(attrs={
				'readonly': True,
				'class': 'form-control',
			}),
		}
