# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     permissions
   Description :
   Author :       bing
   date：          2021/7/10
-------------------------------------------------
   Change Activity:
                   2021/7/10:
-------------------------------------------------
"""
__author__ = 'bing'
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user

