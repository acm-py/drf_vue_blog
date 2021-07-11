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
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'you must be the owner to update'

    def safe_methods_or_owner(self, request, func):
        if request.method in SAFE_METHODS:
            return True

        return func()

    def has_permission(self, request, view):
        return self.safe_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return self.safe_methods_or_owner(
            request,
            lambda: obj.author==request.user
        )