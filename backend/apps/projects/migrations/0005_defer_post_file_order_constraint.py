from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0004_post_is_draft"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="postfile",
            name="unique_file_order_per_post",
        ),
        migrations.AddConstraint(
            model_name="postfile",
            constraint=models.UniqueConstraint(
                fields=("post", "order"),
                name="unique_file_order_per_post",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ),
    ]
