# Generated by Django 3.1.6 on 2021-02-02 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCodeConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('code', models.IntegerField()),
                ('check', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
