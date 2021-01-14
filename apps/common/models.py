import uuid

from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.admin.options import get_content_type_for_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from apps.common.middleware import get_current_user


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, deleted_at=None)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='%(class)s_created_by',
                                   null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='%(class)s_updated_by',
                                   null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='%(class)s_deleted_by',
                                   null=True)
    objects = BaseManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.deleted_by = get_current_user()
        super(BaseModel, self).save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.created_at is None:
            self.created_by = get_current_user()
        else:
            self.updated_by = get_current_user()
        super(BaseModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True


def log_addition(object):
    return LogEntry.objects.create(
        user_id=object.created_by.id,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=ADDITION,
        change_message='add',
    )


def log_change(object):
    return LogEntry.objects.create(
        user_id=object.updated_by.id,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=CHANGE,
        change_message='update',
    )


def log_deletion(objects):
    return LogEntry.objects.create(
        user_id=objects.deleted_by.id,
        content_type_id=get_content_type_for_model(objects).pk,
        object_id=objects.pk,
        object_repr=str(objects),
        action_flag=DELETION,
    )


@receiver(post_save)
def post_save_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, BaseModel):
        if created:
            log_addition(instance)
        elif instance.deleted_at:
            log_deletion(instance)
        else:
            log_change(instance)
