# Generated by Django 3.2.7 on 2021-09-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]