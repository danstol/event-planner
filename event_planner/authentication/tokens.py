from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            user.pk + timestamp + user.profile.email_verified
        )


account_activation_token = AccountActivationTokenGenerator()
