from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import ProductionJob, ModelChangeLogsModel, ProductionList
from django_currentuser.middleware import get_current_user
from django_comments.signals import comment_was_posted
from django_comments.models import Comment
from django.core.mail import send_mail
import datetime
from django.conf import settings
# this receiver is executed every-time some data is saved in any table
@receiver(pre_save, sender=ProductionList)
@receiver(pre_save, sender=ProductionJob)
def audit_log(sender, instance, **kwargs):
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

def comment_handler(sender, comment, request, **kwargs):
    recipient = request.user.email
    requested_by_user = comment.content_object.requested_by.email
    print(comment.content_object.prf_number)
    print(comment.content_object.requested_by.email)
    subject = "A comment was added to {}".format(comment.content_object)
    print(subject)
    message = comment.comment
    from_email = settings.DEFAULT_FROM_EMAIL
    # profile.save()
    send_mail(
        'A comment was added to ',
        message,
        from_email,
        [recipient, requested_by_user],
        fail_silently=False,
    )

comment_was_posted.connect(comment_handler, sender=Comment)