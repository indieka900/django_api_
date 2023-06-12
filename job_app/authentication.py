# from django.contrib.auth.backends import BaseBackend
# from .models import User

# class MongoDBBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(username=username)
#             print(username,password)
#             if user.password == password:
#                 return user
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
