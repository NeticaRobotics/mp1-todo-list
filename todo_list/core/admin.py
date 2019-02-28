from django.contrib import admin
from .models import Card, UserData
# Register your models here.
class CardAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'description', 'importance', 'limit', 'finished')
    list_filter = ('author', 'name', 'created', 'finished', 'limit')
admin.site.register(Card, CardAdmin)


class UserDataAdmin(admin.ModelAdmin):
    fields = ('user', 'ocupation')
    list_filter = ('user', 'ocupation')
admin.site.register(UserData, UserDataAdmin)
