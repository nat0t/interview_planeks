from django.contrib import admin

from main.models import Schema, SchemaDetails, Dataset

admin.site.register(Schema)
admin.site.register(SchemaDetails)
admin.site.register(Dataset)
