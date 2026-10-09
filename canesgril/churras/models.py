import os
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

def get_file_path(instance, filename: str) -> str:
    """Gera um caminho de arquivo seguro e único com base em UUID."""
    ext = os.path.splitext(filename)[1]
    return f'pratos/{uuid.uuid4()}{ext}'

class Prato(models.Model):
    """Modelo que representa um prato ou receita de churrasco."""
    
    nome_prato = models.CharField(max_length=100, verbose_name="Nome do Prato")
    ingredientes = models.TextField(verbose_name="Ingredientes")
    modo_preparo = models.TextField(verbose_name="Modo de Preparo")
    tempo_preparo = models.PositiveIntegerField(verbose_name="Tempo de Preparo (min)")
    rendimento = models.CharField(max_length=10, verbose_name="Rendimento")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    date_prato = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Data de Criação")
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Funcionário Responsável")
    publicado = models.BooleanField(default=False, verbose_name="Publicado")
    
    # ALTERADO: Transformação agressiva para padronização de UI e otimização de banda
    foto_prato = CloudinaryField(
        'foto_do_prato', 
        folder='canesgril_pratos',
        transformation={
            'width': 800,
            'height': 600,
            'crop': 'fill',      # Preenche o quadro 800x600 e recorta o excesso
            'gravity': 'center', # Mantém o foco no centro da imagem original
            'quality': 'auto',   # Compressão sem perda visual
            'fetch_format': 'auto' # Entrega em WebP ou AVIF
        },
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "Prato"
        verbose_name_plural = "Pratos"
        ordering = ['-date_prato']

    def __str__(self) -> str:
        return f'{self.nome_prato} - {self.categoria}'