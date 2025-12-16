from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import UserPassesTestMixin
def login_superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user  is logged in and if the user is a superuser, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u:  u.is_superuser and u.is_active,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
class SuperuserRequiredMixin(UserPassesTestMixin):
      """Mixin that requires the user to be a superuser."""
      def test_func(self):
           return  self.request.user.is_superuser 