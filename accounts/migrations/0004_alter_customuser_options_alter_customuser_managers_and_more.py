# Generated by Django 4.0.1 on 2022-01-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_customuser_birth_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={},
        ),
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="birth_date",
        ),
        migrations.AddField(
            model_name="customuser",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[("admin", "Admin"), ("client", "Client")],
                default="client",
                help_text="Role (Admin, Client)",
                max_length=10,
            ),
        ),
    ]
