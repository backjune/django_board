# Generated by Django 4.2.4 on 2023-09-02 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0014_alter_like_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='PostLike',
        ),
        migrations.AlterModelTable(
            name='postlike',
            table='post_like',
        ),
    ]