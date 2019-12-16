from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import ProductionJob, ModelChangeLogsModel, ProductionList
from django_currentuser.middleware import get_current_user
from django_comments.signals import comment_was_posted
from django_comments.models import Comment
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
    sender = request.user.email
    requested_by_user = comment.content_object.requested_by.email
    first_name =  request.user.first_name
    job_id = comment.content_object.id
    last_name = request.user.last_name
    full_url = request.get_full_path()
    print(full_url)
    subject = "A comment was added to PRF: {}".format(comment.content_object)
    message = """
    A comment has been posted by {0} {1}.
    The comment reads as follows:
    {2}
    click here to see the comment:
    http://0.0.0.0:8000/jobs/all-jobs/{3}

    """.format(first_name, last_name, comment.comment, job_id)
    from_email = settings.DEFAULT_FROM_EMAIL
    # profile.save()
    send_mail(
        'A comment was added to ',
        message,
        from_email,
        [sender, requested_by_user],
        fail_silently=False,
    )

comment_was_posted.connect(comment_handler, sender=Comment)