# Generated by Django 3.2.6 on 2021-08-21 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_delete_usersocialmedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='credits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
