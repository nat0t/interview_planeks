# Generated by Django 3.2.5 on 2021-08-02 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('delimiter', models.CharField(choices=[('CM', 'Comma (,)'), ('TB', 'Tabulation ( )'), ('SP', 'Space ( )'), ('CL', 'Colon (:)'), ('SC', 'Semicolon (;)')], default='CM', max_length=2)),
                ('quotes', models.CharField(choices=[('QT', "Quote (')"), ('DQ', 'Double-quote (")')], default='DQ', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchemaDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(choices=[('DF', '-----'), ('FN', 'Full name'), ('JB', 'Job'), ('EM', 'E-mail'), ('PN', 'Phone number'), ('IT', 'Integer'), ('DT', 'Date')], default='DF', max_length=2)),
                ('order', models.PositiveSmallIntegerField()),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schema')),
            ],
        ),
    ]