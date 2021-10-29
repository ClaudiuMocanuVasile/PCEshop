import django_filters
from django import forms
from .models import *
from django.forms.widgets import Input, NumberInput
from django.db.models import Min, Max
from math import ceil, floor



class CatalogFilter(django_filters.FilterSet):

    """This class inherits from the base FilterSet and builds a
       set of filters for nearly all attributes of Product model
    """


    name = django_filters.CharFilter(
        field_name = "name", 
        lookup_expr = "icontains", 
        widget = Input(
            attrs = {
                'class': 'border w-full col-span-2 h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none shadow-lg focus:ring-1 focus:ring-blue-600 rounded-md border-4 border-blue-600', 'placeholder': 'Name'
            }
        )
    )
    

    price1 = django_filters.NumberFilter(
        field_name = "price", 
        lookup_expr = "gte", 
        widget = NumberInput(
            attrs = {
                'value': floor(min(Product.objects.values_list('price', flat = True))), 
                'min': floor(min(Product.objects.values_list('price', flat = True))), 
                'max': ceil(max(Product.objects.values_list('price', flat = True))), 
                'step': 1, 
                'class': 'border w-full col-span-2 h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none shadow-lg focus:ring-1 focus:ring-blue-600 rounded-md border-4 border-blue-600', 'placeholder': 'Price'
            }
        )
    )
    

    price2 = django_filters.NumberFilter(
        field_name = "price", 
        lookup_expr = "lte", 
        widget = NumberInput(
            attrs = {
                'value': ceil(max(Product.objects.values_list('price', flat = True))), 
                'min': floor(min(Product.objects.values_list('price', flat = True))), 
                'max': ceil(max(Product.objects.values_list('price', flat = True))), 
                'step': 1, 
                'class': 'border w-full col-span-2 h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none shadow-lg focus:ring-1 focus:ring-blue-600 rounded-md border-4 border-blue-600', 'placeholder': 'Price'
            }
        )
    )


    brand_choices = tuple([(i, i) for i in list(Product.objects.order_by('brand').values_list('brand', flat = True).distinct().exclude(brand__isnull = True).exclude(brand__exact=''))])

    brand = django_filters.MultipleChoiceFilter(
        field_name = "brand", 
        lookup_expr = "in", 
        choices = brand_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_brands_method"
    )

    def multiple_brands_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(brand__in = value)
        else:
            return queryset
        return qs


    processor_manufacturer_choices = tuple([(i, i) for i in list(Product.objects.order_by('processor_manufacturer').values_list('processor_manufacturer', flat = True).distinct().exclude(processor_manufacturer__isnull = True).exclude(processor_manufacturer__exact=''))])

    processor_manufacturer = django_filters.MultipleChoiceFilter(
        field_name = "processor_manufacturer", 
        lookup_expr = "in", 
        choices = processor_manufacturer_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_processor_manufacturers_method"
    )

    def multiple_processor_manufacturers_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(processor_manufacturer__in = value)
        else:
            return queryset
        return qs
    

    processor_type_choices = tuple([(i, i) for i in list(Product.objects.order_by('processor_type').values_list('processor_type', flat = True).distinct().exclude(processor_type__isnull = True).exclude(processor_type__exact=''))])

    processor_type = django_filters.MultipleChoiceFilter(
        field_name = "processor_type", 
        lookup_expr = "in", 
        choices = processor_type_choices,
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_processor_types_method"
    )

    def multiple_processor_types_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(processor_type__in = value)
        else:
            return queryset
    
        return qs

    processor_model_choices = tuple([(i, i) for i in list(Product.objects.order_by('processor_model').values_list('processor_model', flat = True).distinct().exclude(processor_model__isnull = True).exclude(processor_model__exact=''))])

    processor_model = django_filters.MultipleChoiceFilter(
        field_name = "processor_model", 
        lookup_expr = "in", 
        choices = processor_model_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_processor_models_method")
    
    def multiple_processor_models_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(processor_model__in = value)
        else:
            return queryset
    
        return qs
    
    gpu_choices = tuple([(i, i) for i in list(Product.objects.values_list('gpu', flat = True).distinct().exclude(gpu__isnull = True).exclude(gpu__exact='').exclude(gpu__exact='Integrated'))])

    gpu = django_filters.MultipleChoiceFilter(
        field_name = "gpu", 
        lookup_expr = "in", 
        choices = gpu_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_gpus_method")

    def multiple_gpus_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(gpu__in = value)
        else:
            return queryset
        return qs


    gpu_manufacturer_choices =tuple([(i, i) for i in list(Product.objects.order_by('gpu_manufacturer').values_list('gpu_manufacturer', flat = True).distinct().exclude(gpu_manufacturer__isnull = True).exclude(gpu_manufacturer__exact=''))])

    gpu_manufacturer = django_filters.MultipleChoiceFilter(
        field_name = "gpu_manufacturer", 
        lookup_expr = "in", 
        choices = gpu_manufacturer_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_gpu_manufacturers_method"
    )

    def multiple_gpu_manufacturers_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(gpu_manufacturer__in = value)
        else:
            return queryset
        return qs


    gpu_model_choices = tuple([(i, i) for i in list(Product.objects.order_by('gpu_model').values_list('gpu_model', flat = True).distinct().exclude(gpu_model__isnull = True).exclude(gpu_model__exact=''))])

    gpu_model = django_filters.MultipleChoiceFilter(
        field_name = "gpu_model", 
        lookup_expr = "in", 
        choices = gpu_model_choices, 
        widget = forms.CheckboxSelectMultiple(),
        method = "multiple_gpu_models_method"
    )

    def multiple_gpu_models_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(gpu_model__in = value)
        else:
            return queryset
        return qs


    gpu_vram_type_choices = tuple([(i, i) for i in list(Product.objects.order_by('gpu_vram_type').values_list('gpu_vram_type', flat = True).distinct().exclude(gpu_vram_type__isnull = True).exclude(gpu_vram_type__exact=''))])

    gpu_vram_type = django_filters.MultipleChoiceFilter(
        field_name = "gpu_vram_type", 
        lookup_expr = "in", 
        choices = gpu_vram_type_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_gpu_vram_types_method"
    )

    def multiple_gpu_vram_types_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(gpu_vram_type__in = value)
        else:
            return queryset
    
        return qs

    ram_type_choices = tuple([(i, i) for i in list(Product.objects.order_by('ram_type').values_list('ram_type', flat = True).distinct().exclude(ram_type__isnull = True).exclude(ram_type__exact=''))])

    ram_type = django_filters.MultipleChoiceFilter(
        field_name = "ram_type", lookup_expr="in", 
        choices = ram_type_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_ram_types_method"
    )

    def multiple_ram_types_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(ram_type__in = value)
        else:
            return queryset
    
        return qs

    ram_memory_choices = tuple([(i, i) for i in list(Product.objects.order_by('ram_memory').values_list('ram_memory', flat = True).distinct().exclude(ram_memory__isnull = True).exclude(ram_memory__exact=''))])

    ram_memory = django_filters.MultipleChoiceFilter(
        field_name = "ram_memory", 
        lookup_expr = "in", 
        choices = ram_memory_choices, 
        widget = forms.CheckboxSelectMultiple(), method="multiple_ram_memorys_method"
    )

    def multiple_ram_memorys_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(ram_memory__in = value)
        else:
            return queryset
        return qs


    ram_frequency_choices = tuple([(i, i) for i in list(Product.objects.order_by('ram_frequency').values_list('ram_frequency', flat = True).distinct().exclude(ram_frequency__isnull = True).exclude(ram_frequency__exact=''))])

    ram_frequency = django_filters.MultipleChoiceFilter(
        field_name = "ram_frequency", 
        lookup_expr = "in", 
        choices = ram_frequency_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_ram_frequencys_method"
    )
    
    def multiple_ram_frequencys_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(ram_frequency__in = value)
        else:
            return queryset
        return qs


    storage_type_choices = tuple([(i, i) for i in list(Product.objects.order_by('storage_type').values_list('storage_type', flat = True).distinct().exclude(storage_type__isnull = True).exclude(storage_type__exact=''))])

    storage_type = django_filters.MultipleChoiceFilter(
        field_name = "storage_type", 
        lookup_expr = "in", 
        choices = storage_type_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_storage_types_method"
    )

    def multiple_storage_types_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(storage_type__in = value)
        else:
            return queryset
        return qs
    

    storage_choices = tuple([(i, i) for i in list(Product.objects.order_by('-storage').values_list('storage', flat = True).distinct().exclude(storage__isnull = True).exclude(storage__exact=''))])

    storage = django_filters.MultipleChoiceFilter(
        field_name = "storage", 
        lookup_expr = "in", 
        choices = storage_choices, 
        widget = forms.CheckboxSelectMultiple(), 
        method = "multiple_storages_method"
    )

    def multiple_storages_method(self, queryset, name, value):
        if len(value):
            return queryset.filter(storage__in = value)
        else:
            return queryset
        return qs


    class Meta:

        model = Product
        fields = '__all__'
        exclude = ['image', 'image2', 'image3']
