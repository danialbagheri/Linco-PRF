from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import ProductionJob, ModelChangeLogsModel, ProductionList
from django_currentuser.middleware import get_current_user
import datetime
# this receiver is executed every-time some data is saved in any table
@receiver(pre_save, sender=ProductionList)
@receiver(pre_save, sender=ProductionJob)
def audit_log(sender, instance, **kwargs):
    print(instance.has_changed)
    # code to execute before every model save
    if instance.has_changed:
        user = get_current_user()
        for changeField in instance.changed_fields:
            ModelChangeLogsModel.objects.create(
                user_id = user.id,
                table_name = instance.__class__.__name__,
                table_id=instance.pk,
                table_row = changeField,
                data = instance.get_field_diff(changeField),
                timestamp = datetime.datetime.now()
            )
    else:
        pass
