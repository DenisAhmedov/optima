from rest_framework import permissions

from config.settings import ALLOWED_ADDRESSES


class IsAllowedAddress(permissions.BasePermission):
    """
    Разрешает доступ к API с определенных адресов
    """

    def has_permission(self, request, view):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip in ALLOWED_ADDRESSES
