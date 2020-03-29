"""
    Admin pages registrations
"""

from django.contrib import admin
from django.db import IntegrityError
from django.utils.html import format_html

from .models import Link, Tag, LinkTag


class LinkTagInline(admin.TabularInline):
    """
        Inline input for link-tag relationship
    """
    model = LinkTag


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
        Link model registration in Django admin
    """
    inlines = [LinkTagInline]
    list_filter = ('status', 'pending', 'tags', 'stars',)
    list_display = ('name', 'status', 'stars', 'pending', 'get_tags', 'link',)

    def get_tags(self, instance):
        return '\n'.join([tag.name for tag in instance.tags.all()])

    def link(self, instance):
        return format_html('<a href="{}">{}</a>'.format(instance.url, instance.url))
    link.allow_tags = True


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
