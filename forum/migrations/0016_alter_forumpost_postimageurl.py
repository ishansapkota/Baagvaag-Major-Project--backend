# Generated by Django 5.0.4 on 2024-06-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_alter_forumpost_postdate_alter_forumpost_posttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='postImageURL',
            field=models.CharField(blank=True, null=True),
        ),
    ]
