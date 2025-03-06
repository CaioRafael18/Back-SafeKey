from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Defina o padrão do Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('BACK-SAFEKEY')

# Carrega a configuração do Celery a partir das configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tarefas automaticamente da pasta safekey/tasks
app.autodiscover_tasks(['safekey.tasks'])
