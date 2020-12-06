from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_vlue(self, user, timestamp):
        return (text_type(user.is_activate)+text_type(user.pk)+text_type(timestamp))

generate_token=TokenGenerator()