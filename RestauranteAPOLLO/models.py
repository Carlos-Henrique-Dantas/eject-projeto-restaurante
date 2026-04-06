from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Mesa(models.Model):
    """Mesas cadastradas pelos funcionários"""
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
            ("cancelada", "Cancelada"),
        ],
        default="Pendente"
    )
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
        if self.num_pessoas < 1:
            raise ValidationError("O número de pessoas deve ser pelo menos 1.")
        if self.mesa and self.num_pessoas > self.mesa.capacidade:
            raise ValidationError(f"Mesa {self.mesa.numero} comporta no máximo {self.mesa.capacidade} pessoas.")


class ConfiguracaoSite(models.Model):
    nome_restaurante = models.CharField(max_length=100, default='Restaurante APOLLO')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    horario_funcionamento = models.TextField(blank=True)
    sobre_texto = models.TextField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'

    def __str__(self):
        return self.nome_restaurante


class SecaoHome(models.Model):
    TIPO_CHOICES = [
        ('banner', 'Banner principal'),
        ('destaque', 'Destaque'),
        ('texto_imagem', 'Texto com imagem'),
    ]
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='secoes/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto_imagem')
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Seção da Home'
        verbose_name_plural = 'Seções da Home'
        ordering = ['ordem']

    def __str__(self):
        return self.titulo


class ItemCardapio(models.Model):
    CATEGORIA_CHOICES = [
        ('entradas', 'Entradas'),
        ('principais', 'Pratos Principais'),
        ('sobremesas', 'Sobremesas'),
        ('bebidas', 'Bebidas'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='principais')
    imagem = models.ImageField(upload_to='cardapio/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Item do Cardápio'
        verbose_name_plural = 'Itens do Cardápio'
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f'{self.nome} - R$ {self.preco}'