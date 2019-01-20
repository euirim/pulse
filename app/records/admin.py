from django.contrib import admin

from .models import Record

# Register your models here.
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    search_fields = ['pk']
    date_hierarchy = 'time_created'
    autocomplete_fields = ['keyphrase']

    list_display = ('keyphrase', 'time_created')
    list_select_related = True
    readonly_fields = ('time_created',)

    list_per_page = 25
    list_max_show_all = 100