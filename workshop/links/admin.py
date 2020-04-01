"""
    Admin pages registrations
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import IntegrityError
from django.db.models import Q
from django.utils.html import escape, format_html
from django.utils.translation import ugettext as _

from .constant import DEFAULT_SCREENSHOT_FILE
from .models import Link, Tag, LinkTag


class LinkTagInline(admin.TabularInline):
    """
        Inline input for link-tag relationship
    """
    model = LinkTag


def take_screenshot(modeladmin, request, queryset):
    for link in queryset:
        link.take_screenshot()
take_screenshot.short_description = "Take screenshots"


class FullFilter(SimpleListFilter):
    title = 'full'
    parameter_name = 'full'

    def lookups(self, request, model_admin):
        return [('full', 'Completo'), ('incomplete', 'Incompleto')]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            if value == 'full':
                return queryset.exclude(screenshot=DEFAULT_SCREENSHOT_FILE).exclude(status=Link.CHECK)
            return queryset.filter(Q(screenshot=DEFAULT_SCREENSHOT_FILE) | Q(status=Link.CHECK))
        return queryset


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
        Link model registration in Django admin
    """
    inlines = [LinkTagInline]
    list_filter = (FullFilter, 'status', 'pending', 'stars', 'tags',)
    list_display = ('name', 'full', 'status', 'stars', 'pending', 'get_tags', 'link', 'screenshot_preview',)
    fields = (
        'name', 'status', 'url',
        'stars', 'pending', 'description',
        'user', 'screenshot', 'screenshot_preview',
    )
    readonly_fields = ('screenshot_preview',)
    actions = [take_screenshot]

    def get_tags(self, instance):
        return '\n'.join([tag.name for tag in instance.tags.all()])

    def link(self, instance):
        return format_html('<a href="{}">{}</a>'.format(instance.url, instance.url[:100]))
    link.allow_tags = True

    def screenshot_preview(self, instance):
        return format_html('<img src="{}" width="200px" />'.format(escape(instance.screenshot.url)))
    screenshot_preview.short_description = _('Screenshot')
    screenshot_preview.allow_tags = True


def merge_similars(modeladmin, request, queryset):
    for tag in queryset:
        similars = tag.get_similars()
        for similar in similars:
            for link_tag in similar.linktag_set.all():
                try:
                    new_link_tag = LinkTag.objects.create(link=link_tag.link, tag=tag)
                    new_link_tag.save()
                except IntegrityError:
                    pass
                link_tag.delete()
merge_similars.short_description = "Merge similars tags"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
        Tag model registration in Django admin
    """
    list_display = ('name', 'links_quantity', 'unused', 'similars', 'description',)
    actions = [merge_similars]
