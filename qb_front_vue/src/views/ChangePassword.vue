<template>
  <div class="change-password-container">
    <div class="change-password-form">
      <div class="header-section">
        <div class="security-icon">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <circle cx="12" cy="16" r="1"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        <div class="header-content">
          <h1 class="header-title">비밀번호 변경</h1>
          <p class="header-subtitle">보안을 위해 새로운 비밀번호로 변경해주세요</p>
        </div>
      </div>
      
      <form @submit.prevent="handleChangePassword" class="password-form">
        <div class="form-group">
          <label for="currentPassword">현재 비밀번호</label>
          <div class="input-wrapper">
            <input
              id="currentPassword"
              v-model="currentPassword"
              type="password"
              placeholder="현재 비밀번호를 입력하세요"
              required
              class="form-input"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="newPassword">새 비밀번호</label>
          <div class="input-wrapper">
            <input
              id="newPassword"
              v-model="newPassword"
              type="password"
              placeholder="새 비밀번호를 입력하세요"
              required
              minlength="8"
              class="form-input"
            />
          </div>
          <div class="password-hint">
            <svg class="hint-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4"/>
              <path d="M12 8h.01"/>
            </svg>
            8자 이상, 영문/숫자/특수문자 포함
          </div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">새 비밀번호 확인</label>
          <div class="input-wrapper">
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="새 비밀번호를 다시 입력하세요"
              required
              class="form-input"
            />
          </div>
        </div>
        
        <!-- 에러 메시지 표시 -->
        <div v-if="errorMessage" class="message error-message">
          <div class="message-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
          </div>
          <div class="message-text">{{ errorMessage }}</div>
        </div>
        
        <!-- 성공 메시지 표시 -->
        <div v-if="successMessage" class="message success-message">
          <div class="message-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22,4 12,14.01 9,11.01"/>
            </svg>
          </div>
          <div class="message-text">{{ successMessage }}</div>
        </div>
        
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="goToChat">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            취소
          </button>
          <button type="submit" class="change-btn" :disabled="isLoading">
            <span v-if="isLoading" class="loading-content">
              <div class="loading-spinner"></div>
              변경 중...
            </span>
            <span v-else class="change-content">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22,4 12,14.01 9,11.01"/>
              </svg>
              변경
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

//TO DO: API_URL 통일하기

