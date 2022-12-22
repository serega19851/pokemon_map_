# Generated by Django 3.1.14 on 2022-12-19 08:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='pokemons')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(blank=True)),
                ('lon', models.FloatField(blank=True)),
                ('appeared_at', models.DateTimeField(default=datetime.datetime(2022, 12, 19, 11, 1, 57, 578504))),
                ('disappeared_at', models.DateTimeField(default=datetime.datetime(2022, 12, 19, 11, 1, 57, 578527))),
                ('level', models.IntegerField(default=0)),
                ('health', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('defence', models.IntegerField(default=0)),
                ('stamina', models.IntegerField(default=0)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
    ]
