# Generated by Django 3.0.4 on 2020-07-13 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosasAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=64)),
                ('email', models.EmailField(default='', max_length=64)),
                ('password', models.CharField(default='', max_length=64)),
                ('image', models.ImageField(default='', null=True, upload_to='Users')),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
