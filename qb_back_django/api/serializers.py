from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'user_type', 'is_initial_password', 
                 'created_at', 'last_login_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_text', 
                 'sql_query', 'sql_results', 'plan_analysis', 'error_message', 'created_at']
        read_only_fields = ['message_id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'user', 'title', 'created_at', 
                 'updated_at', 'last_message_at', 'is_deleted', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']


class ConversationListSerializer(serializers.ModelSerializer):
    """대화 목록용 간단한 Serializer (메시지 포함 안 함)"""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'title', 'created_at', 'updated_at', 
                 'last_message_at', 'message_count']
    
    def get_message_count(self, obj):
        return obj.messages.count()
