from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=200, unique=True, verbose_name="链接"
                    ),
                ),
                (
                    "summary",
                    models.CharField(
                        blank=True, max_length=300, verbose_name="摘要"
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        verbose_name="正文（支持 Markdown 文本，页面按纯文本分段显示）"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="已发布"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
            },
        ),
    ]
