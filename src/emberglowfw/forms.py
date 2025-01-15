from django import forms
from . import widget


class source_destination_dropdowns(forms.Form):

    Source = forms.CharField(
        widget=widget.RedisSelect2Widget(data_view="firewall_obj_data",attrs={'data-width': '300px', 'data-placeholder': 'Select an option...'},reqired=False,blank=True)
    )
    Destination = forms.CharField(
        widget=widget.RedisSelect2Widget(data_view="firewall_obj_data",attrs={'data-width': '300px', 'data-placeholder': 'Select an option...'},reqired=False,blank=True)
    )
    Port = forms.CharField(
        widget=widget.RedisSelect2Widget(data_view="firewall_port_data",attrs={'data-width': '300px', 'data-placeholder': 'Select an option...'},reqired=False,blank=True)
    )