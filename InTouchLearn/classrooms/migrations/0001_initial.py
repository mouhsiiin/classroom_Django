# Generated by Django 5.0.3 on 2024-03-27 16:43

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Classrooms",
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
                ("classroom_name", models.CharField(max_length=100)),
                ("section", models.CharField(default="Third Year", max_length=100)),
                ("class_code", models.CharField(default="0000000", max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Assignments",
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
                ("assignment_name", models.CharField(max_length=50)),
                ("due_date", models.DateField()),
                ("due_time", models.TimeField(default=datetime.time(10, 10))),
                ("posted_date", models.DateField(auto_now_add=True)),
                ("instructions", models.TextField()),
                ("total_marks", models.IntegerField(default=100)),
                (
                    "classroom_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.classrooms",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourseContent",
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
                ("content_title", models.CharField(max_length=50)),
                ("content_description", models.TextField()),
                ("content_file", models.FileField(upload_to="documents")),
                (
                    "classroom_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.classrooms",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Students",
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
                (
                    "classroom_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.classrooms",
                    ),
                ),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submissions",
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
                ("submitted_date", models.DateField(auto_now_add=True)),
                ("submitted_time", models.TimeField(auto_now_add=True)),
                ("submitted_on_time", models.BooleanField(default=True)),
                ("marks_alloted", models.IntegerField(default=0)),
                ("submission_file", models.FileField(upload_to="documents")),
                (
                    "assignment_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.assignments",
                    ),
                ),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.students",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Teachers",
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
                (
                    "classroom_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classrooms.classrooms",
                    ),
                ),
                (
                    "teacher_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
