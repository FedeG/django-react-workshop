"""
from django.contrib import admin

# Register your models here.
"""

from django.contrib import admin
from .models import Link, Tag, LinkTag


class LinkTagInline(admin.TabularInline):
    model = LinkTag


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    inlines = [LinkTagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
