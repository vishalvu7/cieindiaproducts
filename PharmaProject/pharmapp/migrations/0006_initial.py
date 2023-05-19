# Generated by Django 4.0.7 on 2023-05-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pharmapp', '0005_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='pharmapp/static/images/')),
            ],
        ),
    ]