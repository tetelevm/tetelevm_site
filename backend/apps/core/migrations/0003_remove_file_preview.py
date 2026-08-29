from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_file_original_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="file",
            name="preview",
        ),
    ]
