from django.contrib import admin
from .models import Database_Users,Alimentador,Item,Comentario,Voto
# Register your models here.
admin.site.register(Database_Users)
admin.site.register(Alimentador)
admin.site.register(Item)
admin.site.register(Comentario)
admin.site.register(Voto)
