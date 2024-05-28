from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Major",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=30, unique=True, verbose_name="전공명"),
                ),
                (
                    "campus",
                    models.CharField(
                        choices=[("S", "서울"), ("G", "글로벌")],
                        max_length=1,
                        verbose_name="캠퍼스",
                    ),
                ),
                ("college", models.CharField(max_length=30, verbose_name="단과대학")),
            ],
            options={
                "db_table": "major",
            },
        ),
    ]
