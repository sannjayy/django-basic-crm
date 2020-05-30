import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

# https://django-filter.readthedocs.io/en/master/

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name = 'date_created', lookup_expr='gte')
	end_date = DateFilter(field_name = 'date_created', lookup_expr='gte')
	status = CharFilter(field_name = 'status', lookup_expr='icontains')
	class Meta:
		model = Order
		fields = '__all__'
		# fields = ['product', 'status']
		exclude = ['date_created', 'customer']