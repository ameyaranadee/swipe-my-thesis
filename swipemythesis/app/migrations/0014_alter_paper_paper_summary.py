# Generated by Django 5.1.3 on 2024-11-10 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_paper_paper_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='paper_summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
