from __future__ import absolute_import, unicode_literals

# Garante que o Celery seja carregado assim que o Django for iniciado
from .celery import app as celery_app

__all__ = ('celery_app',)