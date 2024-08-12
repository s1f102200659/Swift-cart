# Generated by Django 4.2.7 on 2023-12-03 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('category', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('seller_id', models.IntegerField(default=0)),
                ('comment', models.TextField()),
                ('image', models.ImageField(upload_to='img/')),
            ],
        ),
    ]
