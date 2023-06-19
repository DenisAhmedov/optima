from rest_framework import permissions

from config.settings import ALLOWED_ADDRESSES


class IsAllowedAddress(permissions.BasePermission):
    """
    Разрешает доступ к API с определенных адресов
    """

    def has_permission(self, request, view):
        return request.META.get('REMOTE_ADDR') in ALLOWED_ADDRESSES
