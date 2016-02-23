# import the User object
from models import Member

class CustomBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        try:
            # Try to find a user matching your username
            user = Member.objects.get(username=username)

            if password == user.password:
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except Member.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None
