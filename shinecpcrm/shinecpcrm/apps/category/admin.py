from django.contrib import admin

# Register your models here.
from category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        'Category Information', {
                        'fields': ('category_name', 'sub_category', 'status')
        }),

    list_filter = ('category_name', 'sub_category')
    list_display = ('category_name', 'sub_category', 'status')

# admin.site.register(Category, CategoryAdmin)
