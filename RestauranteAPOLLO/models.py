from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Terão 28 mesas com capacidade para até 6 pessoas
class Mesa(models.Model): # Mesas cadastrada pelos funcionarios
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número da Mesa")
    capacidade = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Capacidade máxima"
    )
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidade} pessoas)."


class Reserva(models.Model):
    nome = models.CharField(verbose_name="Nome completo", max_length=100)
    data = models.DateField(verbose_name="Data da Reserva")
    horario = models.TimeField(verbose_name="Horário")
    num_pessoas = models.PositiveIntegerField(
        default=1,
        verbose_name="Número de Pessoas"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"), 
            ("confirmada", "Confirmada"), 
            ("cancelada","Cancelada")], 
        default="Pendente") 
    criado_em = models.DateTimeField(auto_now_add=True)
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Mesa Atribuída"
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
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
        
        data_hora_reserva = timezone.make_aware(timezone.datetime.combine(self.data, self.horario))
        if data_hora_reserva < timezone.now() + timedelta(minutes=30):
            raise ValidationError("As reservas devem ser feitas com pelo menos 30 minutos de antecedência.")

        if self.horario > timezone.datetime.strptime("21:00", "%H:%M").time():
            raise ValidationError("O horário máximo para reservas é até 21:00.")

        if self.num_pessoas < 1:
            raise ValidationError("O número de pessoas deve ser pelo menos 1.")
        
    def atribuir_mesa_automaticamente(self):  
        mesa_disponivel = Mesa.objects.filter(
            capacidade__gte=self.numero_pessoas,
            disponivel=True
        ).order_by('capacidade').first()

        if mesa_disponivel:
            self.mesa = mesa_disponivel
            self.status = 'confirmada'
        else:
            self.status = 'pendente'
            
