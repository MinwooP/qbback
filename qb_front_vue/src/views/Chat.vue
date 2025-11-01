<template>
  <div class="chatbot-container">
    <!-- 왼쪽 사이드바 - 대화 이력 -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }"  v-if="!isSidebarCollapsed">
      <div class="sidebar-header">
        <div class="sidebar-brand">
          <div class="brand-icon">
            <!-- <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4"></path>
              <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
              <path d="M3 19h18"></path>
            </svg> -->
            <img src="@/images/qb_web.png" alt="Logo" class="title-icon" />
          </div>
          <div class="brand-text">
            <div class="brand-title">Query Buddy</div>
            <div class="brand-subtitle">AI Database Assistant</div>
          </div>
        </div>

        <button @click="toggleSidebar" class="sidebar-toggle" :title="isSidebarCollapsed ? '사이드바 펼치기' : '사이드바 접기'">
          <svg class="hamburger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6" class="line1"></line>
            <line x1="3" y1="12" x2="21" y2="12" class="line2"></line>
            <line x1="3" y1="18" x2="21" y2="18" class="line3"></line>
          </svg>
        </button>
      </div>

      <div class="conversation-list" v-if="!isSidebarCollapsed">
        <button class="new-chat-btn" @click="createNewChat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 5v14m7-7H5"/>
          </svg>
          새 대화
        </button>

        <div class="conversation-items">
          <div v-for="conversation in conversations" :key="conversation.id"
            :class="['conversation-item', { active: currentConversationId === conversation.id }]"
            @click="switchConversation(conversation.id)">
            <div class="conversation-content">
              <div class="conversation-title">{{ conversation.title }}</div>
              <div class="conversation-preview">{{ getConversationPreview(conversation) }}</div>
              <div class="conversation-date">{{ formatDate(conversation.lastMessage) }}</div>
            </div>
            <button @click.stop="deleteConversation(conversation.id)" class="delete-btn" v-if="conversations.length > 1">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 사이드바 하단 정보 -->
      <div class="sidebar-footer" v-if="!isSidebarCollapsed">
        <div style="display: flex;">
          <div class="connection-info">
            <div :class="['status-dot', connectionStatus]"></div>
            <span class="status-text">{{ connectionText }}</span>
          </div>
          <button v-if="isAdmin" @click="goToSQLManage" class="sql-manage-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <ellipse cx="12" cy="5" rx="9" ry="3"/>
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              <path d="M12 12v7"/>
            </svg>
            SQL 관리
          </button>
        </div>
        <button @click="logout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4m7 14l5-5-5-5m5 5H9"/>
          </svg>
          로그아웃
        </button>
      </div>
    </div>

    <!-- 메인 채팅 영역 -->
    <div class="main-chat">
      <!-- 헤더 -->
      <div class="chat-header" v-if="isSidebarCollapsed">
        <div class="header-left">
          <button @click="toggleSidebar" class="mobile-menu-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
          <div class="header-title">Query Buddy</div>
        </div>
        <div class="header-right">
          <div :class="['status-dot', connectionStatus]"></div>
          <span class="status-text">{{ connectionText }}</span>
          <button @click="logout" class="header-logout-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4m7 14l5-5-5-5m5 5H9"/>
            </svg>
            로그아웃
          </button>
        </div>
      </div>

      <!-- 메시지 영역 -->
      <div class="chat-messages" ref="chatMessages" id="chatMessages">
        <!-- 환영 메시지 -->
        <div class="welcome-section" v-if="currentMessages.length === 0">
          <div class="welcome-header">
            <div class="welcome-icon">
              <!-- <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M9 12l2 2 4-4"></path>
                <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
                <path d="M3 19h18"></path>
              </svg> -->
              <img src="@/images/qb_web.png" alt="Logo" class="welcome-title-icon" />
            </div>
            <h1 class="welcome-title">Query Buddy와 함께하세요</h1>
            <p class="welcome-description">
              자연어로 데이터베이스를 조회하는 AI 에이전트입니다.<br>
              아래 예시를 클릭하거나 직접 질문을 입력해보세요.
            </p>
          </div>

          <div class="suggestion-cards">
            <div v-for="suggestion in suggestions" :key="suggestion.id" class="suggestion-card" 
              @click="sendExampleQuery(suggestion.query)">
              <div v-if="suggestion.icon === 'star'" class="suggestion-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <div v-else-if="suggestion.icon === 'users'" class="suggestion-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="8.5" cy="7" r="4"/>
                  <path d="M20 8v6M23 11h-6"/>
                </svg>
              </div>
              <div v-else-if="suggestion.icon === 'monitor'" class="suggestion-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <div class="suggestion-content">
                <div class="suggestion-title">{{ suggestion.title }}</div>
                <div class="suggestion-text">{{ suggestion.text }}</div>
              </div>
            </div>
            
            <!-- <div class="suggestion-card" @click="sendExampleQuery('핫픽 이벤트 응모자 리스트')">
              <div class="suggestion-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="8.5" cy="7" r="4"/>
                  <path d="M20 8v6M23 11h-6"/>
                </svg>
              </div>
              <div class="suggestion-content">
                <div class="suggestion-title">응모자 조회</div>
                <div class="suggestion-text">핫픽 이벤트 응모자 리스트</div>
              </div>
            </div>

            <div class="suggestion-card" @click="sendExampleQuery('모바일 상품권 내역 알려줘')">
              <div class="suggestion-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <div class="suggestion-content">
                <div class="suggestion-title">상품권 내역</div>
                <div class="suggestion-text">모바일 상품권 내역 조회</div>
              </div>
            </div> -->
          </div>
        </div>

        <!-- 메시지 리스트 -->
        <div v-for="message in currentMessages" :key="message.id" :class="`message ${message.sender}`">
          <div class="message-content">
            <!-- 사용자 메시지 -->
            <div v-if="message.sender === 'user'" class="user-message">
              <div class="message-text">{{ message.text }}</div>
            </div>

            <!-- 봇 메시지 -->
            <div v-else class="assistant-message">
              <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4"></path>
                  <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
                  <path d="M3 19h18"></path>
                </svg>
              </div>
              
              <div class="message-body">
                <div v-if="message.response" class="response-text">{{ message.response }}</div>

                <!-- SQL 쿼리 -->
                <div v-if="message.sql" class="sql-container">
                  <div class="sql-header">
                    <div class="sql-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <ellipse cx="12" cy="5" rx="9" ry="3"/>
                        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                      </svg>
                      생성된 SQL 쿼리
                    </div>
                    <button :class="['copy-btn', { 'copied': copiedStates[message.id] }]"
                      @click="copyQueryToClipboard(message.sql, message.id)">
                      <svg v-if="!copiedStates[message.id]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                      </svg>
                      <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20,6 9,17 4,12"/>
                      </svg>
                      {{ copiedStates[message.id] ? '복사됨' : '복사' }}
                    </button>
                  </div>
                  <div class="sql-code">
                    <pre><code 
                      :id="`sql-code-${message.id}`"
                      class="language-sql"
                      v-text="message.sql"
                    ></code></pre>
                  </div>
                </div>

                <!-- 실행 계획 분석 -->
                <div v-if="message.hasPlanAnalysis" class="plan-container">
                  <div class="plan-header">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M3 3v18h18"/>
                      <path d="M7 16l4-4 4 4 6-6"/>
                    </svg>
                    실행 계획 분석
                  </div>
                  <div class="plan-content">{{ message.plan_analysis }}</div>
                </div>

                <!-- 조회 결과 -->
                <div v-if="message.results && message.results.length > 0" class="results-container">
                  <div class="results-header">
                    <div class="results-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l3 9a5.002 5.002 0 01-6.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                      </svg>
                      조회 결과 ({{ message.results.length }}개 행)
                    </div>
                  </div>
                  <div v-html="formatResultsTable(message.results)"></div>
                </div>
                <!-- 조회 결과 0건일 경우 -->
                <div v-if="message.results && message.results.length ===0 && message.showNoResults" class="results-container">
                  <div class="results-header">
                    <div class="results-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l3 9a5.002 5.002 0 01-6.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                      </svg>
                      조회 결과 0 개 행
                    </div>
                  </div>
                  <div class="no-results">결과가 없습니다.</div>
                </div>

                <!-- 에러 메시지 -->
                <div v-if="message.error" class="error-container">
                  <div class="error-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="15" y1="9" x2="9" y2="15"/>
                      <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                  </div>
                  <div class="error-text">{{ message.error }}</div>
                </div>
              </div>
            </div>

            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <!-- 타이핑 인디케이터 -->
        <div v-if="isTyping" class="message assistant">
          <div class="message-content">
            <div class="assistant-message">
              <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4"></path>
                  <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
                  <path d="M3 19h18"></path>
                </svg>
              </div>
              <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 입력 영역 -->
      <div class="chat-input-container">
        <div class="input-wrapper">
          <textarea 
            ref="chatInput" 
            id="chatInput" 
            v-model="newMessage" 
            @keydown="handleKeydown"
            @input="adjustTextareaHeight" 
            placeholder="데이터베이스 쿼리를 자연어로 요청하세요." 
            class="message-input" 
            rows="1"
            maxlength="500"
          ></textarea>
          <button 
            ref="sendButton" 
            id="sendButton" 
            @click="sendMessage" 
            :disabled="!newMessage.trim()"
            class="send-button"
          >
            <svg class="send-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
        <div class="input-footer">
          <div class="char-count">{{ newMessage.length }}/500</div>
          <div class="input-hint">Enter로 전송, Shift+Enter로 줄바꿈</div>
        </div>
      </div>
    </div>

    <!-- 복사 알림 토스트 -->
    <div v-if="showCopyToast" class="toast success">
      <div class="toast-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20,6 9,17 4,12"/>
        </svg>
      </div>
      <div class="toast-message">SQL 쿼리가 클립보드에 복사되었습니다!</div>
    </div>
  </div>
