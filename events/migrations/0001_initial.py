# Generated by Django 4.2.7 on 2023-11-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('desc', models.CharField(max_length=1024)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]