from django.contrib import admin
from .models import Mesa, Reserva, ConfiguracaoSite, SecaoHome, ItemCardapio

admin.site.register(Mesa)
admin.site.register(Reserva)
admin.site.register(ConfiguracaoSite)
admin.site.register(SecaoHome)
admin.site.register(ItemCardapio)

# Register your models here.
