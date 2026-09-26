from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
#from funcionario.models import Funcionario
import uuid
#from cloudinary.models import CloudinaryField
def get_file_path(_instance, filename):
    name = filename.split('.')[0] 
    ext = filename.split('.')[-1]
    filename = f'pratos/{name}-{uuid.uuid4()}.{ext}'
    return filename

class Prato(models.Model):
    nome_prato = models.CharField(max_length=100)
    ingredientes = models.TextField()
    modo_preparo = models.CharField()
    tempo_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=10)
    categoria = models.CharField(max_length=100)
    date_prato = models.DateTimeField(default=datetime.now, blank=True)
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    '''foto_prato = CloudinaryField(
        'foto_do_prato', 
        folder='canesgril_pratos', #NOME DA PASTA DENTRO DO CLOUDINARY
        transformation={ #redimencionamento da imagem
            'width': 600,
            'crop': 'limit',#Outras opções: 'fill', 'scale', 'fit', 'pad'
        },
        blank=True,
        null=True
    )'''

    def __str__(self):
        return f'{self.nome_prato}-{self.categoria}'