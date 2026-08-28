from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_alter_project_post_list_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_draft",
            field=models.BooleanField(default=False, verbose_name="Draft"),
        ),
    ]
