from django.contrib import admin

from .models import FileVersion, User, File

admin.site.register(File)
admin.site.register(FileVersion)
admin.site.register(User)
