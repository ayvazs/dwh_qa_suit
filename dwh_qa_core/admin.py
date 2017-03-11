from django.contrib import admin
from .models import Connection, TestSet, Test
# Register your models here.

admin.site.register(Connection)
admin.site.register(TestSet)
admin.site.register(Test)
