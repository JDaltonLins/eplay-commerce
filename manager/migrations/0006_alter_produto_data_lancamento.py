# Generated by Django 4.1.3 on 2022-12-05 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_produto_data_lancamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='data_lancamento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Lançamento'),
        ),
    ]