import django_filters
from django_filters import DateFilter
# from django_filters import CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name = "date_created", lookup_expr ='gte')
    end_date = DateFilter(field_name = "date_created", lookup_expr ='lte')
    # note = CharField(field_name = 'note', lookup_expr = 'icontains')
    # icontains means ignore case sensitivity

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


class ProductFilter(django_filters.FilterSet):

    # note = CharField(field_name = 'note', lookup_expr = 'icontains')
    # icontains means ignore case sensitivity

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['tags', 'data_created', 'description']
