# Generated by Django 4.1.4 on 2022-12-27 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_usuario_cpf'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='carrinhoitem',
            index_together={('user', 'produto')},
        ),
    ]
