from django.contrib import admin
from user_auth.models import CustomUser, Role, UserGroup

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(UserGroup)
