from ast import Try
import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User,Book,Cart,Customer

#---------Exporting CSV FILES:-----------#
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
class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name','email','phone','date_created')
    actions = ["export_as_csv"]

class CartAdmin(admin.ModelAdmin, ExportCsvMixin):
    #list_display = ('customer', 'books') //ManytoMany: Can't be selected
    actions = ["export_as_csv"]

class BookAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title','Author','Price','Edition','date_created')
    actions = ["export_as_csv"]

#-----------Creating Custom User----------#
class UserAdmin(BaseUserAdmin,  ExportCsvMixin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin','is_active')
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
    actions = ["export_as_csv"]
    

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Cart, CartAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Book ,BookAdmin)
