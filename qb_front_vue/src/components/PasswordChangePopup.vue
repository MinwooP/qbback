<template>
  <div v-if="show" class="popup-overlay" @click="handleOverlayClick">
    <div class="popup-container" @click.stop>
      <div class="popup-header">
        <h3>비밀번호 변경 필요</h3>
      </div>
      
      <div class="popup-content">
        <div class="warning-icon">
          ⚠️
        </div>
        <p>현재 초기 비밀번호를 사용 중입니다.<br>보안을 위해 비밀번호 변경이 필요합니다.</p>
        <p class="sub-text">지금 변경하시겠습니까?</p>
      </div>
      
      <div class="popup-actions">
        <button class="later-btn" @click="handleLater">
          다음에 변경하기
        </button>
        <button class="change-btn" @click="handleChange">
          변경하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue'

defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['change', 'later', 'close'])

const handleChange = () => {
  emit('change')
}

const handleLater = () => {
  emit('later')
}

const handleOverlayClick = () => {
  // 오버레이 클릭 시 팝업 닫기 (선택사항)
  // emit('close')
}
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.popup-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-width: 400px;
  width: calc(100% - 40px);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.popup-header {
  padding: 24px 24px 0 24px;
  text-align: center;
}

.popup-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.popup-content {
  padding: 20px 24px;
  text-align: center;
}

.warning-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

.popup-content p {
  color: #374151;
  line-height: 1.6;
  margin: 0 0 12px 0;
  font-size: 16px;
}

.sub-text {
  font-weight: 600;
  color: #1e293b;
  font-size: 16px;
}

.popup-actions {
  padding: 0 24px 24px 24px;
  display: flex;
  gap: 12px;
}

.later-btn {
  flex: 1;
  padding: 12px 20px;
  background: #f8fafc;
  color: #64748b;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.later-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
  transform: translateY(-1px);
}

.change-btn {
  flex: 1;
  padding: 12px 20px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.change-btn:hover {
  background: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.change-btn:active {
  transform: translateY(0);
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .popup-container {
    width: calc(100% - 20px);
  }
  
  .popup-actions {
    flex-direction: column;
  }
  
  .warning-icon {
    font-size: 40px;
  }
}
</style>