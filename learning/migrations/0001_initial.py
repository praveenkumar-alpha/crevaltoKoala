# Generated by Django 2.1.7 on 2019-03-14 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Vous pouvez utilisez la syntaxe <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown</a> ici.', verbose_name='Description')),
                ('state', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], default='DRAFT', max_length=20, verbose_name='State')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Published the')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last updated the')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writes', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'ordering': ['name'],
            },
        ),
    ]