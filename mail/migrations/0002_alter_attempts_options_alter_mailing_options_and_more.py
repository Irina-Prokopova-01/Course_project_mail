# Generated by Django 4.2.2 on 2024-12-12 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mail", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="attempts",
            options={
                "ordering": ["attempt_date", "attempt_status", "mailing"],
                "verbose_name": "попытка рассылки",
                "verbose_name_plural": "попытки рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "ordering": ["status", "message"],
                "permissions": [("can_finish_mailing", "can finish mailing")],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.AddField(
            model_name="attempts",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailing_attempts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailings",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="recipient",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
    ]