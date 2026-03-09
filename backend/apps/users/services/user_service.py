
from apps.users.models import User,Credit

def create_user(data):
    user = User.objects.create_user(**data)
    
    Credit.objects.create(
        user = user,
        total_credits = 0
    )
    
    return 0