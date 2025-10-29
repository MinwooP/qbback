#!/usr/bin/env python
"""
기존 대화들에 conversation_session_id 부여 스크립트

사용법:
    python manage.py shell < update_conversation_sessions.py
    
또는:
    python manage.py shell
    >>> exec(open('update_conversation_sessions.py').read())
"""

from api.models import Conversation
import secrets

print("=" * 60)
print("기존 대화에 세션 ID 부여 시작")
print("=" * 60)

# 세션 ID가 없는 대화 조회
conversations = Conversation.objects.filter(conversation_session_id__isnull=True)
total_count = conversations.count()

print(f"\n대상 대화 수: {total_count}개")

if total_count == 0:
    print("✅ 모든 대화에 이미 세션 ID가 있습니다.")
else:
    print("\n업데이트 중...\n")
    
    updated_count = 0
    for conv in conversations:
        # 고유한 세션 ID 생성
        conv.conversation_session_id = f"conv_{secrets.token_urlsafe(36)}"
        conv.save(update_fields=['conversation_session_id'])
        
        updated_count += 1
        print(f"  ✓ [{updated_count}/{total_count}] conversation_id={conv.conversation_id}, "
              f"session={conv.conversation_session_id[:20]}...")
    
    print(f"\n{'=' * 60}")
    print(f"✅ 완료! {updated_count}개 대화 업데이트됨")
    print(f"{'=' * 60}")

# 결과 확인
print("\n[결과 확인]")
all_conversations = Conversation.objects.all()
with_session = all_conversations.exclude(conversation_session_id__isnull=True).count()
without_session = all_conversations.filter(conversation_session_id__isnull=True).count()

print(f"  • 전체 대화: {all_conversations.count()}개")
print(f"  • 세션 ID 있음: {with_session}개")
print(f"  • 세션 ID 없음: {without_session}개")

if without_session == 0:
    print("\n🎉 모든 대화에 세션 ID가 정상적으로 부여되었습니다!")
else:
    print(f"\n⚠️ 아직 {without_session}개 대화에 세션 ID가 없습니다.")