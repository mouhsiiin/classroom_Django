# Generated by Django 5.0.3 on 2024-03-23 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0003_alter_post_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="likes",
        ),
        migrations.RemoveField(
            model_name="post",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
    ]
