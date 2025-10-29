# create_users.py (프로젝트 루트에 생성)

import os
import django
import bcrypt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qb_backend.settings')
django.setup()

from api.models import User

def create_initial_users():
    """초기 사용자 생성"""
    users_data = [
        {'username': 'aiadm', 'password': 'new1234!', 'user_type': 'admin', 'is_initial_password': False},
        {'username': 'user', 'password': 'new1234!', 'user_type': 'user', 'is_initial_password': False},
        {'username': 'chulsoo','password': 'password123','user_type': 'user','is_initial_password': True
        },
    ]
    
    for user_data in users_data:
        password = user_data.pop('password')
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user, created = User.objects.update_or_create(
            username=user_data['username'],
            defaults={
                'password_hash': password_hash.decode('utf-8'),
                'user_type': user_data['user_type'],
                'is_initial_password': user_data['is_initial_password']
            }
        )
        
        if created:
            print(f"✅ User '{user.username}' created")
        else:
            print(f"✅ User '{user.username}' updated")

if __name__ == '__main__':
    print("Creating initial users...")
    create_initial_users()
    print("\n✨ Done!")

