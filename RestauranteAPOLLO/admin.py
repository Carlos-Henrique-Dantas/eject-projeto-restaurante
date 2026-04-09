from django.contrib import admin
from .models import Mesa, Reserva
from .models import Post

admin.site.register(Mesa)
admin.site.register(Reserva)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'publicado_em', 'ativo')
    list_filter = ('ativo', 'publicado_em')
    search_fields = ('titulo', 'conteudo')

# Register your models here.
