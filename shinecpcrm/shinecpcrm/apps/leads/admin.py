from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from leads.models import Lead
from users.models import MyUser
from comment.models import Comment
from category.models import Category


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class LeadAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Lead Information', {
                        'fields': ('username', 'email_id', 'name', 'source', 'salary')
                    }),
        ('Address', {
                        'fields': ('city', 'contact')
                    }),
        ('Experience', {
                'fields': ('experience_years', 'experience_level', 'industry')
                    }),
        ('Product details', {
                    'fields': ('product_name',)
                    }),
        ('Caller details', {
                    'fields': ('assign_to',)
                    })
        )

    search_fields = ['username', 'product_name', 'industry']
    list_display = ['username', 'email_id', 'name', 'source', 'industry', 'assign_to', 'created_by']
    list_filter = ['assign_to', 'created_by']

    inlines = [CommentInline, CategoryInline, ]
# function : team leader can see only those caller which he creates..but superuser
# can see all whether he creates or not

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "assign_to":
            if request.user.is_superuser:
                return super(LeadAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            kwargs["queryset"] = MyUser.objects.filter(created_by=request.user)
        return super(LeadAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        try:
            obj.created_by = request.user
        except:
            print "kuch gadbad hai !"
            pass

        return super(LeadAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(LeadAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs1 = qs.filter(created_by__in=(MyUser.objects.filter(groups__name="Team Leader" or "Caller")))
        return qs1


admin.site.register(Lead, LeadAdmin)
