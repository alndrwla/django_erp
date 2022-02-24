# python
from datetime import datetime

#django
from django.db import models
from django.forms import model_to_dict

# choices
from base.erp.choices import gender_choices, way_to_pay_choices, PAY_CHOICES

# models
from base.user.models import User


class Business(models.Model):
	name= models.CharField(max_length=150, null=False, blank=False, verbose_name="Nombre de la empresa")
	ruc = models.CharField(max_length=15, null=False, blank=False, verbose_name="Ruc")
	facebook = models.URLField(max_length=250, null=False, blank=False, verbose_name="Dirección de facebook")
	whatsapp = models.URLField(max_length=250, null=False, blank=False, verbose_name="Dirección de whatsapp")
	state = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Empresa'
		verbose_name_plural = 'Empresas'
		ordering = ['-id']


class Dealer(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Nombre del distribuidor")
	ruc = models.CharField(max_length=15, null=True, blank=True, verbose_name = "Ruc del distribuidor")
	state = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Distribuidor'
		verbose_name_plural = 'Distribuidores'
		ordering = ['-id']


class Category(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="Nombre de la categoría")
	state = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def toJSON(self):
		item = model_to_dict(self)
		return item

	class Meta:
		verbose_name = 'Categoría'
		verbose_name_plural = 'Categorías'
		ordering = ['-id']


class SaleLocation(models.Model):
	name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nombre del local")
	direction = models.CharField(max_length=50, null=False, blank=False, verbose_name="Dirección del local")
	business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name="Empresa")
	state = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Local'
		verbose_name_plural = 'Locales'
		ordering = ['-id']


