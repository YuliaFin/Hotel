# Generated by Django 4.1.7 on 2023-05-17 20:30

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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_post', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_place', models.IntegerField()),
                ('additional_place', models.IntegerField()),
                ('date_of_arrival', models.DateField()),
                ('date_of_departure', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('name_room', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Type_room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='', max_length=32)),
                ('password_user', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=16)),
                ('surname', models.CharField(default='', max_length=32)),
                ('patronymic', models.CharField(default='', max_length=20)),
                ('email', models.CharField(default='', max_length=256)),
                ('phone_number', models.CharField(default='', max_length=17)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=32)),
                ('password_user', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=16)),
                ('surname', models.CharField(max_length=32)),
                ('patronymic', models.CharField(max_length=20)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.request')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
        ),
        migrations.CreateModel(
            name='Room_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_place', models.BooleanField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='main.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='type_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.type_room'),
        ),
        migrations.CreateModel(
            name='Request_Staffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.request')),
                ('staffer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staffer')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user'),
        ),
        migrations.CreateModel(
            name='occupancy_of_rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_arrival', models.DateField()),
                ('date_of_departure', models.DateField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
        ),
    ]