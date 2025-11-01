<template>
  <div class="login-container">
    <div class="login-form">
      <div class="logo-section">
        <div class="logo-icon">
          <img src="@/images/qb_logo.png" alt="Query Buddy" class="logo">
        </div>
        <div class="brand-info">
          <h1 class="brand-title">Query Buddy</h1>
          <p class="brand-subtitle">AI-Powered Database Assistant</p>
        </div>
      </div>
      
      <div class="description">
        <p>자연어로 데이터베이스를 조회하는 AI Agent입니다</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form-content">
        <div class="form-group">
          <label for="employeeId">사번</label>
          <div class="input-wrapper">
            <input 
              id="employeeId" 
              v-model="employeeId" 
              type="text" 
              placeholder="사번을 입력하세요" 
              required 
              class="form-input"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <div class="input-wrapper">
            <input 
              id="password" 
              v-model="password" 
              type="password" 
              placeholder="비밀번호를 입력하세요" 
              required 
              class="form-input"
            />
          </div>
        </div>

        <!-- 에러 메시지 표시 -->
        <div v-if="errorMessage" class="error-message">
          <div class="error-icon">⚠️</div>
          <div class="error-text">{{ errorMessage }}</div>
        </div>

        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="isLoading" class="loading-content">
            <div class="loading-spinner"></div>
            로그인 중...
          </span>
          <span v-else class="login-content">
            <svg class="login-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10,17 15,12 10,7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
            로그인
          </span>
        </button>
      </form>
    </div>

    <!-- 비밀번호 변경 팝업 -->
    <PasswordChangePopup 
      :show="showPasswordChangePopup" 
      @change="goToChangePassword" 
      @later="continueToChat" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PasswordChangePopup from '../components/PasswordChangePopup.vue'

const router = useRouter()
const route = useRoute()

const employeeId = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const showPasswordChangePopup = ref(false)

//TO DO: API_URL 해결하기

/*
// 세션 ID 생성 함수
const generateSessionId = () => {
  const timestamp = new Date().getTime()
  const randomStr = Math.random().toString(36).substring(2, 15)
  const userPrefix = employeeId.value ? employeeId.value : 'user'
  return `${userPrefix}_${timestamp}_${randomStr}`
}

// 세션 토큰 생성 함수 (JWT 스타일)
const generateSessionToken = () => {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payload = btoa(JSON.stringify({
    userId: employeeId.value,
    loginTime: new Date().toISOString(),
    exp: Math.floor(Date.now() / 1000) + (60 * 60 * 8) // 8시간 만료
  }))
  const signature = btoa(`signature_${Math.random().toString(36).substring(2, 15)}`)
  return `${header}.${payload}.${signature}`
}

// 세션 정보 저장 함수
const setSessionInfo = (sessionData) => {
  try {
    // sessionStorage에 세션 정보 저장
    sessionStorage.setItem('sessionId', sessionData.sessionId)
    sessionStorage.setItem('sessionToken', sessionData.token)
    sessionStorage.setItem('sessionCreatedAt', sessionData.createdAt)
    
    console.log('세션 정보가 설정되었습니다:', {
      sessionId: sessionData.sessionId,
      userId: sessionData.userId,
      createdAt: sessionData.createdAt
    })
    
    // 전역에서 사용할 수 있도록 window 객체에도 저장 (선택사항)
    window.currentSession = {
      id: sessionData.sessionId,
      token: sessionData.token,
      userId: sessionData.userId
    }
    
  } catch (error) {
    console.error('세션 정보 저장 중 오류:', error)
  }
}
*/

