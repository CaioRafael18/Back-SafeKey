# Generated by Django 5.1.4 on 2025-03-08 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safekey', '0013_reservation_responsible_reservation_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='status_key',
            field=models.CharField(choices=[('Retirada', 'Retirada'), ('Devolvida', 'Devolvida')], default='Retirada', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Recusado', 'Recusado'), ('Encerrado', 'Encerrado')], default='Aprovado', editable=False, max_length=20),
        ),
    ]
