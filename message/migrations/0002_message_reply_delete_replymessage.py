# Generated by Django 5.0 on 2023-12-13 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='message.message', verbose_name='reply'),
        ),
        migrations.DeleteModel(
            name='ReplyMessage',
        ),
    ]