// django 로그인 API 호출
const handleLogin = async () => {
  // 에러 메시지 초기화
  errorMessage.value = ''
  isLoading.value = true

  try {
    console.log('Login attempt:', { employeeId: employeeId.value, password: password.value })

    // django 로그인 api 호출 
    const response = await fetch(`${API_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: employeeId.value,
        password: password.value
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '로그인에 실패했습니다.');
    }

    const loginData = await response.json();

    // ==========================================
    // 응답 데이터 구조:
    // {
    //   "success": true,
    //   "user": { user_id, username, user_type, is_initial_password },
    //   "session": { session_id, token, expires_at }
    // }
    // ==========================================

    if (loginData.success) {
      // 세션 정보 저장
      sessionStorage.setItem('sessionId', loginData.session.session_id);
      sessionStorage.setItem('sessionToken', loginData.session.token);
      sessionStorage.setItem('sessionCreatedAt', new Date().toISOString());
      
      // 사용자 정보 저장
      sessionStorage.setItem('isLoggedIn', 'true');
      sessionStorage.setItem('user', JSON.stringify({
        userId: loginData.user.user_id,
        employeeId: loginData.user.username,
        isInitialPassword: loginData.user.is_initial_password,
        userType: loginData.user.user_type,
        sessionId: loginData.session.session_id,
        loginTime: new Date().toISOString()
      }));

      // 전역 세션 정보 (선택사항)
      window.currentSession = {
        id: loginData.session.session_id,
        token: loginData.session.token,
        userId: loginData.user.user_id
      };

      console.log('로그인 성공! 세션 정보:', {
        sessionId: loginData.session.session_id,
        userId: loginData.user.user_id,
        userType: loginData.user.user_type
      });

      // // 초기 비밀번호 확인 => 현재는 비활성화 
      // if (loginData.user.is_initial_password) {
      //   // 초기 비밀번호면 팝업 표시
      //   showPasswordChangePopup.value = true;
      // } else {
      //   // 일반 로그인이면 바로 채팅 페이지로
      //   navigateToChat();
      // }
    }
  } catch (error) {
    console.error('로그인 실패:', error);
    errorMessage.value = error.message || '로그인 중 오류가 발생했습니다. 다시 시도해주세요.';
  } finally {
    isLoading.value = false;
  }
};

const goToChangePassword = () => {
  showPasswordChangePopup.value = false
  router.push('/change-password')
}

const continueToChat = () => {
  showPasswordChangePopup.value = false

  // "다음에 변경하기" 허용 플래그 설정
  sessionStorage.setItem('allowSkipPasswordChange', 'true')

  navigateToChat()
}

const navigateToChat = () => {
  // 원래 접근하려던 페이지로 리다이렉트 (있는 경우) 또는 /chat으로 이동
  const redirectPath = route.query.redirect || '/chat'
  router.push(redirectPath)
}

// 세션 검증 API: 페이지 로드 시 세션 확인
const validateSession = async () => {
  const sessionToken = sessionStorage.getItem('sessionToken');
  
  if (!sessionToken) {
    return false;
  }

  try {
    const response = await fetch(`${API_URL}/auth/validate/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionToken}`
      }
    });

    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    return data.valid === true;
  } catch (error) {
    console.error('세션 검증 실패:', error);
    return false;
  }
};

onMounted(async () => {
  // 이미 로그인된 경우 자동으로 채팅 페이지로 이동
  const isValid = await validateSession();
  if (isValid) {
    console.log('유효한 세션이 존재합니다. 채팅 페이지로 이동합니다.');
    router.replace('/chat');
  }
});

</script>

<style scoped>
/* 전역 리셋 및 기본 스타일 */
* {
  box-sizing: border-box;
}

.login-container {
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

.login-form {
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

.login-form::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #1f9dfe 0%, #b5f0f4 100%);
}

/* 로고 섹션 */
.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  /* width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e2e8f0 100%); */
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0px;
  /* box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06); */
  transition: all 0.3s ease;
}

.logo-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
}

.logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  padding: 5px;
}

.brand-info {
  margin-bottom: 16px;
}

.brand-title {
  font-size: 28px;
  font-weight: 800;
  color: #1a1d21;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  margin: 0;
}

/* 설명 섹션 */
.description {
  text-align: center;
  margin-bottom: 32px;
}

.description p {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
  line-height: 1.6;
}

/* 폼 스타일 */
.login-form-content {
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

/* 에러 메시지 */
.error-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 16px;
  animation: slideInDown 0.3s ease;
}

.error-icon {
  flex-shrink: 0;
  font-size: 16px;
}

.error-text {
  flex: 1;
  color: #dc2626;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
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

/* 로그인 버튼 */
.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #1f9dfe 0%, #b5f0f4 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(31, 157, 254, 0.3);
  font-family: inherit;
  letter-spacing: -0.01em;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(31, 157, 254, 0.4);
}

.login-btn:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(31, 157, 254, 0.3);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #9ca3af 0%, #d1d5db 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(156, 163, 175, 0.2);
}

.login-content,
.loading-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
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
  .login-container {
    padding: 16px;
  }
  
  .login-form {
    padding: 32px 24px;
    border-radius: 16px;
  }
  
  .logo-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
  }
  
  .logo {
    width: 60px;
    height: 60px;
  }
  
  .brand-title {
    font-size: 24px;
  }
  
  .description p {
    font-size: 14px;
  }
  
  .form-input {
    padding: 14px 16px;
    font-size: 16px; /* iOS에서 줌 방지 */
  }
  
  .login-btn {
    padding: 14px 20px;
  }
}

@media (max-width: 480px) {
  .login-form {
    padding: 24px 20px;
  }
  
  .logo-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 16px;
  }
  
  .logo {
    width: 40px;
    height: 40px;
  }
  
  .brand-title {
    font-size: 20px;
  }
  
  .brand-subtitle {
    font-size: 12px;
  }
  
  .login-form-content {
    gap: 20px;
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
  .login-container {
    background: #111827;
  }
  
  .login-form {
    background: #1f2937;
    border-color: #374151;
  }
  
  .brand-title {
    color: #f9fafb;
  }
  
  .brand-subtitle {
    color: #9ca3af;
  }
  
  .description p {
    color: #9ca3af;
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
  
  .error-message {
    background: #7f1d1d;
    border-color: #dc2626;
  }
  
  .error-text {
    color: #fca5a5;
  }
}
</style>