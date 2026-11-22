from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("链接", max_length=200, unique=True, blank=True)
    summary = models.CharField("摘要", max_length=300, blank=True)
    content = models.TextField("正文（支持 Markdown 图片/链接：从 ImgBed 复制 MarkDown 格式粘贴即可）")
    is_published = models.BooleanField("已发布", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # 中文标题 slugify 会变空，兜底用 id 占位，保存后再补一次
            self.slug = slugify(self.title) or "post"
        super().save(*args, **kwargs)
        if self.slug == "post":
            self.slug = f"post-{self.pk}"
            super().save(update_fields=["slug"])

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