class Product(models.Model):
	code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Código del producto")
	name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Nombre del producto")
	description = models.CharField(max_length=150, null=True, blank=True, verbose_name="Descripción del producto")
	stock = models.IntegerField(default=0, verbose_name="Cantidad de producto")
	unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name = "Precio unitario neto")
	sale_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name="Precio de venta")
	state = models.BooleanField(default=True)
	dealer = models.ForeignKey(Dealer, verbose_name="Distribuidor", on_delete=models.CASCADE)
	category =  models.ForeignKey(Category, verbose_name="Categoría", on_delete=models.CASCADE)
	sale_location = models.ForeignKey(SaleLocation, verbose_name="Local de ventas", on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def toJSON(self):
		item = model_to_dict(self, exclude=['category','dealer','sale_location'])
		item['full_name'] = '{} / {}'.format(self.name, self.category.name)
		item['cat'] = self.category.toJSON()
		item['sale_price'] = format(self.sale_price, '.2f')
		item['unit_price'] = format(self.unit_price, '.2f')
		return item

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['-id']


class Client(models.Model):
	names = models.CharField(max_length=150, verbose_name='Nombres')
	surnames = models.CharField(max_length=150, verbose_name='Apellidos')
	ci = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
	address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
	gender = models.CharField(max_length=10,choices=gender_choices, default='male', verbose_name='Sexo')
	phone =  models.CharField(null=True, blank=True, max_length=13, verbose_name='Teléfono celular o convencional')
	score = models.IntegerField(null=True, blank=True, default=500, verbose_name='Puntaje')

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return '{} {}'.format(self.names, self.surnames)

	def toJSON(self):
		item = model_to_dict(self)
		item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
		item['full_name'] = self.get_full_name()
		return item

	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clientes'
		ordering = ['-id']


class Sale(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sale_location = models.ForeignKey(SaleLocation, on_delete=models.CASCADE)
	cli = models.ForeignKey(Client, on_delete=models.CASCADE)
	date_joined = models.DateField(default=datetime.now)
	subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	way_to_pay = models.CharField(max_length=10, choices=way_to_pay_choices, default='E', verbose_name='Forma de pago')
	first_pay = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	total_first_pay = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

	def __str__(self):
		return self.cli.names

	def toJSON(self):
		item = model_to_dict(self)
		item['cli'] = self.cli.toJSON()
		item['subtotal'] = format(self.subtotal, '.2f')
		item['iva'] = format(self.iva, '.2f')
		item['det'] = [i.toJSON() for i in self.detsale_set.all()]
		item['det_payment'] = [i.toJSON() for i in self.salepayment_set.all()]
		if len(item['det_payment']) <= 0:
			if(self.first_pay == 0.00):
				item['total_sale'] = format(self.total, '.2f')
			else:
				item['total_sale'] = format(self.total_first_pay, '.2f')
		else:
			aux_total = item['det_payment'][-1]
			item['total_sale'] = list(aux_total.values())[-1]
		item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
		return item

	def delete(self, using=None, keep_parents=False):
		for det in self.detsale_set.all():
			det.prod.stock += det.cant
			det.prod.save()
		super(Sale, self).delete()

	class Meta:
		verbose_name = 'Venta'
		verbose_name_plural = 'Ventas'
		ordering = ['-id']


class DetSale(models.Model):
	sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
	prod = models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	cant = models.IntegerField(default=0)
	subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	discount = models.IntegerField(default=0, verbose_name='Descuento')
	total_discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

	def __str__(self):
		return self.prod.name

	def toJSON(self):
		item = model_to_dict(self, exclude=['sale'])
		item['prod'] = self.prod.toJSON()
		item['price'] = format(self.price, '.2f')
		item['subtotal'] = format(self.subtotal, '.2f')
		return item

	class Meta:
		verbose_name = 'Detalle de Venta'
		verbose_name_plural = 'Detalle de Ventas'
		ordering = ['id']


class Guide(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sale_location = models.ForeignKey(SaleLocation, on_delete=models.CASCADE)
	subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	date_joined = models.DateField(default=datetime.now)

	def __str__(self):
		return self.cli.names

	def toJSON(self):
		item = model_to_dict(self)
		item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
		item['det'] = [i.toJSON() for i in self.detguide_set.all()]
		return item

	class Meta:
		verbose_name = 'Guía'
		verbose_name_plural = 'Guías'
		ordering = ['-id']


class DetGuide(models.Model):
	guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
	prod = models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	cant = models.IntegerField(default=0)
	subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

	def __str__(self):
		return self.prod.name

	def toJSON(self):
		item = model_to_dict(self, exclude=['guide'])
		item['prod'] = self.prod.toJSON()
		item['price'] = format(self.price, '.2f')
		item['subtotal'] = format(self.subtotal, '.2f')
		return item

	class Meta:
		verbose_name = 'Detalle de Guía'
		verbose_name_plural = 'Detalle de Guías'
		ordering = ['id']


class Paychecks(models.Model):
	numCheck = models.CharField(max_length=10, verbose_name='Cheque N.')
	name = models.CharField(max_length=100, verbose_name='Páguese a la orden de')
	valor = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='US')
	plus = models.CharField(max_length=250, verbose_name='La suma de ')
	place = models.CharField(max_length=100, verbose_name='Ciudad')
	date = models.DateField(verbose_name='Fecha')
	payChoice = models.CharField(max_length=1, choices=PAY_CHOICES, default='C',verbose_name='Estado')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

	def __str__(self):
		return self.name

	def toJSON(self):
		item = model_to_dict(self)
		item['valor'] = format(self.valor, '.2f')
		return item

	class Meta:
		verbose_name = 'Detalle de Cheque'
		verbose_name_plural = 'Detalle de Cheques'
		ordering = ['-created']


class SalePayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
	payment = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	detail = models.CharField(max_length=255, null=True, blank=True,verbose_name="Detalle")
	subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	created = models.DateTimeField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

	def toJSON(self):
		item = model_to_dict(self, exclude=['sale'])
		item['payment'] = format(self.payment, '.2f')
		item['subtotal'] = format(self.subtotal, '.2f')
		return item

	class Meta:
		verbose_name = 'Detalle de Venta a crédito'
		verbose_name_plural = 'Detalle de Ventas a crédito'
		ordering = ['id']
