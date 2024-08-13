from django.urls import path
from .views import (device_list, device_detail, add_device, update_device, delete_device, device_map,
                    equipament_list, equipament_detail, equipament_create, equipament_update, equipament_delete,
                    maintenance_list, maintenance_create, maintenance_delete,maintenance_reset, 
                    MaintenanceUpdateUsageHoursAPIView, MaintenanceUpdateAlarmHoursAPIView, MaintenanceUpdateOSAPIView )

urlpatterns = [
    path('', device_list, name='device_list'),
    path('device/<int:id>/', device_detail, name='device_detail'),
    path('add-device/', add_device, name='add_device'),
    path('update-device/<int:id>/', update_device, name='update_device'),
    path('delete-device/<int:id>/', delete_device, name='delete_device'),
    path('device/map/<int:id>/', device_map, name='device_map'),
    #
    path('equipaments/', equipament_list, name='equipament_list'),
    path('equipaments/<int:pk>/', equipament_detail, name='equipament_detail'),
    path('equipaments/create/', equipament_create, name='equipament_create'),
    path('equipaments/<int:pk>/edit/', equipament_update, name='equipament_update'),
    path('equipaments/<int:pk>/delete/', equipament_delete, name='equipament_delete'),
    #
    path('maintenance/<int:pk>/maintenance/', maintenance_list, name='maintenance'),
    path('maintenance/create/<int:equipament_id>/', maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/delete/', maintenance_delete, name='maintenance_delete'),
    path('maintenance/<int:pk>/reset/', maintenance_reset, name='maintenance_reset'),
    path('api/maintenance/<int:pk>/update_usage_hours/', MaintenanceUpdateUsageHoursAPIView.as_view(), name='maintenance_update_usage_hours'),
    path('api/maintenance/<int:pk>/update_alarm_hours/', MaintenanceUpdateAlarmHoursAPIView.as_view(), name='maintenance_update_alarm_hours'),
    path('api/maintenance/<int:pk>/update_os/', MaintenanceUpdateOSAPIView.as_view(), name='maintenance_update_os'),
]
