# Generated by Django 4.0.7 on 2023-06-07 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmapp', '0022_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='parent_category',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='parent_subcategory',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
