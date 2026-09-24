from django.db import migrations, models
from django.db.models import Max


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_defer_post_file_order_constraint"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="number",
            field=models.IntegerField(verbose_name="Number"),
        ),

        migrations.AddConstraint(
            model_name="post",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(is_draft=True, number__lte=0)
                    | models.Q(is_draft=False, number__gt=0)
                ),
                name="post_number_sign_matches_draft_status",
            ),
        ),
    ]
