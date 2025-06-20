# Generated by Django 5.2.2 on 2025-06-20 03:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('text_format', models.CharField(choices=[('TEXT', 'Plain Text'), ('HTML', 'HTML'), ('MD', 'Markdown')], default='MD', max_length=10, verbose_name='Text Format')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('is_template', models.BooleanField(default=False, help_text='Flag that this course is only used for creating other courses.', verbose_name='Is Template')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                ('owner', models.ForeignKey(blank=True, help_text='The owner always has full permissions.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('public_permissions', models.ManyToManyField(blank=True, help_text='Permissions available to logged-out users and all logged-in users independent of their role.', related_name='+', to='auth.permission', verbose_name='Public Permissions')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
    ]
