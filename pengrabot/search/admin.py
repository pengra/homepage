from django.contrib import admin
from search import models

# Register your models here.

class QueryAdmin(admin.ModelAdmin):
    list_display = ('query',)

    search_fields = ('query',)

class ResultAdmin(admin.ModelAdmin):
    search_fields = ('url',)

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'count', 'pages',)
    search_fields = ('word',)

admin.site.register(models.Query, QueryAdmin)
admin.site.register(models.Result, ResultAdmin)
admin.site.register(models.Word, WordAdmin)