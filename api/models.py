from django.db import models
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class Device(models.Model):
    device_id = models.CharField(max_length=20, unique=True)
    hourmeter = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Device {self.device_id} - Hourmeter: {self.hourmeter:.2f}"



class Equipament(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='equipament')
    initial_suntech_hourmeter = models.DecimalField('Initial Suntech Hourmeter', max_digits=20, decimal_places=2, default=Decimal('0.00'), editable=False)
    initial_machine_hourmeter = models.DecimalField('Initial Machine Hourmeter', max_digits=20, decimal_places=2, default=Decimal('0.00'))
    worked_hours = models.DecimalField('Worked Hours', max_digits=20, decimal_places=2, default=Decimal('0.00'), editable=False)
    name = models.CharField('Name', max_length=255)
    fuel = models.CharField('Fuel', max_length=8, default='DIESEL', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['device', 'name']),
        ]
        verbose_name_plural = "Equipaments"

    def save(self, *args, **kwargs):
        # Verifica se o objeto já existe no banco de dados
        if self.pk is None:
            # Defina o initial_suntech_hourmeter apenas uma vez ao criar o objeto
            self.initial_suntech_hourmeter = self.device.hourmeter

        # Calcula as horas trabalhadas
        hourmeter_increment = self.device.hourmeter - self.initial_suntech_hourmeter
        if hourmeter_increment > 0:
            self.worked_hours += hourmeter_increment
            self.worked_hours = self.worked_hours.quantize(Decimal('0.00'))
            self.initial_suntech_hourmeter = self.device.hourmeter

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.device}"



class Maintenance(models.Model):
    equipament = models.ForeignKey('Equipament', on_delete=models.CASCADE, related_name='maintenances')
    initial_suntech_hourmeter = models.DecimalField('Initial Suntech Hourmeter', max_digits=20, decimal_places=2, default=Decimal('0.00'))
    initial_maintenance_hourmeter = models.DecimalField('Initial Maintenance Hourmeter', max_digits=20, decimal_places=2, default=Decimal('0.00'))
    name = models.CharField('Nome do Alarme', max_length=255)
    os = models.BooleanField('Order Service (OS)', default=False)
    usage_hours = models.DecimalField('Tempo de uso (Peça)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    alarm_hours = models.DecimalField('Tempo para o próximo alarme', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    obs = models.TextField('Observações', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['equipament']),
            models.Index(fields=['name']),
            models.Index(fields=['os']),
        ]
        verbose_name_plural = "Maintenances"
        verbose_name = "Maintenance"

    @property
    def remaining_hours(self):
        """Calculate remaining hours before maintenance is due."""
        return self.alarm_hours - self.usage_hours

    def save(self, *args, **kwargs):
        """Override the save method to update usage_hours and remaining_hours."""
        if self.equipament and self.equipament.device:
            current_hourmeter = self.equipament.device.hourmeter

            # Log the current state before changes
            logger.info(f"Current Hourmeter: {current_hourmeter}")
            logger.info(f"Initial Suntech Hourmeter: {self.initial_suntech_hourmeter}")
            logger.info(f"Initial Maintenance Hourmeter: {self.initial_maintenance_hourmeter}")
            logger.info(f"Current Usage Hours: {self.usage_hours}")
            logger.info(f"Current Alarm Hours: {self.alarm_hours}")

            # Calculate the increment based on the hourmeter
            hourmeter_increment = current_hourmeter - self.initial_suntech_hourmeter

            # Ensure the increment is positive
            if hourmeter_increment > 0:
                # Increment usage_hours by the hourmeter increment
                self.usage_hours += hourmeter_increment

                # Decrement alarm_hours by the hourmeter increment
                self.alarm_hours -= hourmeter_increment

                # Log the updates
                logger.info(f"Hourmeter Increment: {hourmeter_increment}")
                logger.info(f"Updated Usage Hours: {self.usage_hours}")
                logger.info(f"Updated Alarm Hours: {self.alarm_hours}")

                # Reset initial_suntech_hourmeter to the current hourmeter for the next increment
                self.initial_suntech_hourmeter = current_hourmeter

        super().save(*args, **kwargs)

    def reset_usage_hours(self):
        """Reset usage hours and remaining hours after maintenance."""
        if self.equipament and self.equipament.device:
            # Log the state before reset
            logger.info(f"Resetting Maintenance: {self.name}")
            logger.info(f"Current Usage Hours: {self.usage_hours}")
            logger.info(f"Current Alarm Hours: {self.alarm_hours}")

            # Reset usage_hours to 0
            self.usage_hours = Decimal('0.00')

            # Reset initial_maintenance_hourmeter to the current hourmeter
            self.initial_maintenance_hourmeter = self.equipament.device.hourmeter

            # Reset remaining_hours to match alarm_hours (full cycle)
            self.alarm_hours = self.alarm_hours

            # Log the state after reset
            logger.info(f"Post-Reset Usage Hours: {self.usage_hours}")
            logger.info(f"Post-Reset Alarm Hours: {self.alarm_hours}")
            logger.info(f"Post-Reset Initial Maintenance Hourmeter: {self.initial_maintenance_hourmeter}")

            # Save the changes
            self.save(update_fields=['usage_hours', 'initial_maintenance_hourmeter', 'alarm_hours'])


class StopRecord(models.Model):
    maintenance = models.ForeignKey('Maintenance', on_delete=models.CASCADE, related_name='stop_records')
    date = models.DateTimeField(auto_now_add=True)
    hourmeter = models.DecimalField(max_digits=20, decimal_places=2)
    identifier = models.CharField(max_length=255)
    preventive = models.CharField(max_length=255)
    
    # Additional fields
    piece_name = models.CharField(max_length=255)  # Name of the piece
    equipment = models.ForeignKey('Equipament', on_delete=models.CASCADE, related_name='stop_records')
    time_in_maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Time spent in maintenance
    additional_info = models.TextField(blank=True, null=True)  # For complete audit information

    def __str__(self):
        return f"StopRecord for {self.maintenance.name} on {self.date}"

    def save(self, *args, **kwargs):
        # Calculate the time spent in maintenance if necessary
        if not self.pk:  # New record
            previous_record = StopRecord.objects.filter(maintenance=self.maintenance).order_by('-date').first()
            if previous_record:
                self.time_in_maintenance = self.hourmeter - previous_record.hourmeter
        super().save(*args, **kwargs)