// 비밀번호 변경 함수 - Django API 호출
const handleChangePassword = async () => {
  // 비밀번호 유효성 검사
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = '새 비밀번호가 일치하지 않습니다.';
    return;
  }

  if (newPassword.value.length < 8) {
    errorMessage.value = '비밀번호는 최소 8자 이상이어야 합니다.';
    return;
  }

  // 비밀번호 강도 검증 (영문, 숫자, 특수문자 포함)
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
  if (!passwordRegex.test(newPassword.value)) {
    errorMessage.value = '비밀번호는 영문, 숫자, 특수문자를 포함해야 합니다.';
    return;
  }

  errorMessage.value = '';
  successMessage.value = '';
  isLoading.value = true;

  try {
    // ==========================================
    // Django 비밀번호 변경 API 호출
    // ==========================================
    const response = await fetch(`${API_URL}/auth/change-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
      },
      body: JSON.stringify({
        current_password: currentPassword.value,
        new_password: newPassword.value
      })
    });

    const resultData = await response.json();

    if (!response.ok) {
      throw new Error(resultData.error || '비밀번호 변경에 실패했습니다.');
    }

    // ==========================================
    // 성공 응답:
    // {
    //   "success": true,
    //   "message": "비밀번호가 성공적으로 변경되었습니다."
    // }
    // ==========================================

    if (resultData.success) {
      successMessage.value = '비밀번호가 성공적으로 변경되었습니다!';
      
      // 사용자 정보 업데이트 (초기 비밀번호 플래그 해제)
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      user.isInitialPassword = false;
      sessionStorage.setItem('user', JSON.stringify(user));
      
      // 'allowSkipPasswordChange' 플래그 제거
      sessionStorage.removeItem('allowSkipPasswordChange');
      
      console.log('비밀번호 변경 완료');
      
      // 2초 후 채팅 페이지로 이동
      setTimeout(() => {
        router.push('/chat');
      }, 2000);
    }
  } catch (error) {
    console.error('비밀번호 변경 실패:', error);
    errorMessage.value = error.message || '비밀번호 변경 중 오류가 발생했습니다. 다시 시도해주세요.';
  } finally {
    isLoading.value = false;
  }
};

const goToChat = () => {
  router.push('/chat')
}
</script>

<style scoped>
/* 전역 리셋 및 기본 스타일 */
* {
  box-sizing: border-box;
}

.change-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding: 20px;
}

.change-password-form {
  background: #ffffff;
  padding: 48px 40px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid #e1e5e9;
  width: 100%;
  max-width: 480px;
  position: relative;
  overflow: hidden;
}

.change-password-form::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #1f9dfe 0%, #b5f0f4 100%);
}

/* 헤더 섹션 */
.header-section {
  text-align: center;
  margin-bottom: 32px;
}

.security-icon {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  box-shadow: 0 8px 32px rgba(31, 157, 254, 0.1);
  transition: all 0.3s ease;
}

.security-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(31, 157, 254, 0.15);
}

.security-icon .icon {
  width: 48px;
  height: 48px;
  stroke: #1f9dfe;
  stroke-width: 1.5;
}

.header-content {
  margin-bottom: 16px;
}

.header-title {
  font-size: 28px;
  font-weight: 800;
  color: #1a1d21;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.header-subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
  line-height: 1.6;
}

/* 폼 스타일 */
.password-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  letter-spacing: -0.01em;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  font-family: inherit;
  background: #ffffff;
  transition: all 0.2s ease;
  color: #374151;
}

.form-input:focus {
  outline: none;
  border-color: #1f9dfe;
  box-shadow: 0 0 0 3px rgba(31, 157, 254, 0.1);
  transform: translateY(-1px);
}

.form-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

/* 비밀번호 힌트 */
.password-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
  background: #f8fafc;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.hint-icon {
  width: 14px;
  height: 14px;
  stroke: #6b7280;
  flex-shrink: 0;
}

/* 메시지 스타일 */
.message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  animation: slideInDown 0.3s ease;
}

.message-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.message-icon svg {
  width: 100%;
  height: 100%;
}

.message-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.error-message .message-icon svg {
  stroke: #dc2626;
}

.error-message .message-text {
  color: #dc2626;
}

.success-message {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.success-message .message-icon svg {
  stroke: #16a34a;
}

.success-message .message-text {
  color: #16a34a;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 폼 액션 버튼들 */
.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.cancel-btn,
.change-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex: 1;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  letter-spacing: -0.01em;
}

.btn-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

/* 취소 버튼 */
.cancel-btn {
  background: #ffffff;
  color: #6b7280;
  border: 2px solid #e5e7eb;
}

.cancel-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.cancel-btn:active {
  transform: translateY(0);
}

/* 변경 버튼 */
.change-btn {
  background: linear-gradient(135deg, #1f9dfe 0%, #b5f0f4 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 16px rgba(31, 157, 254, 0.3);
}

.change-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(31, 157, 254, 0.4);
}

.change-btn:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(31, 157, 254, 0.3);
}

.change-btn:disabled {
  background: linear-gradient(135deg, #9ca3af 0%, #d1d5db 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(156, 163, 175, 0.2);
}

.change-content,
.loading-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 로딩 스피너 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .change-password-container {
    padding: 16px;
  }
  
  .change-password-form {
    padding: 32px 24px;
    border-radius: 16px;
  }
  
  .security-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
  }
  
  .security-icon .icon {
    width: 40px;
    height: 40px;
  }
  
  .header-title {
    font-size: 24px;
  }
  
  .header-subtitle {
    font-size: 14px;
  }
  
  .form-input {
    padding: 14px 16px;
    font-size: 16px; /* iOS에서 줌 방지 */
  }
  
  .cancel-btn,
  .change-btn {
    padding: 14px 20px;
  }
}

@media (max-width: 480px) {
  .change-password-form {
    padding: 24px 20px;
  }
  
  .security-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 16px;
  }
  
  .security-icon .icon {
    width: 32px;
    height: 32px;
  }
  
  .header-title {
    font-size: 20px;
  }
  
  .password-form {
    gap: 20px;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .cancel-btn,
  .change-btn {
    padding: 12px 16px;
  }
}

/* 접근성 개선 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 다크모드 지원 */
@media (prefers-color-scheme: dark) {
  .change-password-container {
    background: #111827;
  }
  
  .change-password-form {
    background: #1f2937;
    border-color: #374151;
  }
  
  .header-title {
    color: #f9fafb;
  }
  
  .header-subtitle {
    color: #9ca3af;
  }
  
  .security-icon {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  }
  
  .security-icon .icon {
    stroke: #60a5fa;
  }
  
  label {
    color: #e5e7eb;
  }
  
  .form-input {
    background: #111827;
    border-color: #4b5563;
    color: #e5e7eb;
  }
  
  .form-input:focus {
    border-color: #1f9dfe;
    background: #1f2937;
  }
  
  .form-input::placeholder {
    color: #6b7280;
  }
  
  .password-hint {
    background: #374151;
    border-color: #4b5563;
    color: #d1d5db;
  }
  
  .hint-icon {
    stroke: #9ca3af;
  }
  
  .error-message {
    background: #7f1d1d;
    border-color: #dc2626;
  }
  
  .error-message .message-text {
    color: #fca5a5;
  }
  
  .success-message {
    background: #064e3b;
    border-color: #059669;
  }
  
  .success-message .message-text {
    color: #6ee7b7;
  }
  
  .cancel-btn {
    background: #374151;
    border-color: #4b5563;
    color: #d1d5db;
  }
  
  .cancel-btn:hover {
    background: #4b5563;
    border-color: #6b7280;
    color: #f3f4f6;
  }
}
</style>