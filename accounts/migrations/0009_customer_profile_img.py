# Generated by Django 3.0.5 on 2020-05-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200527_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
