from django.urls import path
from . import views

urlpatterns = [
    path("select2/fwobjs/", views.firewall_objs_data.as_view(), name="firewall_obj_data"),
    path("select2/fwports/", views.firewall_ports_data.as_view(), name="firewall_port_data"),
    path('rule_request/', views.request_start),
    path('rule_view/', views.view_rules),
]
