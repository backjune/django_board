# Generated by Django 4.2.4 on 2023-09-02 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_rename_like_postlike_alter_postlike_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postlike',
            old_name='user_id',
            new_name='user',
        ),
    ]
