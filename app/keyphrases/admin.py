from django.contrib import admin

from .models import Keyphrase

# Register your models here.
@admin.register(Keyphrase)
class KeyphraseAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_created'
    search_fields = ('name',)

    list_display = ('name', 'time_created', 'active', 'display')
    list_editable = ('display',)
    list_select_related = True
    readonly_fields = ('time_created',)

    list_per_page = 25
    list_max_show_all = 100