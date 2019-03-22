# Generated by Django 2.1.7 on 2019-03-18 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leagueName', models.CharField(max_length=32)),
                ('startingBalance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('maxPlayers', models.IntegerField(default=15)),
            ],
        ),
    ]
