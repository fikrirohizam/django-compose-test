# Generated by Django 4.1.6 on 2023-02-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catwiki', '0002_alter_breed_breed_name_alter_cat_cat_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
