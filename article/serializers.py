# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     serializers
   Description :
   Author :       bing
   date：          2021/7/9
-------------------------------------------------
   Change Activity:
                   2021/7/9:
-------------------------------------------------
"""
__author__ = 'bing'
from rest_framework import serializers
from article.models import *
from user_info.serializers import UserDescSerializer
from comment.serializers import *


class AvatarSerializer(serializers.ModelSerializer):
    """
    图片序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    """

    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    分类的序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    # 自定义错误信息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here...'
    }
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    # # 新增每篇文章url字段
    # url = serializers.HyperlinkedIdentityField(view_name="article:detail")

    category = CategorySerializer(read_only=True)
    # 外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # category_id 验证

    # 添加tag字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )
    # 图片
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
    )

    # 验证图片id是否存在
    # def validate_avatar_id(self, value):
    #     if not Avatar.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError("Avatar with id {} not exists".format(value))
    #     return value
    #
    # def validate_category_id(self, value):
    #     if not Category.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError('Category with id {} not exists'.format(value))
    #     return value

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'
        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )
        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
         model=Category,
         value=value,
         message='incorrect_category_id'
        )
        return value

    # 覆写方法，如果输入的标签不存在就创建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)


class ArticleSerializer(ArticleBaseSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class ArticleDetailSerializer(ArticleBaseSerializer):
    # 经过md渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()
    # comment 字段
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    分类详情页
    """
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]