</template>

<script>
import { ref, computed, nextTick, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Prism from 'prismjs'
import 'prismjs/components/prism-sql'
import 'prismjs/themes/prism-tomorrow.css'

export default {
  name: 'ChatbotApp',
  setup() {
    // API 설정
    const API_URL = window.APP_CONFIG?.API_URL || 'http://10.220.150.75:8012/api/v1'

    // Suggestions 설정
    const suggestions = window.APP_CONFIG?.SUGGESTIONS || []
    console.log('Loaded suggestions:', suggestions.value)

    // Vue Router 초기화
    const router = useRouter()

    // 로그인 상태 확인 함수
    const checkAuth = () => {
      if (!validateSession()) {
        router.replace('/login')
        return false
      }
      return true
    }

    const isAdmin = computed(() => {
      try{
        const user = JSON.parse(sessionStorage.getItem('user') || '{}')
        return user.userType === 'admin'
      } catch(error){
        return false;
      }
    })

    // 세션 유효성 검사 함수
    const validateSession = () => {
      const sessionId = sessionStorage.getItem('sessionId')
      const sessionToken = sessionStorage.getItem('sessionToken')
      const isLoggedIn = sessionStorage.getItem('isLoggedIn')
      const user = sessionStorage.getItem('user')
      
      // 모든 필수 세션 정보가 있는지 확인
      const isValid = !!(sessionId && sessionToken && isLoggedIn === 'true' && user)
      
      console.log('세션 검증 결과:', {
        sessionId: !!sessionId,
        sessionToken: !!sessionToken,
        isLoggedIn: isLoggedIn === 'true',
        user: !!user,
        isValid
      })
      
      return isValid
    }

    const logout = async () => {
      if (!confirm('정말로 로그아웃하시겠습니까?')) {
        return;
      }

      try {
        // Django 로그아웃 API 호출
        const response = await fetch(`${API_URL}/auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
          }
        });

        if (response.ok) {
          console.log('서버 로그아웃 성공');
        } else {
          console.error('서버 로그아웃 실패:', response.status);
        }
      } catch (error) {
        console.error('로그아웃 API 호출 오류:', error);
      } finally {
        // 로컬 세션 정보 삭제 (API 실패해도 클라이언트는 정리)
        sessionStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('sessionId');
        sessionStorage.removeItem('sessionToken');
        sessionStorage.removeItem('sessionCreatedAt');
        sessionStorage.removeItem('allowSkipPasswordChange');
        
        if (window.currentSession) {
          delete window.currentSession;
        }
        
        console.log('로컬 세션 정보가 모두 정리되었습니다.');
        router.replace('/login');
      }
    }

    const goToSQLManage = () => {
      router.push('/SQLManage')
    }

    // 템플릿 참조
    const chatMessages = ref(null)
    const chatInput = ref(null)
    const sendButton = ref(null)

    // 복사 기능 관련 상태
    const copiedStates = reactive({})
    const showCopyToast = ref(false)

    // 반응형 데이터
    const conversations = ref([])
    const currentConversationId = ref(null)
    const currentConversationSessionId = ref(null)
    const newMessage = ref('')
    const isTyping = ref(false)
    const messageIdCounter = ref(1)
    const conversationIdCounter = ref(1)
    const isSidebarCollapsed = ref(false)
    const conversationHistory = ref([])
    const connectionStatus = ref('connected')
    const currentTableData = ref(null)

    // 연결 상태 텍스트
    const connectionText = computed(() => {
      return connectionStatus.value === 'connected' ? '연결됨' : '연결 끊김'
    })

    // 현재 대화 메시지
    const currentMessages = computed(() => {
      const conversation = conversations.value.find(c => c.id === currentConversationId.value)
      return conversation ? conversation.messages : []
    })

    // 대화 미리보기 텍스트 생성
    const getConversationPreview = (conversation) => {
      if (conversation.messages.length === 0) return '새 대화'
      const lastUserMessage = conversation.messages.filter(m => m.sender === 'user').pop()
      if (!lastUserMessage) return '새 대화'
      return lastUserMessage.text.length > 50 ? 
        lastUserMessage.text.substring(0, 50) + '...' : 
        lastUserMessage.text
    }

    // API 연결 확인
    const checkAPIConnection = async () => {
      try {
        const response = await fetch(`${API_URL}/health`)
        if (!response.ok) {
          throw new Error('API connection failed')
        }
        connectionStatus.value = 'connected'
      } catch (error) {
        console.error('API 연결 실패:', error)
        connectionStatus.value = 'disconnected'
      }
    }

    // 대화 목록 로드 - Django API 호출
    const loadConversations = async () => {
      try {
        const response = await fetch(`${API_URL}/conversations/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const conversationsData = await response.json();
        
        // Django API 응답 형식에 맞게 변환
        conversations.value = conversationsData.map(conv => ({
          id: conv.conversation_id,
          title: conv.title,
          messages: [], // 메시지는 필요할 때 따로 로드
          lastMessage: new Date(conv.last_message_at || conv.updated_at),
          createdAt: new Date(conv.created_at),
          sessionId: conv.conversation_session_id
        }));

        console.log(`${conversations.value.length}개의 대화를 로드했습니다.`);
        
        // 첫 번째 대화 선택 (있는 경우)
        if (conversations.value.length > 0) {
          await selectConversation(conversations.value[0].id);
        }
      } catch (error) {
        console.error('대화 목록 로드 실패:', error);
        connectionStatus.value = 'disconnected';
      }
    };

    // 특정 대화 선택 시, 해당 대화로 현재 대화 설정하기
    // 특정 대화에 대한 메세지 로드
    const selectConversation = async (conversationId) => {
      currentConversationId.value = conversationId;
      
      const conversation = conversations.value.find(c => c.id === conversationId);
      if (!conversation) return;

      currentConversationSessionId.value = conversation.sessionId;
      
      // 메시지가 아직 로드되지 않았으면 로드
      if (!conversation.messages || conversation.messages.length === 0) {
        await loadConversationMessages(conversationId);
      }
      
      nextTick(() => {
        scrollToBottom();
        highlightSQLCode();
      });
    };

    // 특정 대화에 대한 메세지 상세 조회
    const loadConversationMessages = async (conversationId) => {
      try {
        const response = await fetch(`${API_URL}/conversations/${conversationId}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const conversationData = await response.json();
        
        // conversation 내 현재 대화 찾고 받아온 메세지 저장
        const conversation = conversations.value.find(c => c.id === conversationId);
        if (!conversation) return;

        // 메시지 변환 및 저장
        conversation.messages = conversationData.messages.map(msg => {
          if (msg.sender === 'user') {
            return {
              id: msg.message_id,
              sender: 'user',
              text: msg.message_text,
              timestamp: new Date(msg.created_at)
            };
          } else {
            return {
              id: msg.message_id,
              sender: 'assistant',
              response: msg.message_text,
              sql: msg.sql_query || '',
              plan_analysis: msg.plan_analysis || '',
              results: msg.sql_results || [],
              error: msg.error_message || '',
              timestamp: new Date(msg.created_at),
              hasPlanAnalysis: !!msg.plan_analysis,
              showNoResults: msg.sql_results && Array.isArray(msg.sql_results) && msg.sql_results.length === 0
            };
          }
        });

        console.log(`대화 ${conversationId}의 메시지 ${conversation.messages.length}개 로드됨`);
      } catch (error) {
        console.error('대화 메시지 로드 실패:', error);
      }
    };

    // 예제 쿼리 전송
    const sendExampleQuery = (query) => {
      newMessage.value = query
      nextTick(() => {
        if (chatInput.value) {
          adjustTextareaHeight()
        }
        sendMessage()
      })
    }

    // 키보드 이벤트 처리
    const handleKeydown = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        sendMessage()
      }
    }

    // 메시지 전송
    const sendMessage = async () => {
      // 유저가 입력한 메세지 가져오기 
      const userMessageText = newMessage.value.trim()
      if (!userMessageText) return

      // ============================================
      // 1. 현재 대화방 찾기 (임시 대화방 포함)
      // ============================================
      let currentConversation = conversations.value.find(
        c => c.id === currentConversationId.value
      );

      // 대화방이 없으면 임시 생성 (방어 코드)
      if (!currentConversation) {
        currentConversation = {
          id: null,
          title: '새 대화',
          messages: [],
          lastMessage: new Date(),
          isTemporary: true
        };
        conversations.value.push(currentConversation);
        currentConversationId.value = null;
      }

      // ============================================
      // 2. UI에 사용자 메시지 먼저 표시
      // ============================================
      const newUserMessage = {
        id: messageIdCounter.value++,
        sender: 'user',
        text: userMessageText,
        timestamp: new Date()
      };

      currentConversation.messages.push(newUserMessage);
      currentConversation.lastMessage = new Date();

      newMessage.value = '';
      nextTick(() => {
        if (chatInput.value) {
          chatInput.value.style.height = 'auto';
        }
        scrollToBottom();
        highlightSQLCode();
      });
  
      isTyping.value = true

      try {
        // ============================================
        // 3. Django Backend API 호출
        // conversation_id가 없으면 null로 전송 → 백엔드가 자동 생성
        // ============================================
        const apiResponse = await fetch(`${API_URL}/chat/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
          },
          body: JSON.stringify({
            message: userMessageText,
            conversation_id: currentConversationId.value  // null일 수 있음 (첫 메시지인 경우)
          })
        });
    
        if (!apiResponse.ok) {
          throw new Error(`HTTP error! status: ${apiResponse.status}`);
        }

        const responseData = await apiResponse.json();

        // ============================================
        // 4. 새로 생성된 대화방 ID 업데이트 (첫 메시지인 경우)
        // ============================================
        if (!currentConversationId.value && responseData.conversation_id) {
          // 로컬 상태 업데이트
          currentConversationId.value = responseData.conversation_id;
          currentConversationSessionId.value = responseData.conversation_session_id;
          
          // 임시 대화방을 실제 대화방으로 전환
          currentConversation.id = responseData.conversation_id;
          currentConversation.title = responseData.title || userMessageText.substring(0, 30);
          currentConversation.isTemporary = false;
          
          console.log('새 대화 생성됨:', {
            conversation_id: responseData.conversation_id,
            conversation_session_id: responseData.conversation_session_id,
            title: responseData.title
          });
        }

        isTyping.value = false;

        // ============================================
        // 5. AI 응답 메시지 처리 (기존 로직 유지)
        // ============================================
        const newBotMessage = {
          id: messageIdCounter.value++,
          sender: 'assistant',
          response: responseData.response || '',
          sql: responseData.sql || '',
          plan_analysis: responseData.plan_analysis ? '' : (responseData.plan_analysis || ''),
          hasPlanAnalysis: !!(responseData.plan_analysis),
          results: responseData.results && responseData.results.length > 0 ? [] : (responseData.results || []),
          showNoResults: false,
          error: responseData.error || '',
          timestamp: new Date()
        };

        currentConversation.messages.push(newBotMessage);
        currentConversation.lastMessage = new Date();
    
        isTyping.value = false

        await nextTick();
        scrollToBottom();
        highlightSQLCode();


        // ============================================
        // 6. Plan analysis typing effect (기존 로직 유지)
        // ============================================
        // Plan analysis typing effect
        if (responseData.plan_analysis) {
          await new Promise((resolveTyping) => {
            let typingInterval;
            const fullText = responseData.plan_analysis;
            let currentIndex = 0;

            const startTyping = () => {
              typingInterval = setInterval(() => {
                if (currentIndex < fullText.length) {
                  currentIndex++;
                  const targetMessage = currentConversation.messages.find(m => m.id === newBotMessage.id);
                  if (targetMessage) {
                    targetMessage.plan_analysis = fullText.slice(0, currentIndex);
                  }
                  nextTick(() => {
                    scrollToBottom();
                  });
                } else {
                  clearInterval(typingInterval);
                  resolveTyping();
                }
              }, 30);
            };

            startTyping();
          });

          const targetMessage = currentConversation.messages.find(m => m.id === newBotMessage.id);
          if (targetMessage) {
            if (responseData.results && Array.isArray(responseData.results) && responseData.results.length > 0) {
              targetMessage.results = responseData.results;
              currentTableData.value = responseData.results;
            }else if(responseData.results && Array.isArray(responseData.results) && responseData.results.length === 0){
              newBotMessage.showNoResults = true;
            }
            await nextTick();
            scrollToBottom();
          }
        } else {
          if (responseData.results && Array.isArray(responseData.results)) {
            if(responseData.results.length > 0){
              newBotMessage.results = responseData.results;
              currentTableData.value = responseData.results;
            }else if(responseData.results.length === 0){
              newBotMessage.showNoResults = true;
            }
            nextTick(() => {
              scrollToBottom();
            });
          }
        }
      } catch (errorObject) {
        console.error('Error:', errorObject);
        let errorMessageText = '죄송합니다. 오류가 발생했습니다.';
        
        if (errorObject.message.includes('Failed to fetch')) {
          errorMessageText = 'API 서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.';
          connectionStatus.value = 'disconnected';
        } else if (errorObject.message.includes('HTTP error')) {
          errorMessageText = `서버 오류가 발생했습니다. (${errorObject.message})`;
        }

        const errorBotMessage = {
          id: messageIdCounter.value++,
          sender: 'assistant',
          error: errorMessageText,
          timestamp: new Date()
        };

        currentConversation.messages.push(errorBotMessage);
        isTyping.value = false;
        nextTick(() => {
          scrollToBottom();
          highlightSQLCode();
        });
      }
    }

    // 결과 테이블 포맷팅
    const formatResultsTable = (results) => {
      if (!results || !Array.isArray(results) || results.length === 0) {
        return '<div class="no-results">결과가 없습니다.</div>'
      }

      try {
        const columns = Object.keys(results[0])
        const totalRows = results.length
        const displayRows = results.slice(0, 100)

        let html = `
          <div class="results-table-container">
            <div class="table-info">
              <div class="table-stats">
                <span class="stat-item">총 ${totalRows.toLocaleString()}행</span>
                <span class="stat-item">${columns.length}열</span>
              </div>
              <div class="table-actions">
                <button class="table-btn" onclick="window.exportToCSV && window.exportToCSV()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  CSV 다운로드
                </button>
              </div>
            </div>
            
            <div class="table-wrapper">
              <table class="results-table">
                <thead>
                  <tr>`

        // 헤더
        columns.forEach(col => {
          const sampleValue = displayRows.find(row => row[col] !== null && row[col] !== undefined)?.[col]
          const dataType = detectDataType(sampleValue)
          html += `<th title="컬럼: ${escapeHtml(col)} (타입: ${dataType})">${escapeHtml(col)}</th>`
        })
        
        html += '</tr></thead><tbody>'

        // 데이터 행
        displayRows.forEach((row, index) => {
          html += `<tr class="${index % 2 === 0 ? 'even' : 'odd'}">`
          columns.forEach(col => {
            let value = row[col]
            let cellClass = ''

            if (value === null || value === undefined) {
              value = 'NULL'
              cellClass = 'null-cell'
            } else if (typeof value === 'object') {
              if (value.toString && value.toString().includes('Timestamp')) {
                value = value.toString().replace(/Timestamp\('(.+?)'\)/, '$1')
              } else if (value instanceof Date) {
                value = value.toLocaleString('ko-KR')
              } else {
                value = JSON.stringify(value)
              }
            } else if (typeof value === 'number') {
              cellClass = 'number-cell'
              if (Number.isInteger(value)) {
                value = value.toLocaleString()
              } else {
                value = value.toFixed(2).replace(/\.00$/, '')
              }
            } else {
              value = String(value)
            }

            const displayValue = value.length > 100 ? value.substring(0, 97) + '...' : value
            html += `<td class="${cellClass}" title="${escapeHtml(String(value))}">${
              value === 'NULL' ? '<span class="null-value">NULL</span>' : escapeHtml(String(displayValue))
            }</td>`
          })
          html += '</tr>'
        })

        html += '</tbody></table></div>'

        if (totalRows > 100) {
          html += `
            <div class="table-pagination">
              <span class="pagination-text">처음 100개 행을 표시하고 있습니다 (전체 ${totalRows.toLocaleString()}개 중)</span>
            </div>
          `
        }
        
        html += '</div>'
        return html
        
      } catch (error) {
        console.error('Error formatting table:', error)
        return '<div class="error-table">테이블을 표시하는 중 오류가 발생했습니다.</div>'
      }
    }

    // 데이터 타입 감지
    const detectDataType = (value) => {
      if (value === null || value === undefined) return 'NULL'
      if (typeof value === 'number') {
        return Number.isInteger(value) ? 'Integer' : 'Decimal'
      }
      if (typeof value === 'boolean') return 'Boolean'
      if (value instanceof Date) return 'Date'
      if (typeof value === 'object') return 'Object'
      if (typeof value === 'string') {
        if (!isNaN(Date.parse(value)) && /\d{4}-\d{2}-\d{2}/.test(value)) {
          return 'Date String'
        }
        if (!isNaN(value) && !isNaN(parseFloat(value))) {
          return 'Numeric String'
        }
        return 'String'
      }
      return 'Unknown'
    }

    // HTML 이스케이프
    const escapeHtml = (text) => {
      if (text === null || text === undefined) return ''
      const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
        '/': '&#x2F;'
      }
      return text.replace(/[&<>"']/g, m => map[m])
    }

    // CSV 내보내기 함수를 전역으로 등록
    const setupExportFunction = () => {
      window.exportToCSV = () => {
        if (!currentTableData.value) {
          alert('내보낼 데이터가 없습니다.')
          return
        }

        const data = currentTableData.value
        const columns = Object.keys(data[0])
        let csvContent = '\uFEFF'

        csvContent += columns.map(col => `"${String(col).replace(/"/g, '""')}"`).join(',') + '\n'

        data.forEach(row => {
          const values = columns.map(col => {
            let value = row[col]

            if (value === null || value === undefined) {
              return '""'
            }

            if (typeof value === 'object') {
              if (value.toString && value.toString().includes('Timestamp')) {
                value = value.toString().replace(/Timestamp\('(.+?)'\)/, '$1')
              } else if (value instanceof Date) {
                value = value.toISOString().split('T')[0]
              } else {
                value = JSON.stringify(value)
              }
            }

            const stringValue = String(value)
            const escapedValue = stringValue
              .replace(/"/g, '""')
              .replace(/\r?\n/g, ' ')
              .replace(/\t/g, ' ')

            if (escapedValue.includes(',') || escapedValue.includes('"') || escapedValue.includes('\n') || escapedValue.includes('\r')) {
              return `"${escapedValue}"`
            }

            return `"${escapedValue}"`
          })
          csvContent += values.join(',') + '\n'
        })

        const blob = new Blob([csvContent], {
          type: 'text/csv;charset=utf-8;'
        })

        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        link.setAttribute('href', url)

        const filename = `쿼리결과_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`
        link.setAttribute('download', filename)

        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
      }
    }

    // ========================================
    // 새 대화 버튼 클릭 시 로컬에서만 임시 대화방 생성
    // ========================================
    const createNewChat = () => {
      // 서버 호출 없이 로컬에서만 상태 초기화
      currentConversationId.value = null
      currentConversationSessionId.value = null
      
      // UI에 빈 대화방 추가 (임시)
      const tempConversation = {
        id: null,  // 아직 서버에 생성 안 됨
        title: '새 대화',
        lastMessage: new Date(),
        messages: [],
        isTemporary: true  // 임시 플래그
      }
      
      conversations.value.unshift(tempConversation)
      currentConversationId.value = null
      console.log('새 대화 준비 (서버 생성 안 됨)')
    }

    // 새 채팅 생성 이전 버전 기록
    // const createNewChat = () => {
    //   const newConversation = {
    //     id: conversationIdCounter.value++,
    //     title: '새 대화',
    //     lastMessage: new Date(),
    //     messages: []
    //   }

    //   conversations.value.unshift(newConversation)
    //   currentConversationId.value = newConversation.id
    //   conversationHistory.value = []

    //   nextTick(() => {
    //     scrollToBottom()
    //   })
    // }

    const highlightSQLCode = () => {
      nextTick(() => {
        document.querySelectorAll('code.language-sql').forEach((block) => {
          Prism.highlightElement(block)
        })
      })
    }

    // 클립보드 복사 함수
    const copyQueryToClipboard = async (query, messageId) => {
      try {
        await navigator.clipboard.writeText(query)
        copiedStates[messageId] = true
        showCopyToast.value = true
        
        setTimeout(() => {
          showCopyToast.value = false
        }, 3000)

        setTimeout(() => {
          copiedStates[messageId] = false
        }, 2000)

      } catch (err) {
        console.error('복사 실패:', err)
        fallbackCopy(query, messageId)
      }
    }

    const fallbackCopy = (text, messageId) => {
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      
      try {
        document.execCommand('copy')
        copiedStates[messageId] = true
        showCopyToast.value = true
        
        setTimeout(() => {
          showCopyToast.value = false
        }, 3000)
        
        setTimeout(() => {
          copiedStates[messageId] = false
        }, 2000)
      } catch (err) {
        console.error('폴백 복사 실패:', err)
      }
      
      document.body.removeChild(textArea)
    }

    // 대화 전환
    const switchConversation = (conversationId) => {
      currentConversationId.value = conversationId
      conversationHistory.value = []
      nextTick(() => {
        scrollToBottom()
        highlightSQLCode()
      })
    }

    // 대화 삭제
    const deleteConversation = async (conversationId) => {
      if (!confirm('이 대화를 삭제하시겠습니까?')) {
        return;
      }

      try {
        const response = await fetch(`${API_URL}/conversations/${conversationId}/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('sessionToken')}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 로컬에서도 제거
        const index = conversations.value.findIndex(c => c.id === conversationId);
        if (index !== -1) {
          conversations.value.splice(index, 1);
        }

        // 삭제한 대화가 현재 선택된 대화였다면 다른 대화 선택
        if (currentConversationId.value === conversationId) {
          if (conversations.value.length > 0) {
            await selectConversation(conversations.value[0].id);
          } else {
            currentConversationId.value = null;
            currentConversationSessionId.value = null;
          }
        }

        console.log(`대화 ${conversationId} 삭제 완료`);
      } catch (error) {
        console.error('대화 삭제 실패:', error);
        alert('대화 삭제에 실패했습니다.');
      }
    };

    // 사이드바 토글
    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value
    }

    // 시간 포맷팅
    const formatTime = (timestamp) => {
      return timestamp.toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 날짜 포맷팅
    const formatDate = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp

      if (diff < 86400000) { // 24시간 이내
        return formatTime(timestamp)
      } else if (diff < 604800000) { // 7일 이내
        return timestamp.toLocaleDateString('ko-KR', {
          weekday: 'short'
        })
      } else {
        return timestamp.toLocaleDateString('ko-KR', {
          month: 'short',
          day: 'numeric'
        })
      }
    }

    // 스크롤을 하단으로
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatMessages.value) {
          chatMessages.value.scrollTop = chatMessages.value.scrollHeight
        }
      })
    }

    // 텍스트에어리어 높이 조절
    const adjustTextareaHeight = () => {
      nextTick(() => {
        if (chatInput.value) {
          chatInput.value.style.height = 'auto'
          chatInput.value.style.height = Math.min(chatInput.value.scrollHeight, 120) + 'px'
        }
      })
    }

    // 초기화
    onMounted(async () => {
      if (!checkAuth()) {
        return
      }
      
      createNewChat()
      checkAPIConnection()
      setupExportFunction()
      await loadConversations();

      nextTick(() => {
        scrollToBottom()
        highlightSQLCode()
      })
    })

    return {
      // 반응형 데이터
      conversations,
      currentConversationId,
      currentMessages,
      newMessage,
      isTyping,
      isSidebarCollapsed,
      connectionStatus,
      connectionText,
      suggestions,
      isAdmin,

      // 템플릿 참조
      chatMessages,
      chatInput,
      sendButton,

      // 복사 기능 관련
      copiedStates,
      showCopyToast,
      copyQueryToClipboard,

      // 메소드
      sendMessage,
      sendExampleQuery,
      createNewChat,
      switchConversation,
      deleteConversation,
      toggleSidebar,
      formatTime,
      formatDate,
      adjustTextareaHeight,
      formatResultsTable,
      handleKeydown,
      logout,
      checkAuth,
      getConversationPreview,
      goToSQLManage
    }
  }
}
</script>

<style src="@/css/chat.css" scoped></style>