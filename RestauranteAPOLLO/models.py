from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Mesa(models.Model): # Mesas cadastrada pelos funcionarios
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número da Mesa")
    capacidade = models.PositiveIntegerField(default=1, validators="Capacidade máxima")
    disponivel = models.BooleanField(default=True, verbose_name="Dísponivel")

    class Meta():
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidade} pessoas)."

class Reserva(models.Model):
    nome = models.CharField(verbose_name="Nome completo", max_length=100)
    data = models.DateField(verbose_name="Data da Reserva")
    horario = models.TimeField(verbose_name="Horário") #Confirmar com o CLiente os horarios de funcionamento
    num_pessoas = models.PositiveIntegerField(default=1, verbose_name="Número de Pessoas") #Confirmar com o CLiente o limite max de pessoas
    status = models.CharField(max_length=20, 
        choices=[
            ("pendente", "Pendente"), 
            ("confirmada", "Confirmada"), 
            ("cancelada","Cancelada")], 
        default="Pendente") # Confirmar com o Cliente como deve funcionar essa confirmação.
    criado_em = models.DateTimeField(auto_now_add=True)
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, null=True, blank=True, verbose_name= "Mesa Atribuida")

    class Meta():
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-data', 'horario']

    def __str__(self):
        if self.mesa:
            return f"{self.nome} - Mesa {self.mesa.numero} - {self.data} {self.horario}"
        return f"{self.nome} - Mesa não atribuída - {self.data} {self.horario}"

    def clean(self):
        if self.data < timezone.now().date():
            raise ValidationError("Não é possível realizar reserva para datas passadas.") 
        
        if self.num_pessoas < 1:
            raise ValidationError("O número de pessoas deve ser pelo menos 1.")