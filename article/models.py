from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown
# Create your models here.


# 图片
class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


# 文章分类
class Category(models.Model):
    """
    文章分类
    """
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


# 标签模型
class Tag(models.Model):
    """
    文章标签
    """
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)

    # 作者，外键
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    # 标签 多对多
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )
    # 分类
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    # 标题图
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )

    # 将body征文转化为带markdown格式的文章
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc是渲染后的目录
        return md_body, md.toc

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title






