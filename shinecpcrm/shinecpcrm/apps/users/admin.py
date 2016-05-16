from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
#from posts.models import Post   #since admin and models are inside the same app,we can use .models instead of posts.models
from users.models import MyUser


class MyUserAdmin(UserAdmin):
    search_fields = ['empid', 'username']
    list_filter = ["role"]
    fieldsets = (
            (None, {
                'fields': ('username', 'password', 'first_name', 'last_name', 'empid', 'email', 'phoneno', 'role', 'is_active', 'is_staff', 'groups', 'report', 'date_joined', 'last_login'),
                }),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'empid'),
        }),
    )

    list_display = ['empid', 'username', 'email', 'is_active', 'role', 'created_by']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        try:
            obj.created_by = request.user
        except:
            print "kuch gadbad hai !"
            pass

        return super(MyUserAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(MyUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs1 = qs.filter(created_by=request.user)
        qs2 = qs.filter(pk=request.user.pk)
        result = qs2 | qs1  # | is set Union not Bitwise OR
        return result.distinct()


admin.site.register(MyUser, MyUserAdmin)
