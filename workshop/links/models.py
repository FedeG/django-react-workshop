"""
    Django models for link application
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _

from .constant import DEFAULT_SCREENSHOT_FILE
from .utils import is_similar, get_screenshot


class Tag(models.Model):
    """
        Tag model
    """
    name = models.CharField(_('name'), max_length=30, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey(
        User, verbose_name=_('user'), blank=True, null=True,
        on_delete=models.CASCADE)

    @property
    def links_quantity(self):
        return self.linktag_set.all().count()

    @property
    def similars(self):
        return self.get_similars()

    @property
    def unused(self):
        return self.links_quantity == 0

    def __str__(self):
        return self.name

    def get_similars(self):
        """
            Return similars tags (search for name)
        """
        tags = Tag.objects.all().exclude(pk=self.pk)
        similars = [tag for tag in tags if is_similar(self.name, tag.name)]
        return similars

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Link(models.Model):
    """
        Link model
    """
    ONLINE = 'ON'
    OFFLINE = 'OFF'
    CHECK = 'NEW'
    ERROR = 'ERR'
    STATUS_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
        (ERROR, 'Error'),
        (CHECK, 'Check'),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=CHECK,
    )
    name = models.CharField(_('name'), max_length=30)
    url = models.URLField(_('url'), unique=True)
    pending = models.BooleanField(_('pending'), default=True)
    description = models.TextField(_('description'), blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='LinkTag', editable=True)
    user = models.ForeignKey(User, verbose_name=_('user'),
                             on_delete=models.CASCADE)
    stars = models.IntegerField(
        _('stars'),
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    screenshot = models.ImageField(
        _('screenshot'),
        upload_to='screenshot/',
        default=DEFAULT_SCREENSHOT_FILE
    )

    @property
    def full(self):
        checked = self.status != Link.CHECK
        has_screenshot = self.screenshot.name != DEFAULT_SCREENSHOT_FILE
        return checked and has_screenshot

    def take_screenshot(self, force=False):
        if force or self.screenshot.name == DEFAULT_SCREENSHOT_FILE:
            filename = 'screenshot/{}-{}.png'.format(self.id, self.name)
            full_path = '{}/{}'.format(settings.MEDIA_ROOT, filename)
            get_screenshot(self.url, full_path)
            self.screenshot = filename
            self.save()

    def __str__(self):
        return '{}({}): {}'.format(self.name, self.status, self.url)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')


class LinkTag(models.Model):
    """
    Model for link-tag relationship
    """
    link = models.ForeignKey(Link, verbose_name=_('link'),
                             on_delete=models.CASCADE)

    tag = models.ForeignKey(Tag, verbose_name=_('tag'),
                            on_delete=models.CASCADE)


    class Meta:
        unique_together = (('link', 'tag'))
        verbose_name = _('link x tag')
        verbose_name_plural = _('link x tag')
