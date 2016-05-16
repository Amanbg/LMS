from django.contrib import admin

# Register your models here.
from comment.models import Comment
from leads.models import Lead
from users.models import MyUser


class CommentsAdmin(admin.ModelAdmin):
    fieldsets = (
            'Comments Details', {
                            'fields': ('description', 'lead', 'package_offered', 'created_by')
        }),

    list_display = ['description', 'lead', 'package_offered', 'created_by']
    list_filter = ['lead', 'package_offered', 'created_by']

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = MyUser.objects.filter(created_by=request.user)
        return super(CommentsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# admin.site.register(Comment, CommentsAdmin)
