from argparse import Action
import csv
from importlib.metadata import files
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User,Book,Cart,Customer


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

#---------Exporting CSV FILES:-----------#
Action = ['Export_Selected_Files']

def Export_Selected_Files(self, request, queryset):
    pass
Export_Selected_Files.short_description = "Export Selected"

import csv
from django.http import HttpResponse, response
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv') 
        response['Content-Disposition'] = 'attachment; filename = export.csv'.format(meta) 
        writer = csv.writer(response)
        writer.writerow(field_names) 
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names]) 
        return response
    export_as_csv.short_description = "Export Selected"
class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name", "is_immortal", "category", "origin", "is_very_benevolent")
    list_filter = ("is_immortal", "category", "origin", "IsVeryBenevolentFilter")
    actions = ["export_as_csv"]

class VillainAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name", "category", "origin")
    actions = ["export_as_csv"]
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Customer)
