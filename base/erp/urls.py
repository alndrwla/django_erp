from django.urls import path
from base.erp.views.business.views import BusinessListView, BusinessCreateView,BusinessUpdateView
from base.erp.views.sale_location.views import SaleLocationListView, SaleLocationCreateView, SaleLocationUpdateView, SaleLocationDeleteView

from base.erp.views.dealer.views import *
from base.erp.views.category.views import *
from base.erp.views.product.views import *
from base.erp.views.client.views import *
from base.erp.views.sale.views import *
from base.erp.views.sale_payment.views import *
from base.erp.views.guide.views import *
from base.erp.views.paycheck.views import *
from base.erp.views.dashboard.views import *

app_name = 'erp'

urlpatterns = [

	# business
	path("business_list/", BusinessListView.as_view(), name="business_list"),
	path("business_create/", BusinessCreateView.as_view(), name="business_create"),
	path("business_update/<int:pk>/", BusinessUpdateView.as_view(), name="business_update"),

	# sale location
	path("sale_location_list/", SaleLocationListView.as_view(), name="sale_location_list"),
	path("sale_location_create/", SaleLocationCreateView.as_view(), name="sale_location_create"),
	path("sale_location_update/<int:pk>/", SaleLocationUpdateView.as_view(), name="sale_location_update"),
	path("sale_location_delete/<int:pk>/", SaleLocationDeleteView.as_view(), 
	name="sale_location_delete"),

	# dealer
	path("dealer_list/", DealerListView.as_view(), name="dealer_list"),
	path("dealer_create/", DealerCreateView.as_view(), name="dealer_create"),
	path("dealer_update/<int:pk>/", DealerUpdateView.as_view(), name="dealer_update"),
	path("dealer_delete/<int:pk>/", DealerDeleteView.as_view(), 
	name="dealer_delete"),

	# category
	path("category_list/", CategoryListView.as_view(), name="category_list"),
	path("category_create/", CategoryCreateView.as_view(), name="category_create"),
	path("category_update/<int:pk>/", CategoryUpdateView.as_view(), name="category_update"),
	path("category_delete/<int:pk>/", CategoryDeleteView.as_view(), 
	name="category_delete"),

	# product
	path("product_list/", ProductListView.as_view(), name="product_list"),
	path("product_create/", ProductCreateView.as_view(), name="product_create"),
	path("product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
	path("product_delete/<int:pk>/", ProductDeleteView.as_view(), 
	name="product_delete"),
	path("product_print/<int:pk>/", ProductPrintView.as_view(), 
	name="product_print"),

	# client
	path('client/list/', ClientListView.as_view(), name='client_list'),
	path('client/add/', ClientCreateView.as_view(), name='client_create'),
	path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
	path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

	# sale
	path('sale/index/', SaleIndexView.as_view(), name='sale_index'),
	path('sale/list/<int:pk>/', SaleListView.as_view(), name='sale_list'),
	path('sale/add/<int:pk>/', SaleCreateView.as_view(), name='sale_create'),
	path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
	path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
	path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),

	# sale - payments
	path('sale_payment/index/', SalePaymentIndexView.as_view(), name='sale_payment_index'),
	path('sale_payment/list/<int:pk>/', SalePaymentListView.as_view(), name='sale_payment_list'),
	path('sale_payment/add/<int:pk>/', SalePaymentCreateView.as_view(), name='sale_payment_create'),
	path('sale_payment/invoice/pdf/<int:pk>/', SalePaymentInvoicePdfView.as_view(), name='sale_payment_invoice_pdf'),

	# paycheck
	path('paycheck/list/', PayCheckListView.as_view(), name='paycheck_list'),
	path('paycheck/add/', PayCheckCreateView.as_view(), name='paycheck_create'),
	path('paycheck/update/<int:pk>/', PayCheckUpdateView.as_view(), name='paycheck_update'),
	path('paycheck/delete/<int:pk>/', PayCheckDeleteView.as_view(), name='paycheck_delete'),

	# guide
	path('guide/index/', GuideIndexView.as_view(), name='guide_index'),
	path('guide/add/<int:pk>/', GuideCreateView.as_view(), name='guide_create'),
	path('guide/invoice/pdf/<int:pk>/', GuideInvoicePdfView.as_view(), name='guide_invoice_pdf'),

	# dashboard
	path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
