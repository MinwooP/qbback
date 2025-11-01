import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import Chat from '@/views/Chat.vue'
import Login from '@/views/Login.vue' 
import ChangePassword from '@/views/ChangePassword.vue'
import SQLManage from '@/views/SQLManage.vue'

// TO DO: API 설정
const API_URL = window.APP_CONFIG?.API_URL || 'http://10.220.150.75:8012/api/v1';

const routes = [
  {
    path: '/',
    redirect:'/login',
    component: App
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true }  // 비로그인 사용자만 접근 가능
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: { requiresAuth: true }
  },
  {
    path: '/sqlManage',
    name: 'SQLManage',
    component: SQLManage,
    meta: { requiresAuth: true, requiresAdmin: true}
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 로그인 상태 확인 함수 
function isAuthenticated() {
  const sessionId = sessionStorage.getItem('sessionId');
  const sessionToken = sessionStorage.getItem('sessionToken');
  const isLoggedIn = sessionStorage.getItem('isLoggedIn');
  const user = sessionStorage.getItem('user');
  
  // 모든 필수 세션 정보가 있는지 확인
  return !!(sessionId && sessionToken && isLoggedIn === 'true' && user);
}

// 초기 비밀번호 사용자인지 확인 함수
function isInitialPasswordUser() {
  const user = JSON.parse(sessionStorage.getItem('user') || '{}')
  return user.isInitialPassword === true
}

//관리자 권한 확인 함수
function isAdmin(){
  const user = JSON.parse(sessionStorage.getItem('user') || '{}')
  return user.userType =='admin'
}

// 서버 세션 검증 
// TO DO: 사용될 부분 찾아보기
async function validateServerSession() {
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
}

router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()
  
  // 1. 로그인이 필요한 페이지 접근 시
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authenticated) {
      // 로그인 안됨 → 로그인 페이지로 리다이렉트
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 로그인 후 원래 페이지로 돌아가기 위한 정보 저장
      });
    } else {
      
      // 서버 세션 검증 추가
      // 주의: 매 라우팅마다 API 호출하면 성능 저하 가능
      // 필요시 주석 해제하기
      // ========================================
      // const isValidSession = await validateServerSession();
      // if (!isValidSession) {
      //   // 세션 만료됨
      //   sessionStorage.clear();
      //   alert('세션이 만료되었습니다. 다시 로그인해주세요.');
      //   next('/login');
      //   return;
      // }

      //관리자 접근 확인
      if(to.matched.some(record => record.meta.requiresAdmin)){
        if(!isAdmin()){
          alert('접근 권한이 없습니다.')
          next('/chat')
          return
        }
      }

      // 인증된 사용자이지만 초기 비밀번호를 사용 중이고, 비밀번호 변경 페이지가 아닌 경우
      if (isInitialPasswordUser() && to.path !== '/change-password') {
        // 초기 비밀번호 사용자는 비밀번호 변경 페이지로만 접근 가능
        // 단, 팝업에서 "다음에 변경하기"를 선택한 경우는 예외
        const allowSkip = sessionStorage.getItem('allowSkipPasswordChange') === 'true'
        if (!allowSkip) {
          next('/change-password')
          return
        }
      }
      next();
    }

  } 
  // 2. 로그인한 사용자가 접근하면 안되는 페이지 (게스트 전용)
  else if (to.matched.some(record => record.meta.guestOnly)) {
    if (authenticated) {
      // 이미 로그인된 사용자 → 채팅 페이지로 리다이렉트
      next('/chat')
    } else {
      // 비로그인 사용자 → 정상 접근
      next()
    }
  } 
  // 3. 접근 제한이 없는 페이지
  else {
    //정의되지 않은 경로 리다이렉트 처리
    if(to.matched.length===0){
      if(authenticated){
        next('/chat')
      }else{
        next('/login')
      }
    }else{
      next();
    }

  }
});

export default router