# Generated by Django 4.0.6 on 2022-07-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=10),
        ),
    ]
