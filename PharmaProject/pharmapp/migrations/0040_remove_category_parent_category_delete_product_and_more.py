# Generated by Django 4.0.7 on 2023-06-07 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmapp', '0039_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='parent_category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
