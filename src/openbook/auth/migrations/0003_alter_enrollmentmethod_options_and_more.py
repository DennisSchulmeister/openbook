# Generated by Django 5.2.1 on 2025-05-28 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('openbook_auth', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrollmentmethod',
            options={'permissions': (('self_enroll', 'Can self-enroll in a scope'),), 'verbose_name': 'Enrollment Method', 'verbose_name_plural': 'Enrollment Methods'},
        ),
        migrations.AlterField(
            model_name='permission_t',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='auth.permission', verbose_name='Permission'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='openbook_auth.group', verbose_name='Groups'),
        ),
    ]
