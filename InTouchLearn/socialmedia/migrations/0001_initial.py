# Generated by Django 5.0.3 on 2024-03-20 14:26

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="uploads/post_photos"
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True, null=True, upload_to="uploads/post_videos"
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dislikes",
                    models.ManyToManyField(
                        blank=True, related_name="dislikes", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField()),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dislikes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="comment_dislikes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="comment_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="socialmedia.comment",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialmedia.post",
                    ),
                ),
            ],
        ),
    ]
