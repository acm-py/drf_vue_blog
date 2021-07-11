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
from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户登录序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'password',
            'is_superuser'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'lastname',
            'firstname',
            'email',
            'last_login',
            'date_joined'
        ]


class UserDescSerializer(serializers.ModelSerializer):
    """
    文章列表中引用的嵌套序列化器
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined'
        ]

