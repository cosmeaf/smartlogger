from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipament, Maintenance, Device
from .forms import DeviceForm, EquipamentForm, MaintenanceForm
from .serializers import MaintenanceAlarmHoursSerializer, MaintenanceOSSerializer, MaintenanceUsageHoursSerializer



def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device/device_list.html', {'devices': devices})

def device_detail(request, id):
    device = get_object_or_404(Device, id=id)
    return render(request, 'device/device_detail.html', {'device': device})

def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'device/add_device.html', {'form': form})


def update_device(request, id):
    device = get_object_or_404(Device, id=id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', id=device.id)  # Ensure the 'id' is correctly passed here
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device/update_device.html', {'form': form, 'device': device})


def delete_device(request, id):
    device = get_object_or_404(Device, id=id)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'device/delete_device.html', {'device': device})


def device_map(request, id):
    device = get_object_or_404(Device, id=id)
    return render(request, 'device/device_map.html', {'device': device})


# Equipaments Views
def equipament_list(request):
    equipaments = Equipament.objects.all()
    return render(request, 'equipament/equipament_list.html', {'equipaments': equipaments})

def equipament_detail(request, pk):
    equipament = get_object_or_404(Equipament, pk=pk)
    return render(request, 'equipament/equipament_detail.html', {'equipament': equipament})

def equipament_create(request):
    if request.method == 'POST':
        form = EquipamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipament_list')
    else:
        form = EquipamentForm()
    return render(request, 'equipament/equipament_form.html', {'form': form})

def equipament_update(request, pk):
    equipament = get_object_or_404(Equipament, pk=pk)
    if request.method == 'POST':
        form = EquipamentForm(request.POST, instance=equipament)
        if form.is_valid():
            form.save()
            return redirect('equipament_list')
    else:
        form = EquipamentForm(instance=equipament)
    return render(request, 'equipament/equipament_form.html', {'form': form})

def equipament_delete(request, pk):
    equipament = get_object_or_404(Equipament, pk=pk)
    if request.method == 'POST':
        equipament.delete()
        return redirect('equipament_list')
    return render(request, 'equipament/equipament_confirm_delete.html', {'equipament': equipament})


# Maintenance Data View

def maintenance_list(request, pk):
    equipament = get_object_or_404(Equipament, pk=pk)
    maintenances = Maintenance.objects.filter(equipament=equipament)

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            piece = form.save(commit=False)
            piece.equipament = equipament
            piece.save()
            return redirect('maintenance', pk=equipament.pk)  # Correct usage of the URL name
    else:
        form = MaintenanceForm()

    return render(request, 'maintenance/maintenance_list.html', {
        'form': form,
        'equipament': equipament,
        'maintenances': maintenances
    })


def maintenance_create(request, equipament_id):
    equipament = get_object_or_404(Equipament, id=equipament_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.equipament = equipament
            maintenance.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'equipament': equipament})


def maintenance_delete(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        equipament_pk = maintenance.equipament.pk
        maintenance.delete()
        return redirect('maintenance', pk=equipament_pk)  # Redirect to the correct maintenance list
    return render(request, 'maintenance/maintenance_confirm_delete.html', {'maintenance': maintenance})


def maintenance_reset(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        maintenance.reset_usage_hours()
        return redirect('maintenance', pk=maintenance.equipament.pk)
    return redirect('maintenance', pk=maintenance.equipament.pk)


class MaintenanceUpdateUsageHoursAPIView(APIView):
    def post(self, request, pk, format=None):
        try:
            maintenance = Maintenance.objects.get(pk=pk)
        except Maintenance.DoesNotExist:
            return Response({'error': 'Maintenance not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaintenanceUsageHoursSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceUpdateAlarmHoursAPIView(APIView):
    def post(self, request, pk, format=None):
        try:
            maintenance = Maintenance.objects.get(pk=pk)
        except Maintenance.DoesNotExist:
            return Response({'error': 'Maintenance not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaintenanceAlarmHoursSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceUpdateOSAPIView(APIView):
    def post(self, request, pk, format=None):
        try:
            maintenance = Maintenance.objects.get(pk=pk)
        except Maintenance.DoesNotExist:
            return Response({'error': 'Maintenance not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaintenanceOSSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
