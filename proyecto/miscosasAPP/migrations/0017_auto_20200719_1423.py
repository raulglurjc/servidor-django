# Generated by Django 3.0.4 on 2020-07-19 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosasAPP', '0016_auto_20200719_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database_users',
            name='image',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to='Usuario'),
        ),
    ]
