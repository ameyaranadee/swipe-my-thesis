# Generated by Django 5.1.3 on 2024-11-10 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_paper_paper_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='paper_recency',
            field=models.IntegerField(),
        ),
    ]
