# Generated by Django 4.0.6 on 2022-07-09 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_is_admin_user_is_staff_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]
