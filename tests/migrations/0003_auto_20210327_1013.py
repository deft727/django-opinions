# Generated by Django 3.1.7 on 2021-03-27 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_auto_20210327_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='create_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tests.tests'),
        ),
    ]
