# Generated by Django 5.0.4 on 2024-05-23 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_forumpost_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='postImage',
            field=models.TextField(null=True),
        ),
    ]
