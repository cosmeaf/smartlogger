from django import forms
from .models import Device, Equipament, Maintenance

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_id', 'hourmeter']


class EquipamentForm(forms.ModelForm):
    class Meta:
        model = Equipament
        fields = ['device', 'initial_machine_hourmeter', 'name', 'fuel']
        # Exclude non-editable fields like initial_suntech_hourmeter


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['name', 'os', 'usage_hours', 'alarm_hours', 'obs']  # Inclua 'usage_hours' nos fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'os': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'usage_hours': forms.NumberInput(attrs={'class': 'form-control'}),  # Mantém como campo editável
            'alarm_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }