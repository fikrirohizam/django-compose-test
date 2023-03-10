# Generated by Django 4.1.6 on 2023-02-24 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catwiki', '0007_alter_cat_cat_breed_alter_cat_cat_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='cat_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_cats', to='catwiki.human'),
        ),
    ]
