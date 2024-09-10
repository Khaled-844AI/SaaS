# Generated by Django 5.0.8 on 2024-09-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.group')),
                ('permissions', models.ManyToManyField(limit_choices_to={'codename__in': ['basic', 'advanced', 'pro', 'basic_ai'], 'content_type__app_label': 'subscriptions'}, to='auth.permission')),
            ],
            options={
                'permissions': [('advanced', 'Advanced Perm'), ('pro', 'Pro Perm'), ('basic', 'Basic Perm'), ('basic_ai', 'Basic_AI Perm')],
            },
        ),
    ]
