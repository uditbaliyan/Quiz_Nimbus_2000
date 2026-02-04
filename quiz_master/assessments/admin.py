# Register your models here.
# blog/admin.py
from django.contrib import admin

from .models import Subject
from .models import Topic

admin.site.register(Subject)
admin.site.register(Topic)
