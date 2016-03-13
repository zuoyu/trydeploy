from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import Author


class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (AuthorInline, )


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Author)
