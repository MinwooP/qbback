from django.db import models
from django.utils import timezone
import secrets

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    is_initial_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users'
        managed = False  # Django가 테이블을 관리하지 않음 (이미 생성됨)
    
    def __str__(self):
        return self.username
    
class UserSession(models.Model):
    """사용자 인증 세션"""
    session_id = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    last_activity = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    # 세션 메타데이터
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_sessions'
        managed = 'True' # django가 관리함
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def is_valid(self):
        """세션이 유효한지 확인"""
        return (
            self.is_active and 
            self.expires_at > timezone.now()
        )
    
    @classmethod
    def create_session(cls, user, ip_address=None, user_agent=None):
        """새 세션 생성"""
        session_id = secrets.token_urlsafe(32)
        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timezone.timedelta(hours=8)
        
        return cls.objects.create(
            session_id=session_id,
            user=user,
            token=token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def refresh(self):
        """세션 갱신"""
        self.last_activity = timezone.now()
        self.expires_at = timezone.now() + timezone.timedelta(hours=8)
        self.save(update_fields=['last_activity', 'expires_at'])

class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    title = models.CharField(max_length=255, default='새 대화')
    conversation_session_id = models.CharField(
        max_length=64, 
        unique=True, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'conversations'
        managed = False
        ordering = ['-last_message_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    @classmethod
    def create_conversation_with_session(cls, user, title='새 대화'):
        """
        대화 생성 시 고유한 세션 ID도 함께 생성
        """
        # 고유한 세션 ID 생성 (48 bytes = 64 chars in base64)
        conversation_session_id = f"conv_{secrets.token_urlsafe(36)}"
        
        # 대화 생성
        conversation = cls.objects.create(
            user=user,
            title=title,
            conversation_session_id=conversation_session_id
        )
        
        return conversation

class ConversationContext(models.Model):
    """대화방별 컨텍스트 저장"""
    conversation = models.OneToOneField(
        Conversation, 
        on_delete=models.CASCADE, 
        primary_key=True,
        db_column='conversation_id'
    )
    context_data = models.JSONField(default=dict)
    message_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation_contexts'
        managed = 'True' # django가 관리함
    
    def add_message(self, role, content):
        """대화 히스토리에 메시지 추가"""
        if 'history' not in self.context_data:
            self.context_data['history'] = []
        
        self.context_data['history'].append({
            'role': role,
            'content': content,
            'timestamp': timezone.now().isoformat()
        })
        
        self.message_count += 1
        self.save()
    
    def get_recent_history(self, limit=10):
        """최근 N개의 메시지 히스토리 반환"""
        history = self.context_data.get('history', [])
        return history[-limit:] if history else []


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, 
                                    db_column='conversation_id', related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message_text = models.TextField()
    sql_query = models.TextField(null=True, blank=True)
    sql_results = models.JSONField(null=True, blank=True)
    plan_analysis = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'messages'
        managed = False
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender}: {self.message_text[:50]}"
