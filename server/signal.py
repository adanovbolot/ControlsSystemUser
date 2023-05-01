from django.contrib.auth.signals import user_logged_in, user_logged_out
from server.models import UserAccess
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import User, UserSession


@receiver(pre_save, sender=User)
def update_user_session_access(sender, instance, **kwargs):
    if instance.pk:
        try:
            user_sessions = UserSession.objects.filter(user=instance)
            user_sessions.update(access=instance.access)
        except UserSession.DoesNotExist:
            pass


@receiver(post_save, sender=UserSession)
def update_user_access_from_session(sender, instance, created, **kwargs):
    try:
        user = instance.user
        user.access = instance.access
        user.save()
        if instance.access:
            request = kwargs.get('request')
            if request:
                logout(request)
            Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key__in=Session.objects.filter(
                    session_data__contains=str(instance.id)
                ).values_list('session_key', flat=True)
            ).delete()
    except User.DoesNotExist:
        pass


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    from .models import User
    user_instance = User.objects.get(id=user.id)
    user_instance.status = True
    user_instance.save()


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    from .models import User
    user_instance = User.objects.get(id=user.id)
    user_instance.status = False
    user_instance.save()


@receiver(post_save, sender=User)
def create_user_access(sender, instance, created, **kwargs):
    if created:
        UserAccess.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_session(sender, instance, created, **kwargs):
    if created:
        UserSession.objects.create(user=instance)
