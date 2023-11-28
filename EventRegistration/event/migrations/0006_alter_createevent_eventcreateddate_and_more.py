# Generated by Django 4.2.7 on 2023-11-28 14:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_createevent_eventcreateddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createevent',
            name='eventCreatedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='createevent',
            name='eventModifyDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='createDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='modifyDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]