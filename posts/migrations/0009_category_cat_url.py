# Generated by Django 2.1.5 on 2020-07-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20200621_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_url',
            field=models.CharField(default='cat', max_length=40),
        ),
    ]
