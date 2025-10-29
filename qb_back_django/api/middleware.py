from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils import timezone
from .models import UserSession

class SessionAuthenticationMiddleware(MiddlewareMixin):
    """세션 인증 미들웨어"""
    
    # 인증이 필요 없는 경로
    EXEMPT_PATHS = [
        '/api/v1/auth/login/',
        '/api/v1/health/',
        '/admin/',
    ]
    
    def process_request(self, request):
        
        # 디버그 로그 추가
        print(f"[Middleware] Path: {request.path}")
        print(f"[Middleware] Headers: {request.headers.get('Authorization')}")
        
        # 인증 불필요 경로는 스킵
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            print("[Middleware] Exempt path - skipping auth")
            return None
        
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            print("[Middleware] No auth header")
            return JsonResponse(
                {'error': '인증 토큰이 필요합니다.'},
                status=401
            )
        
        try:
            # "Bearer <token>" 형식 파싱
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            print(f"[Middleware] Token: {token[:20]}...")

            # 세션 조회 및 검증
            session = UserSession.objects.select_related('user').get(
                token=token,
                is_active=True
            )
            print(f"[Middleware] Session found: user_id={session.user.user_id}")

            if not session.is_valid():
                print("[Middleware] Session expired")
                session.is_active = False
                session.save()
                return JsonResponse(
                    {'error': '세션이 만료되었습니다.'},
                    status=401
                )
            
            # 세션 활동 시간 갱신
            session.last_activity = timezone.now()
            session.save(update_fields=['last_activity'])
            
            # request에 사용자 정보 추가
            # request.user와 request.custom_user 모두 설정 => Django REST Framework로 인한 AnonymousUser 문제 해결 위해 추가
            request.user = session.user
            request.custom_user = session.user
            request.session_obj = session
            
            print(f"[Middleware] request.user set to: {request.user.username} (type: {type(request.user)})")
            
            return None
        
        except (UserSession.DoesNotExist, IndexError):
            print("[Middleware] Session not found")
            return JsonResponse(
                {'error': '유효하지 않은 인증 토큰입니다.'},
                status=401
            )
        except Exception as e:
            print(f"[Middleware] Error: {e}")
            return JsonResponse(
                {'error': f'인증 오류: {str(e)}'},
                status=500
            )
