# System modules
import datetime
import uuid

# Django modules
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import pre_delete, post_save
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

# 3rd party modules
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission

# Lablup modules
from entry.models import Entry
from talkativot.permission import PermissionAlias, get_group_name

def get_default_user_slug_text_url(user):
    username = user.get_username()
    return slugify(username)


class UserProfile(models.Model):
    """ User profile model.

    :param models.Model: django.db.models.Model object
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    profile_photo = models.ImageField(upload_to='profiles', blank=True)
    birthday = models.DateTimeField(
        default=timezone.make_aware(datetime.datetime(1970, 1, 1), timezone.get_current_timezone()), blank=True)
    gender = models.CharField(max_length=10, default="unknown")
    join_date = models.DateTimeField(auto_now_add=True)
    logincount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    about_me = models.CharField(max_length=300, default='')
    username_changed = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=32, default='')
    #: Parent account
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="children",
                               blank=True, null=True)
    #: Default manager.
    objects = models.Manager()

    @property
    def fullname(self):
        """ Full name: first name + last name.
        """
        return "%s %s" % (self.user.first_name, self.user.last_name)


class UserPreference(models.Model):
    """ User preference model.

    :param models.Model: django.db.models.Model object
    """
    #: One-to-One relationship to a user. A user can access the profile through ``user.preference``.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="preference")
	#: Site key. ``Site`` model
    site = models.ForeignKey(Site, related_name="preference", blank=True)
    #: Default manager.
    objects = models.Manager()
    class Meta:
        """ Includes permissions for user model
        """
        #: A preferences can belong to unique (user, entry) pair.
        unique_together = ("user", "site")


class Friendship(models.Model):
    """ User friendship model.

    :param models.Model: django.db.models.Model object
    """
    #: Many-to-One relationship to a user. A user can access the friendship through ``user.my_friend``.
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="my_friend")
    #: Many-to-One relationship to a user. A user can access the friendship through ``user.friend_of``.
    friend_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friend_of")
    create_date = models.DateTimeField(auto_now_add=True)
    #: Default manager.
    objects = models.Manager()

    class Meta:
        """ Includes permissions for user model
        """
        #: A bookmark can belong to unique (user, entry) pair.
        unique_together = ("user_id", "friend_id")



def create_user_profile(sender, instance, created, **kwargs):
    """ Create profile and preference upon user creation (``post_save.connect``).

    :param sender: sender object
    :param instance: user instance
    :param created: user creation flag
    :param kwargs: dictionary argument
    :return: None
    """
    if created:
        user = instance
        # Create profile / preference objects for user
        profile, created = UserProfile.objects.get_or_create(user=instance)
        preference, created = UserPreference.objects.get_or_create(user=instance,
                                                                   site=Site.objects.get_current())
        # User automatically belongs to meta_all_members
        g, c = Group.objects.get_or_create(name=PermissionAlias.all)
        user.groups.add(g)


def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    """ Remove user's permissions upon user deletion (``pre_delete.connect``).

    :param sender: sender object
    :param instance: user instance
    :param kwargs: dictionary argument
    :return: None
    """
    filters = Q(content_type=ContentType.objects.get_for_model(instance),
                object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()

    if instance.profile:
        instance.profile.delete()
    if instance.preference:
        for i in instance.preference.all():
            i.delete()


def remove_menu_cache(sender, instance, **kwargs):
    cache.delete('menu_count_' + str(instance.user.id))


pre_delete.connect(remove_obj_perms_connected_with_user, sender=settings.AUTH_USER_MODEL)
post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
