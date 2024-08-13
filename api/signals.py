from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Device, Equipament, Maintenance
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Device)
def update_worked_hours(sender, instance, **kwargs):
    try:
        # Atualiza as horas trabalhadas do Equipament
        equipament = Equipament.objects.get(device=instance)
        hourmeter_increment = instance.hourmeter - equipament.initial_suntech_hourmeter
        equipament.worked_hours += hourmeter_increment
        equipament.worked_hours = equipament.worked_hours.quantize(Decimal('0.00'))
        equipament.initial_suntech_hourmeter = instance.hourmeter
        equipament.save()

        logger.info(f"Updated worked hours for {equipament.name}: {equipament.worked_hours}")

        # Atualiza os registros de Manutenção relacionados
        maintenances = Maintenance.objects.filter(equipament=equipament)
        for maintenance in maintenances:
            maintenance.usage_hours += hourmeter_increment
            maintenance.alarm_hours -= hourmeter_increment
            maintenance.usage_hours = maintenance.usage_hours.quantize(Decimal('0.00'))
            maintenance.save()
            
            logger.info(f"Updated usage hours for maintenance {maintenance.name}: {maintenance.usage_hours}")

    except Equipament.DoesNotExist:
        logger.error(f"Equipament related to device {instance.device_id} does not exist.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
