from datetime import datetime
from django.db import models
    
class Reserva(models.Model):
    nome_cliente = models.CharField(verbose_name="Nome completo", max_length=100)
    telefone = models.CharField(max_length=20)

    data = models.DateField()
    horario = models.TimeField() #Confirmar com o CLiente os horarios de funcionamento

    num_pessoas = models.IntegerField(default=1) #Confirmar com o CLiente o limite max de pessoas

    status = models.CharField(max_length=20, 
        choices=[
            ("pendente", "Pendente"), 
            ("confirmada", "Confirmada"), 
            ("cancelada","Cancelada")], 
        default="Pendente") # Confirmar com o Cliente como deve funcionar essa confirmação.

    criado_em = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.nome_cliente} - {self.data} {self.horario}"
