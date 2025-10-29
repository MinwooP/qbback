import bcrypt
from django.utils import timezone
from django.db import connection
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserSession, Conversation, ConversationContext, Message
from .serializers import (UserSerializer, ConversationSerializer, 
                         ConversationListSerializer, MessageSerializer)
import uuid
import json


# ==================== 헬스 체크 ====================
@api_view(['GET'])
def health_check(request):
    """API 연결 상태 확인"""
    return Response({'status': 'ok', 'message': 'API is running'})


# ==================== 인증 관련 ====================
class AuthViewSet(viewsets.ViewSet):
    """인증 관련 API"""
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """로그인"""
        username = request.data.get('employeeId')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'success': False, 'message': '사번과 비밀번호를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
            
            # 비밀번호 확인
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # 기존 활성 세션 비활성화 (중복 로그인 방지)
                UserSession.objects.filter(user=user, is_active=True).update(
                    is_active=False
                )
                
                # 새 세션 생성
                ip_address = self._get_client_ip(request)
                user_agent = request.headers.get('User-Agent', '')
                
                session = UserSession.create_session(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                # 로그인 시간 업데이트
                user.last_login_at = timezone.now()
                user.save(update_fields=['last_login_at'])

                return Response({
                    'success': True,
                    'userId': user.user_id,
                    'username': user.username,
                    'userType': user.user_type,
                    'isInitialPassword': user.is_initial_password,
                    'sessionId': session.session_id,
                    'token': session.token,
                    'expiresAt': session.expires_at.isoformat()
                })
            else:
                return Response(
                    {'success': False, 'message': '사번 또는 비밀번호가 올바르지 않습니다.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        except User.DoesNotExist:
            return Response(
                {'success': False, 'message': '사번 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """비밀번호 변경"""
        username = request.data.get('username')
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        
        if not all([username, current_password, new_password]):
            return Response(
                {'success': False, 'message': '필수 정보가 누락되었습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
            
            # 현재 비밀번호 확인
            if bcrypt.checkpw(current_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # 새 비밀번호 해싱
                new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = new_password_hash.decode('utf-8')
                user.is_initial_password = False
                user.save(update_fields=['password_hash', 'is_initial_password', 'updated_at'])
                
                return Response({
                    'success': True,
                    'message': '비밀번호가 성공적으로 변경되었습니다.'
                })
            else:
                return Response(
                    {'success': False, 'message': '현재 비밀번호가 올바르지 않습니다.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        except User.DoesNotExist:
            return Response(
                {'success': False, 'message': '사용자를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """로그아웃 - 세션 무효화"""
        if hasattr(request, 'session_obj'):
            request.session_obj.is_active = False
            request.session_obj.save()
            
            return Response({
                'success': True,
                'message': '로그아웃되었습니다.'
            })
        
        return Response(
            {'success': False, 'message': '세션을 찾을 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'], url_path='validate')
    def validate_session(self, request):
        """세션 유효성 검증"""
        if hasattr(request, 'session_obj'):
            return Response({
                'valid': True,
                'userId': request.user.user_id,
                'username': request.user.username,
                'expiresAt': request.session_obj.expires_at.isoformat()
            })
        
        return Response(
            {'valid': False},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def _get_client_ip(request):
        """클라이언트 IP 추출"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# ==================== 대화 관련 ====================
class ConversationViewSet(viewsets.ModelViewSet):
    """대화 관련 API"""
    queryset = Conversation.objects.filter(is_deleted=False)
    serializer_class = ConversationSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """현재 사용자의 대화방만 조회"""
        # custom_user 사용
        user = getattr(self.request, 'custom_user', None)
        if not user:
            return Conversation.objects.none()
        
        return Conversation.objects.filter(
            user=user,
            is_deleted=False
        ).order_by('-updated_at')
    
    def create(self, request):
        """새 대화 생성"""

        # 미들웨어에서 설정한 request.custom_user 사용 => Django REST Framework로 인한 AnonymousUser 문제 해결 위해 추가
        user = getattr(request, 'custom_user', None)
        
        # 디버그 로그 추가 
        print(f"[View] request.user: {request.user}")
        print(f"[View] request.custom_user: {user}")
        print(f"[View] request.user type: {type(request.user)}")
        print(f"[View] Is authenticated: {hasattr(request, 'session_obj')}")
    
        print(f"[View] Creating conversation for user_id: {user.user_id}")
        
        if not user or not hasattr(user, 'user_id'):
            return Response(
                {'error': '인증되지 않은 사용자입니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        conversation = Conversation.objects.create(
            user=user,
            title=request.data.get('title', '새 대화')
        )

        # 컨텍스트 생성
        ConversationContext.objects.create(
            conversation=conversation
        )

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        """대화 삭제 (소프트 삭제)"""
        try:
            conversation = self.get_queryset().get(conversation_id=pk)
            conversation.is_deleted = True
            conversation.save()
            
            return Response({
                'success': True,
                'message': '대화가 삭제되었습니다.'
            })
        except Conversation.DoesNotExist:
            return Response(
                {'error': '대화를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

# ==================== 채팅 API ====================
@api_view(['POST'])
def chat(request):
    """
    메시지 전송 및 SQL 쿼리 실행
    대화방별 컨텍스트를 활용한 멀티턴 대화
    """

    # custom_user 사용
    user = getattr(request, 'custom_user', None)
    
    if not user:
        return Response(
            {'error': '인증되지 않은 사용자입니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user_message = request.data.get('message')
    conversation_id = request.data.get('conversation_id')
    
    if not all([user_message, conversation_id]):
        return Response(
            {'error': '필수 정보가 누락되었습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # 대화방 조회 및 권한 확인
        conversation = Conversation.objects.get(
            conversation_id=conversation_id,
            user=user,
            is_deleted=False
        )

        # 대화방 컨텍스트 가져오기 또는 생성
        context, created = ConversationContext.objects.get_or_create(
            conversation=conversation
        )
        
        # 사용자 메시지 저장
        user_msg = Message.objects.create(
            conversation=conversation,
            sender='user',
            message_text=user_message
        )
        
        # 컨텍스트에 메시지 추가
        context.add_message('user', user_message)
        
        # 최근 대화 히스토리 가져오기 (멀티턴을 위해)
        recent_history = context.get_recent_history(limit=10)
        
        # TODO: LLM을 이용한 SQL 생성 (히스토리 포함)
        # 예: sql_query = generate_sql_with_llm(user_message, recent_history)
        
        sql_query = "SELECT * FROM users LIMIT 10;"
        
        # SQL 실행
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            assistant_response = '요청하신 데이터를 조회했습니다.'
            
            # Assistant 응답 저장
            assistant_msg = Message.objects.create(
                conversation=conversation,
                sender='assistant',
                message_text=assistant_response,
                sql_query=sql_query,
                sql_results=results
            )
            
            # 컨텍스트에 응답 추가
            context.add_message('assistant', assistant_response)
            
            # 대화의 last_message_at 업데이트
            conversation.last_message_at = timezone.now()
            conversation.save(update_fields=['last_message_at'])
            
            return Response({
                'response': assistant_response,
                'sql': sql_query,
                'results': results,
                'plan_analysis': None,
                'conversation_context': {
                    'message_count': context.message_count,
                    'history_length': len(recent_history)
                }
            })
        
        except Exception as e:
            error_msg = f'쿼리 실행 중 오류가 발생했습니다: {str(e)}'
            Message.objects.create(
                conversation=conversation,
                sender='assistant',
                message_text=error_msg,
                error_message=str(e)
            )
            
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Conversation.DoesNotExist:
        return Response(
            {'error': '대화를 찾을 수 없거나 접근 권한이 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )