# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     permissions
   Description :
   Author :       bing
   date：          2021/7/9
-------------------------------------------------
   Change Activity:
                   2021/7/9:
-------------------------------------------------
"""
__author__ = 'bing'
from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    管理员可以修改
    其他用户仅查看
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser