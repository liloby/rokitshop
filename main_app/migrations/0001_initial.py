# Generated by Django 4.0.6 on 2022-07-17 07:29

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

            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.CharField(max_length=1000)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField(verbose_name='Upload Date')),
                ('description', models.TextField(max_length=250)),
                ('posted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),

            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('signup_date', models.DateTimeField(auto_now_add=True, verbose_name='Signup Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),

            ],
        ),
    ]
