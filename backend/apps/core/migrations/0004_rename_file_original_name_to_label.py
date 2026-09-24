from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_remove_file_preview"),
    ]

    operations = [
        migrations.RenameField(
            model_name="file",
            old_name="original_name",
            new_name="label",
        ),
        migrations.AlterField(
            model_name="file",
            name="label",
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name="Label",
            ),
        ),
    ]
