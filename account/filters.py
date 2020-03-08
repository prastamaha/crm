import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    # uncomment ini jika ingin menambahkan fitur filter berdasarkan tanggal lebih atau kurang dari sama dengan
    #start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte')
    #end_date = django_filters.DateFilter(field_name='date_created', lookup_expr='lte')
    
    # untuk search berdasarkan huruf yang menyerupai
    note = django_filters.CharFilter(field_name='note',lookup_expr='icontains',label='Note')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = [
            'customer', 
            #'date_created'
        ]