# Generated by Django 4.0.1 on 2022-01-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
