# Generated by Django 5.0.4 on 2024-05-20 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_alter_forumpost_postdate_alter_forumpost_postimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumpost',
            name='postDate',
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='postTime',
        ),
    ]
