from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin, UserPassesTestMixin, \
    PermissionRequiredMixin as BasePermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(BaseLoginRequiredMixin):
    login_url = '/contas/login/'
    redirect_field_name = 'next'


class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """
    group_required = tuple()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0 and len(self.group_required) > 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(UserPassesTestMixin, BasePermissionRequiredMixin):
    raise_exception = True

    permission_required = ()
    group_required = ()

    def test_func(self):
        if not getattr(self, 'group_required', None):
            return True

        if self.request.user.groups.filter(name__in=self.group_required).exists():
            return True

        return False
