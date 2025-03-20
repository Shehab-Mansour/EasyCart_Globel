from rest_framework_simplejwt.tokens import RefreshToken
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_custom_user(cls, user, user_type):
        token = cls()
        token["user_id"] = user.id
        token["user_type"] = user_type  # إضافة نوع المستخدم
        return token