# Generated by Django 3.0.4 on 2020-07-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=64)),
                ('email', models.EmailField(default='', max_length=64)),
                ('password', models.CharField(default='', max_length=64)),
                ('image', models.ImageField(default='', null=True, upload_to='Users')),
                ('tamañoletra', models.CharField(default='', max_length=64)),
                ('estilo', models.CharField(default='', max_length=64)),
            ],
        ),
    ]