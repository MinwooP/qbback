<template>
  <div class="chatbot-container">
    <!-- 왼쪽 사이드바 - 대화 이력 -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }" v-if="!isSidebarCollapsed">
      <div class="sidebar-header">
        <div class="sidebar-brand">
          <div class="brand-icon">
            <img src="@/images/qb_web.png" alt="Logo" class="title-icon" />
          </div>
          <div class="brand-text">
            <div class="brand-title">Query Buddy Admin</div>
            <div class="brand-subtitle">Database Management</div>
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
        <button class="new-chat-btn" @click="goToChat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          채팅으로 이동
        </button>

        <div class="conversation-items">
          <div class="admin-menu-item" :class="{ active: activeTab === 'schema' }" @click="activeTab = 'schema'">
            <div class="conversation-content">
              <div class="conversation-title">스키마 관리</div>
              <div class="conversation-preview">데이터베이스 스키마 관리</div>
            </div>
          </div>
          
          <div class="admin-menu-item" :class="{ active: activeTab === 'sql' }" @click="activeTab = 'sql'">
            <div class="conversation-content">
              <div class="conversation-title">SQL 관리</div>
              <div class="conversation-preview">SQL 쿼리 템플릿 관리</div>
            </div>
          </div>
          <button class="vectorize-btn" @click="vectorizeData">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; margin-right: 6px; vertical-align: middle;">
              <polyline points="23 4 23 10 17 10" />
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
            벡터화 처리
          </button>
        </div>
      </div>

      <!-- 사이드바 하단 정보 -->
      <div class="sidebar-footer" v-if="!isSidebarCollapsed">
        <div class="connection-info pulse-effect">
          <!-- <div class="status-dot connected"></div> -->
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
          </svg>
          <span class="status-text">관리자 모드</span>
        </div>
        <button @click="logout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4m7 14l5-5-5-5m5 5H9"/>
          </svg>
          로그아웃
        </button>
      </div>
    </div>

    <!-- 메인 관리 영역 -->
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
          <div class="header-title">Query Buddy Admin</div>
        </div>
        <div class="header-right">
          <span class="status-text">
            <svg width="16" height="16" viewBox="0 0 28 16" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
            관리자 모드</span>
          <button @click="logout" class="header-logout-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4m7 14l5-5-5-5m5 5H9"/>
            </svg>
            로그아웃
          </button>
        </div>
      </div>

      <!-- 관리 콘텐츠 영역 -->
      <div class="chat-messages admin-content">
        <!-- Schema Management Tab -->
        <div v-if="activeTab === 'schema'" class="tab-content">
          <div class="content-header">
            <h2>스키마 관리</h2>
            <button class="btn btn-primary" @click="toggleSchemaForm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14m7-7H5"/>
              </svg>
              {{ showSchemaForm ? '취소' : '새 스키마 추가' }}
            </button>
          </div>

          <!-- 검색창 추가 -->
          <div class="search-container">
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <input 
              type="text" 
              v-model="schemaSearchQuery" 
              class="search-input"
              placeholder="스키마명으로 검색..."
            >
          </div>

          <!-- Schema Table -->
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>NO.</th>
                  <th>스키마명</th>
                  <th>설명</th>
                  <th>액션</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="schema in filteredSchemas" :key="schema.id" @click="viewSchema(schema)" style="cursor: pointer;">
                  <td>{{ schema.id }}</td>
                  <td class="schema-name">{{ schema.name }}</td>
                  <td class="description">{{ schema.description }}</td>
                  <td class="actions">
                    <button class="btn-icon btn-view" @click.stop="viewSchema(schema)">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                    <button class="btn-icon btn-delete" @click.stop="deleteSchema(schema.id)">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Schema View -->
          <div v-if="showSchemaView" class="inline-form-container">
            <div class="inline-form" :class="{ 'edit-mode': isEditingInSchemaView }">
              <div class="form-header">
                <h3>{{ viewingSchema?.name }} {{ isEditingInSchemaView ? '- 편집' : '- 상세보기' }}</h3>
                <div class="header-actions" style="gap:5px;">
                  <!-- 편집 모드가 아닐 때 -->
                  <template v-if="!isEditingInSchemaView">
                    <button type="button" class="btn btn-primary" style="margin-right:5px;" @click="startEditInSchemaView">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                      편집
                    </button>
                    <button type="button" class="btn btn-outline" @click="closeSchemaView">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                      닫기
                    </button>
                  </template>
                  
                  <!-- 편집 모드일 때 -->
                  <template v-if="isEditingInSchemaView">
                    <button type="button" class="btn btn-primary" style="margin-right:5px;" @click="saveEditInSchemaView">
                      저장
                    </button>
                    <button type="button" class="btn btn-outline" @click="cancelEditInSchemaView">
                      취소
                    </button>
                  </template>
                </div>
              </div>
              
              <div class="sql-view-content">
                <!-- 읽기 모드 -->
                <template v-if="!isEditingInSchemaView">
                  <div class="view-layout">
                    <!-- 좌측 영역 -->
                    <div class="view-left">
                      <div class="info-item">
                        <label>스키마명</label>
                        <span class="schema-name">{{ viewingSchema?.name }}</span>
                      </div>
                      
                      <div v-if="viewingSchema?.description" class="info-item">
                        <label>설명</label>
                        <p>{{ viewingSchema.description }}</p>
                      </div>
                      
                      <div class="info-item">
                        <label>스키마 정의 (JSON)</label>
                        <div class="sql-query-display">
                          <pre>{{ viewingSchema?.definition }}</pre>
                          <button type="button" class="copy-sql-btn" @click="copySchemaDefinition" title="스키마 정의 복사">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 우측 영역 (동의어) -->
                    <div class="view-right">
                      <div class="info-item">
                        <label>동의어</label>
                        <div v-if="viewingSchema?.synonyms && viewingSchema.synonyms.length > 0" class="synonyms-tags">
                          <span v-for="(synonym, index) in viewingSchema.synonyms" :key="index" class="synonym-tag">
                            {{ synonym }}
                          </span>
                        </div>
                        <span v-else class="no-data">등록된 동의어가 없습니다.</span>
                      </div>
                    </div>
                  </div>
                </template>
                
                <!-- 편집 모드 -->
                  <template v-if="isEditingInSchemaView">
                    <div class="form-layout">
                      <!-- 좌측 영역 -->
                      <div class="form-left">
                        <div class="form-group">
                          <label>스키마명</label>
                          <input 
                            type="text" 
                            v-model="viewSchemaEditForm.name" 
                            class="form-input"
                            placeholder="스키마명을 입력하세요"
                            disabled
                            required
                          >
                        </div>
                        
                        <div class="form-group">
                          <label>설명</label>
                          <textarea 
                            v-model="viewSchemaEditForm.description" 
                            class="form-textarea"
                            placeholder="스키마 설명을 입력하세요"
                            rows="3"
                          ></textarea>
                        </div>
                        
                        <div class="form-group">
                          <label>스키마 정의 (JSON)</label>
                          <textarea 
                            v-model="viewSchemaEditForm.definition" 
                            class="form-textarea code-input"
                            placeholder='{"tables": [], "relationships": []}'
                            rows="12"
                            required
                          ></textarea>
                        </div>
                      </div>
                      
                      <!-- 우측 영역 -->
                      <div class="form-right">
                        <div class="form-group">
                          <label>동의어</label>
                          <div class="synonym-container">
                            <div class="synonym-row" v-for="(synonym, index) in viewSchemaEditForm.synonyms" :key="index">
                              <input 
                                type="text" 
                                v-model="viewSchemaEditForm.synonyms[index]" 
                                class="form-input synonym-input"
                                :placeholder="index === 0 ? '동의어를 추가하세요' : `동의어 ${index + 1}`"
                              >
                              <button 
                                v-if="index === viewSchemaEditForm.synonyms.length - 1" 
                                type="button"
                                @click="viewSchemaEditForm.synonyms.push('')" 
                                class="btn btn-primary synonym-add-btn"
                                title="동의어 추가"
                              >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                  <path d="M12 5v14m7-7H5"/>
                                </svg>
                              </button>
                              <button 
                                v-if="viewSchemaEditForm.synonyms.length > 1" 
                                type="button"
                                @click="viewSchemaEditForm.synonyms.splice(index, 1)" 
                                class="btn btn-danger synonym-remove-btn"
                                title="동의어 삭제"
                              >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                  <path d="M18 6L6 18M6 6l12 12"/>
                                </svg>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
              </div>
            </div>
          </div>

          <!-- Schema Form -->
          <div v-if="showSchemaForm" class="inline-form-container">
            <div class="inline-form edit-mode">
              <div class="form-header">
                <h3>{{ editingSchema ? '스키마 수정' : '새 스키마 추가' }}</h3>
              </div>
              <form @submit.prevent="saveSchema" class="form-layout">
                <!-- 좌측 영역 (2/3) -->
                <div class="form-left">
                  <div class="form-group">
                    <label>스키마명</label>
                    <input 
                      type="text" 
                      v-model="schemaForm.name" 
                      class="form-input"
                      placeholder="스키마명을 입력하세요"
                      :disabled="editingSchema !== null"
                      required
                    >
                  </div>
                  
                  <div class="form-group">
                    <label>설명</label>
                    <textarea 
                      v-model="schemaForm.description" 
                      class="form-textarea"
                      placeholder="스키마 설명을 입력하세요"
                      rows="3"
                    ></textarea>
                  </div>
                  
                  <div class="form-group">
                    <label>스키마 정의 (JSON)</label>
                    <textarea 
                      v-model="schemaForm.definition" 
                      class="form-textarea code-input"
                      placeholder='{"tables": [], "relationships": []}'
                      rows="8"
                      required
                    ></textarea>
                  </div>
                </div>
                
                <!-- 우측 영역 (1/3) -->
                <div class="form-right">
                  <div class="form-group">
                    <label>동의어</label>
                    <div class="synonym-container">
                      <div class="synonym-row" v-for="(synonym, index) in schemaForm.synonyms" :key="index">
                        <input 
                          type="text" 
                          v-model="schemaForm.synonyms[index]" 
                          class="form-input synonym-input"
                          :placeholder="index === 0 ? '동의어를 추가하세요' : `동의어 ${index + 1}`"
                        >
                        <button 
                          v-if="index === schemaForm.synonyms.length - 1" 
                          type="button"
                          @click="addSynonym" 
                          class="btn btn-primary synonym-add-btn"
                          title="동의어 추가"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 5v14m7-7H5"/>
                          </svg>
                        </button>
                        <button 
                           v-if="schemaForm.synonyms.length > 1" 
                            type="button"
                            @click="removeSynonym(index)" 
                            class="btn btn-danger synonym-remove-btn"
                            title="동의어 삭제"
                          >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 버튼 영역 -->
                  <div class="form-actions full-width">
                    <button type="button" class="btn btn-outline" @click="cancelSchemaForm">
                      취소
                    </button>
                    <button type="submit" class="btn btn-primary">
                      {{ editingSchema ? '수정' : '저장' }}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

        </div>

        <!-- SQL Management Tab -->
        <div v-if="activeTab === 'sql'" class="tab-content">
          <div class="content-header">
            <h2>SQL 관리</h2>
            <button class="btn btn-primary" @click="toggleSqlForm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14m7-7H5"/>
              </svg>
              {{ showSqlForm ? '취소' : '새 SQL 추가' }}
            </button>
          </div>

          <!-- 검색창 추가 -->
          <div class="search-container">
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <input 
              type="text" 
              v-model="sqlSearchQuery" 
              class="search-input"
              placeholder="제목으로 검색..."
            >
          </div>

          <!-- SQL Table -->
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>제목</th>
                  <th>유형</th>
                  <th>스키마</th>
                  <th>액션</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sql in filteredSqlQueries" :key="sql.id" @click="viewSql(sql)" style="cursor: pointer;">
                  <td>{{ sql.id }}</td>
                  <td class="sql-title">{{ sql.title }}</td>
                  <td class="sql-type">
                    <span :class="'type-' + sql.type">{{ sql.type }}</span>
                  </td>
                  <td>{{ sql.schema_name }}</td>
                  <td class="actions">
                    <button class="btn-icon btn-view" @click.stop="viewSql(sql)">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                    <button class="btn-icon btn-delete" @click.stop="deleteSql(sql.id)">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="showSqlView" class="inline-form-container">
            <div class="inline-form" :class="{ 'edit-mode': isEditingInView }">
              <div class="form-header">
                <h3>{{ viewingSql?.title }} {{ isEditingInView ? '- 편집' : '- 상세보기' }}</h3>
                <div class="header-actions" style="gap:5px;">
                  <!-- 편집 모드가 아닐 때 -->
                  <template v-if="!isEditingInView">
                    <button type="button" class="btn btn-primary" style="margin-right:5px;" @click="startEditInView">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                      편집
                    </button>
                    <button type="button" class="btn btn-outline" @click="closeSqlView">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                      닫기
                    </button>
                  </template>
                  
                  <!-- 편집 모드일 때 -->
                  <template v-if="isEditingInView">
                    <button type="button" class="btn btn-primary" style="margin-right:5px;" @click="saveEditInView">
                      저장
                    </button>
                    <button type="button" class="btn btn-outline" @click="cancelEditInView">
                      취소
                    </button>
                  </template>
                </div>
              </div>
              
              <div class="sql-view-content">
                <!-- 읽기 모드 -->
                <template v-if="!isEditingInView">
                  <div class="view-layout">
                    <!-- 좌측 영역 -->
                    <div class="view-left">
                      <div class="sql-info-grid">
                        <div class="info-item">
                          <label>유형</label>
                          <span :class="'type-' + viewingSql?.type" class="sql-type-badge">{{ viewingSql?.type }}</span>
                        </div>
                        <div class="info-item">
                          <label>스키마</label>
                          <span>{{ viewingSql?.schema_name }}</span>
                        </div>
                      </div>
                      
                      <div v-if="viewingSql?.description" class="sql-description-section">
                        <label>설명</label>
                        <p>{{ viewingSql.description }}</p>
                      </div>

                      <div class="sql-query-section">
                        <label>SQL 쿼리</label>
                        <div class="sql-query-display">
                          <pre>{{ viewingSql?.query }}</pre>
                          <button type="button" class="copy-sql-btn" @click="copySqlToClipboard" title="SQL 복사">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 우측 영역 (동의어) -->
                    <div class="view-right">
                      <div class="info-item">
                        <label>동의어</label>
                        <div v-if="viewingSql?.synonyms && viewingSql.synonyms.length > 0" class="synonyms-tags">
                          <span v-for="(synonym, index) in viewingSql.synonyms" :key="index" class="synonym-tag">
                            {{ synonym }}
                          </span>
                        </div>
                        <span v-else class="no-data">등록된 동의어가 없습니다.</span>
                      </div>
                    </div>
                  </div>
                </template>
                
                <!-- 편집 모드 -->
                <template v-if="isEditingInView">
                  <div class="form-layout">
                    <!-- 좌측 영역 -->
                    <div class="form-left">
                      <div class="form-group">
                        <label>제목</label>
                        <input 
                          type="text" 
                          v-model="viewEditForm.title" 
                          class="form-input"
                          placeholder="SQL 제목을 입력하세요"
                          required
                        >
                      </div>
                      
                      <div class="form-group">
                        <label>유형</label>
                        <select v-model="viewEditForm.type" class="form-select" required>
                          <option value="">선택하세요</option>
                          <option value="SELECT">SELECT</option>
                          <option value="INSERT">INSERT</option>
                          <option value="UPDATE">UPDATE</option>
                          <option value="DELETE">DELETE</option>
                          <option value="CREATE">CREATE</option>
                          <option value="DROP">DROP</option>
                        </select>
                      </div>
                      
                      <div class="form-group">
                        <label>스키마 선택</label>
                        <select v-model="viewEditForm.schema_id" class="form-select" required>
                          <option value="">선택하세요</option>
                          <option v-for="schema in schemas" :key="schema.id" :value="schema.id">
                            {{ schema.name }}
                          </option>
                        </select>
                      </div>
                      
                      <div class="form-group">
                        <label>SQL 쿼리</label>
                        <textarea 
                          v-model="viewEditForm.query" 
                          class="form-textarea code-input"
                          placeholder="SQL 쿼리를 입력하세요"
                          rows="8"
                          required
                        ></textarea>
                      </div>
                      
                      <div class="form-group">
                        <label>설명</label>
                        <textarea 
                          v-model="viewEditForm.description" 
                          class="form-textarea"
                          placeholder="SQL 설명을 입력하세요"
                          rows="3"
                        ></textarea>
                      </div>
                    </div>
                    
                    <!-- 우측 영역 -->
                    <div class="form-right">
                      <div class="form-group">
                        <label>동의어</label>
                        <div class="synonym-container">
                          <div class="synonym-row" v-for="(synonym, index) in viewEditForm.synonyms" :key="index">
                            <input 
                              type="text" 
                              v-model="viewEditForm.synonyms[index]" 
                              class="form-input synonym-input"
                              :placeholder="index === 0 ? '동의어를 추가하세요' : `동의어 ${index + 1}`"
                            >
                            <button 
                              v-if="index === viewEditForm.synonyms.length - 1" 
                              type="button"
                              @click="viewEditForm.synonyms.push('')" 
                              class="btn btn-primary synonym-add-btn"
                              title="동의어 추가"
                            >
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 5v14m7-7H5"/>
                              </svg>
                            </button>
                            <button 
                              v-if="viewEditForm.synonyms.length > 1" 
                              type="button"
                              @click="viewEditForm.synonyms.splice(index, 1)" 
                              class="btn btn-danger synonym-remove-btn"
                              title="동의어 삭제"
                            >
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M18 6L6 18M6 6l12 12"/>
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- SQL Form -->
          <div v-if="showSqlForm" class="inline-form-container">
            <div class="inline-form edit-mode">
              <div class="form-header">
                <h3>{{ editingSql ? 'SQL 수정' : '새 SQL 추가' }}</h3>
              </div>
              <form @submit.prevent="saveSql" class="form-layout">
                <!-- 좌측 영역 (2/3) -->
                <div class="form-left">
                  <div class="form-group">
                    <label>제목</label>
                    <input 
                      type="text" 
                      v-model="sqlForm.title" 
                      class="form-input"
                      placeholder="SQL 제목을 입력하세요"
                      required
                    >
                  </div>
                  
                  <div class="form-group">
                    <label>유형</label>
                    <select v-model="sqlForm.type" class="form-select" required>
                      <option value="">선택하세요</option>
                      <option value="SELECT">SELECT</option>
                      <option value="INSERT">INSERT</option>
                      <option value="UPDATE">UPDATE</option>
                      <option value="DELETE">DELETE</option>
                      <option value="CREATE">CREATE</option>
                      <option value="DROP">DROP</option>
                    </select>
                  </div>
                  
                  <div class="form-group">
                    <label>스키마 선택</label>
                    <select v-model="sqlForm.schema_id" class="form-select" required>
                      <option value="">선택하세요</option>
                      <option v-for="schema in schemas" :key="schema.id" :value="schema.id">
                        {{ schema.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label>설명</label>
                    <textarea 
                      v-model="sqlForm.description" 
                      class="form-textarea"
                      placeholder="SQL 설명을 입력하세요"
                      rows="3"
                    ></textarea>
                  </div>
                  
                  <div class="form-group">
                    <label>SQL 쿼리</label>
                    <textarea 
                      v-model="sqlForm.query" 
                      class="form-textarea code-input"
                      placeholder="SQL 쿼리를 입력하세요"
                      rows="8"
                      required
                    ></textarea>
                  </div>

                </div>
                
                <!-- 우측 영역 (1/3) -->
                <div class="form-right">
                  <div class="form-group">
                    <label>동의어</label>
                    <div class="synonym-container">
                      <div class="synonym-row" v-for="(synonym, index) in sqlForm.synonyms" :key="index">
                        <input 
                          type="text" 
                          v-model="sqlForm.synonyms[index]" 
                          class="form-input synonym-input"
                          :placeholder="index === 0 ? '동의어를 추가하세요' : `동의어 ${index + 1}`"
                        >
                        <button 
                          v-if="index === sqlForm.synonyms.length - 1" 
                          type="button"
                          @click="sqlForm.synonyms.push('')" 
                          class="btn btn-primary synonym-add-btn"
                          title="동의어 추가"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 5v14m7-7H5"/>
                          </svg>
                        </button>
                        <button 
                          v-if="sqlForm.synonyms.length > 1" 
                          type="button"
                          @click="sqlForm.synonyms.splice(index, 1)" 
                          class="btn btn-danger synonym-remove-btn"
                          title="동의어 삭제"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 버튼 영역 -->
                  <div class="form-actions">
                    <button type="button" class="btn btn-outline" @click="cancelSqlForm">
                      취소
                    </button>
                    <button type="submit" class="btn btn-primary">
                      {{ editingSql ? '수정' : '저장' }}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>처리 중...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SQLManage',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(false)
    const activeTab = ref('schema')
    const isSidebarCollapsed = ref(false)
    
    // Schema data
    const schemas = ref([])
    const filteredSchemas = ref([])
    const schemaSearchQuery = ref('')
    const showSchemaForm = ref(false)
    const showSchemaView = ref(false)
    const editingSchema = ref(null)
    const viewingSchema = ref(null) 
    const isEditingInSchemaView = ref(false)
    const schemaForm = reactive({
      name: '',
      description: '',
      definition: '',
      synonyms: [''] // 동의어 배열 추가
    })
    const viewSchemaEditForm = reactive({
      name: '',
      description: '',
      definition: '',
      synonyms: ['']
    })

    const viewSchema = (schema) => {
      viewingSchema.value = schema
      showSchemaView.value = true
    }
    const closeSchemaView = () => {
      showSchemaView.value = false
      viewingSchema.value = null
      isEditingInSchemaView.value = false
    }
    const startEditInSchemaView = () => {
      Object.assign(viewSchemaEditForm, {
        name: viewingSchema.value.name,
        description: viewingSchema.value.description,
        definition: viewingSchema.value.definition,
        synonyms: (viewingSchema.value.synonyms && viewingSchema.value.synonyms.length > 0) 
          ? [...viewingSchema.value.synonyms] 
          : [''] 
      })
      isEditingInSchemaView.value = true
    }

    const cancelEditInSchemaView = () => {
      isEditingInSchemaView.value = false
      Object.assign(viewSchemaEditForm, {
        name: '',
        description: '',
        definition: '',
        synonyms: ['']
      })
    }

    const saveEditInSchemaView = async () => {
      const filteredSynonyms = viewSchemaEditForm.synonyms.filter(synonym => synonym.trim() !== '')
      
      if (filteredSynonyms.length === 0) {
        alert('동의어를 최소 1개 이상 입력해주세요.')
        return
      }

      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const index = schemas.value.findIndex(s => s.id === viewingSchema.value.id)
        if (index !== -1) {
          schemas.value[index] = {
            ...schemas.value[index],
            description: viewSchemaEditForm.description,
            definition: viewSchemaEditForm.definition,
            synonyms: filteredSynonyms,
            updated_at: new Date().toISOString()
          }
          
          viewingSchema.value = schemas.value[index]
        }
        
        isEditingInSchemaView.value = false
        alert('스키마가 수정되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const copySchemaDefinition = async () => {
      try {
        await navigator.clipboard.writeText(viewingSchema.value.definition)
        alert('스키마 정의가 복사되었습니다.')
      } catch (error) {
        alert('복사에 실패했습니다.')
      }
    }

    const searchSchemas = () => {
      if (!schemaSearchQuery.value.trim()) {
        filteredSchemas.value = schemas.value
      } else {
        filteredSchemas.value = schemas.value.filter(schema => 
          schema.name.toLowerCase().includes(schemaSearchQuery.value.toLowerCase())
        )
      }
    }

    // SQL data
    const sqlQueries = ref([])
    const filteredSqlQueries = ref([])
    const sqlSearchQuery = ref('')
    const showSqlForm = ref(false)
    const showSqlView = ref(false)
    const editingSql = ref(null)
    const viewingSql = ref(null)
    const sqlForm = reactive({
      title: '',
      type: '',
      schema_id: '',
      query: '',
      description: '',
      synonyms: ['']
    })

    // Mock data for demonstration
    const initializeMockData = () => {
      schemas.value = [
        {
          id: 1,
          name: 'abc_cont',
          description: '캠페인 수행을 위한 동의여부 및 부수적인 회선 정보 테이블',
          definition: '{\n"table_name": "abc_cont",\n"description": "서비스 계약(회선) 정보 테이블",\n"primary_key": {\n  "columns": ["svc_cont_id"],\n  "description": "서비스계약 아이디"\n},\n"columns": [\n  {\n    "name": "svc_cont_id",\n    "type": "string",\n    "nullable": false,\n    "description": "서비스계약 아이디"\n  },\n  {\n    "name": "src_cust_sorc_id",\n    "type": "string",\n    "nullable": true,\n    "description": "원천고객 소스 아이디"\n  },\n  {\n    "name": "sbsc_aftr_elaps_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "가입후 경과 개월수, 가능한 값 : [1~37]"\n  },\n  {\n    "name": "comb_engt_exp_rmnd_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "결합약정 만료잔여 개월수, 가능한 값 : [-37~37] (음수(-):약정만료까지 남은 개월, 양수(+):약정만료 경과 개월수)"\n  },\n  {\n    "name": "engt_exp_rperd_itg_cd",\n    "type": "string",\n    "nullable": true,\n    "description": "약정만료 잔여기간 통합코드, 가능한 값 : [-37~37] (음수(-):약정만료까지 남은 개월, 양수(+):약정만료 경과 개월수)"\n  },\n  {\n    "name": "engt_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "약정여부, 가능한 값 : [Y:약정, N:미약정]"\n  },\n  {\n    "name": "engt_rmnd_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "약정만료 개월수, 가능한 값 : [-37~37] (음수(-):약정만료까지 남은 개월, 양수(+):약정만료 경과 개월수)"\n  },\n  {\n    "name": "cont_sttus_group_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "계약상태그룹명, 가능한 값: [정지중, 해지, 사용중]"\n  },\n  {\n    "name": "mphon_comb_circuit_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "이동전화결합회선수(모바일결합회선수)"\n  },\n  {\n    "name": "inet_comb_circuit_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "인터넷결합회선수"\n  },\n  {\n    "name": "pstn_comb_circuit_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "PSTN결합회선수(일반전화결합회선수)"\n  },\n  {\n    "name": "hndset_model_div_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "단말기모델 구분명",\n    "valid_values": [\n      {\n        "value": "",\n        "desc": "SoIP서비스, APT_AT203-308W 등 단말기의 모델이 구분되지 않는 회선"\n      },\n      { "value": "스마트폰", "desc": "모바일 상품의 스마트폰 회선" },\n      { "value": "패드", "desc": "모바일 상품의 패드 회선" }\n    ]\n  },\n  {\n    "name": "svc_use_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "서비스 사용 개월수, 가능한 값: 0~9999"\n  },\n  {\n    "name": "hndset_model_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "단말기모델명(모바일:단말기모델, 유선:장비명)"\n  },\n  {\n    "name": "entr_prod_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "단말기모델 전사상품명",\n    "valid_values": [\n      {\n        "value": "기업용인터넷전화폰(Biz)",\n        "desc": "기업 또는 공공기관 사무실에서 쓰는 IP기반 전화기 단말기"\n      },\n      {\n        "value": "LTE 스마트폰",\n        "desc": "LTE 기술을 지원하는 스마트폰을 의미합니다. LTE는 고속 데이터 전송을 가능하게 하여 이동 중에도 빠른 인터넷 접속을 제공하는 점에서 중요한 기술"\n      },\n      {\n        "value": "홈인터넷전화폰",\n        "desc": "홈 환경에서 사용되는 인터넷 전화 폰을 뜻합니다. 가정용으로 디자인된 제품으로, 가정 어디에서나 안정적인 통신을 지원하는 것을 강조"\n      },\n      {\n        "value": "5G 스마트폰",\n        "desc": "5G 네트워크를 지원하는 스마트폰을 의미하며, 5G 기술은 초고속 데이터 전송 및 저지연성을 제공하여 혁신적인 모바일 경험을 가능"\n      },\n      {\n        "value": "",\n        "desc": "GiGA WiFi home, xDSL 모뎀, KAO_KG3100_샌드그레이, MAU4800D_LW_릴리화이트 등의 단말기 상품"\n      }\n    ]\n  },\n  {\n    "name": "cust_dtl_ctg_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "고객상세분류명",\n    "valid_values": [\n      {\n        "value": "MASS",\n        "desc": "개인 사업자"\n      },\n      {\n        "value": "법인",\n        "desc": "법인 고객을 대상으로 한 서비스를 나타내며, 비즈니스 고객군을 의미합니다."\n      },\n      {\n        "value": "AM",\n        "desc": "대기업"\n      },\n      {\n        "value": "가치",\n        "desc": "개인 고객 중 114게재(상호명) 등록되었거나 세금정보 등록된 고객"\n      },\n      {\n        "value": "APT",\n        "desc": "아파트 거주 고객을 대상으로 하는 세그먼트로, 특정 거주 형태나 위치 기반의 타겟 마케팅을 위한 정보"\n      }\n    ]\n  },\n  {\n    "name": "new_date",\n    "type": "string",\n    "nullable": true,\n    "description": "신규일자. 값 형식 : YYYYMMDD"\n  },\n  {\n    "name": "now_hndset_use_day_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "현 단말기 사용일수, 가능한 값 : 0~9999"\n  },\n  {\n    "name": "spnsr_engt_exp_pam_date",\n    "type": "string",\n    "nullable": true,\n    "description": "스폰서 약정만료 예정일자(스폰서:단말기약정)"\n  },\n  {\n    "name": "no_mov_pre_bizr_itg_cd",\n    "type": "string",\n    "nullable": true,\n    "description": "번호이동전사업자통합코드명",\n    "valid_values": [\n      {\n        "value": "유니컴즈LG",\n        "desc": "LG의 네트워크를 이용하는 MVNO(가상 이동망 운영자)로, 유니컴즈가 제공하는 서비스입니다."\n      },\n      {\n        "value": "SK텔링크(재판매)",\n        "desc": "SK텔레콤의 자회사 SK텔링크에서 제공하는 MVNO 서비스로, 기존 네트워크를 재판매하는 형태입니다."\n      },\n      {\n        "value": "",\n        "desc": "회선을 사용 중인 고객의 번호이동 전 통신 사업자의 정보를 알 수 없음"\n      },\n      {\n        "value": "(주)조이텔",\n        "desc": "조이텔은 MVNO로서 다른 대형 통신사의 망을 임대하여 서비스하며, 별정사업자로 지정된 사업자입니다."\n      },\n      {\n        "value": "(주)미디어로그",\n        "desc": "미디어로그는 MVNO로서 다른 통신사의 네트워크를 이용해 이동통신 서비스를 제공합니다."\n      },\n      {\n        "value": "KT",\n        "desc": "대한민국 주요 이동통신사 중 하나로, 자체 네트워크를 통해 번호이동 및 통신 서비스를 제공합니다."\n      },\n      {\n        "value": "유니컴즈",\n        "desc": "유니컴즈의 MVNO 서비스로, 다른 주요 통신사의 네트워크를 사용하여 운영됩니다."\n      },\n      {\n        "value": "이지모바일LG",\n        "desc": "LG 네트워크를 활용하는 이지모바일의 MVNO 서비스입니다."\n      },\n      {\n        "value": "LG유플러스",\n        "desc": "LG유플러스는 전국적인 이동통신 네트워크를 자체적으로 운영하는 주요 통신사업자입니다."\n      },\n      {\n        "value": "SKBroadband (L)",\n        "desc": "SK브로드밴드의 일부 서비스로, (L)은 특정 기술 또는 서비스 유형을 나타냅니다."\n      },\n      {\n        "value": "(주)미니게이트",\n        "desc": "포괄적인 이동통신 서비스를 MVNO 모델로 제공하는 사업자입니다."\n      },\n      {\n        "value": "친구아이앤씨LG",\n        "desc": "LG망을 사용하는 친구아이앤씨의 MVNO 이동통신 서비스입니다."\n      },\n      {\n        "value": "SKBroadband (V)",\n        "desc": "SK브로드밴드의 VoIP 기반 인터넷 및 이동통신 서비스입니다."\n      },\n      {\n        "value": "아이즈비전SKT",\n        "desc": "SK텔레콤의 네트워크를 기반으로 운영되는 아이즈비전의 MVNO 서비스입니다."\n      },\n      {\n        "value": "케이티엠모바일",\n        "desc": "KT의 네트워크를 이용해 이동통신 서비스를 제공하는 KT 엠모바일입니다."\n      },\n      {\n        "value": "케이티스카이라이프",\n        "desc": "KT망을 활용하여 위성 방송 및 인터넷 서비스를 제공하는 케이티스카이라이프입니다."\n      },\n      {\n        "value": "LG데이콤 (V)",\n        "desc": "LG데이콤의 VoIP 기반 이동통신 서비스입니다."\n      },\n      {\n        "value": "KT인터넷전화 (V)",\n        "desc": "KT에서 제공하는 VoIP 기반 인터넷 전화 서비스입니다."\n      },\n      {\n        "value": "(주)고고팩토리",\n        "desc": "다양한 MVNO 이동통신 서비스를 제공하는 사업자입니다."\n      },\n      {\n        "value": "프리텔레콤SKT",\n        "desc": "SK텔레콤 네트워크 기반으로 운영되는 프리텔레콤의 MVNO 서비스입니다."\n      },\n      {\n        "value": "KPMOLG",\n        "desc": "LG 네트워크를 활용해 이동통신 서비스를 제공하는 KPMO입니다."\n      },\n      {\n        "value": "KCT (V)",\n        "desc": "VoIP 기술을 기반으로 한 KCT 이동통신 서비스입니다."\n      },\n      {\n        "value": "앤텔레콤",\n        "desc": "다른 주요 통신사의 망을 임대하여 운영하는 MVNO 사업자입니다."\n      },\n      {\n        "value": "CJ헬로비전KT",\n        "desc": "KT망을 활용하여 CJ헬로비전이 제공하는 이동통신 서비스입니다."\n      },\n      {\n        "value": "KT (L)",\n        "desc": "KT의 특정 기술 또는 서비스 유형을 가진 이동통신 서비스입니다."\n      },\n      {\n        "value": "㈜유니컴즈",\n        "desc": "다양한 통신망을 임대해 MVNO로 운영하는 유니컴즈의 서비스입니다."\n      },\n      {\n        "value": "SK텔레콤",\n        "desc": "SK텔레콤은 자체적으로 전국적인 이동통신 네트워크를 운영하는 주요 통신 사업자입니다."\n      }\n    ]\n  },\n  {\n    "name": "svc_rl_use_day_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "서비스 실사용일수, 가능한 값 : 0~999999"\n  },\n  {\n    "name": "hndset_rmnd_insl_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 잔여할부 개월수(0~37)"\n  },\n  {\n    "name": "hndset_rmnd_insl_amt",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 잔여할부 금액(0: 할부금없음)"\n  },\n  {\n    "name": "otcom_mbl_use_hndset_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "타사 모바일 사용 단말기수(0:타사모바일없음)"\n  },\n  {\n    "name": "spnsr_dc_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "스폰서 할인유형명(N:스폰서없음)",\n    "valid_values": [\n      {\n        "value": "",\n        "desc": "홈 인터넷 전화 등 재판매유형에 속하지 않은 회선 정보"\n      },\n      {\n        "value": "요금할인(선택약정)",\n        "desc": "요금 할인을 제공하는 선택약정 방식으로, 고객이 특정 기간 동안 서비스 이용을 약정하면 요금을 할인받을 수 있는 형태입니다."\n      },\n      {\n        "value": "SIMPLE COURSE",\n        "desc": "간단하고 편리한 재판매 서비스 혹은 요금제를 강조하며, 접근성과 사용법이 단순하여 고객의 편의를 높이는 방식입니다."\n      }\n    ]\n  },\n  {\n    "name": "rsal_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "재판매 유형명(순수판매:KT, 그외:별정사업자명)"\n  },\n  {\n    "name": "vipchc_yrl_rmnd_tmscnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "VIP초이스 년간 잔여횟수(년간 최대:12회)"\n  },\n  {\n    "name": "vipchc_tmon_use_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "VIP초이스 당월 사용여부(Y:사용, N:미사용)"\n  },\n  {\n    "name": "tvng_acc_actva_derv_tgt_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "티빙계정 활성화 유도대상여부(Y:사용, N:미사용)"\n  }\n],\n"relations": [\n  {\n    "target_table": "bidw_camp_cont_txn",\n    "join_type": "inner",\n    "join_spec": "abc_cont.svc_cont_id = abc_camp_cont.svc_cont_id",\n    "description": "서비스계약아이디를 기준으로 bidw_camp_cont_txn 테이블과 조인"\n  },\n  {\n    "target_table": "rtd_cust",\n    "join_type": "inner",\n    "join_spec": "abc_cont.src_cust_sorc_id = rtd_cust.src_cust_sorc_id",\n    "description": "원천고객소스아이디 기준으로 rtd_cust 테이블과 조인"\n  }\n]}',
          synonyms: ["캠페인 수행을 위한 고객 동의여부 테이블", "캠페인 수행을 위한 부수적인 회선 정보 테이블", "캠페인 수행을 위한 요금제 테이블", "캠페인 수행을 위한 상품 테이블" ],
          created_at: '2024-01-15T10:30:00Z',
          updated_at: '2024-01-20T15:45:00Z'
        },
        {
          id: 2,
          name: 'bidw_camp_cont_txn',
          description: '캠페인 수행을 위한 동의여부 및 부수적인 회선 정보 테이블',
          definition: '{\n"table_name": "bidw_camp_cont_txn",\n"description": "캠페인 수행을 위한 동의여부 및 부수적인 회선 정보 테이블",\n"columns": [\n  {\n    "name": "svc_cont_id",\n    "type": "string",\n    "nullable": false,\n    "description": "서비스 계약 아이디"\n  },\n  {\n    "name": "src_cust_sorc_id",\n    "type": "string",\n    "nullable": true,\n    "description": "원천 고객 소스 아이디"\n  },\n  {\n    "name": "dm_kt_ntf_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "DMKT 공지 거부 여부. 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "dm_kt_pr_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "DMKT 홍보 거부 여부. 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "indv_info_colec_use_agree_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "[01]개인정보 수집 사용 동의 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "indv_info_handl_csgn_agree_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "[04]개인정보 취급 위탁 동의 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "iifhlc_info_advm_rcv_agree_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "[30]개인정보 취급 위탁 정보 광고 수신 동의 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "msg_kt_ntf_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "메시지 KT공지 거부 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "msg_kt_advm_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "메시지 KT광고 거부 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "msg_kt_cprt_advm_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "메시지 KT제휴광고 거부 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "hsmvn_cont_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "이사 계약 여부, 가능한 값 : [Y=계약, N=미계약]"\n  },\n  {\n    "name": "losht_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "장단기 여부, 가능한 값 : [Y=장기, N=단기]"\n  },\n  {\n    "name": "tm_kt_ntf_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "TMKT 공지 거부 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "tm_kt_pr_rfsl_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "TMKT 광고 거부 여부, 가능한 값 : [Y=동의, N=미동의]"\n  },\n  {\n    "name": "oagncy_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "개통 관리 대리점명"\n  },\n  {\n    "name": "comb_svc_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "결합 서비스명",\n    "valid_values": [\n      {\n        "value": "인터넷+tv+모바일",\n        "desc": "인터넷과 TV, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+일반전화",\n        "desc": "인터넷, TV, 일반전화를 포함한 결합 서비스입니다."\n      },\n      { "value": "", "desc": "." },\n      {\n        "value": "모바일+모바일",\n        "desc": "모바일 서비스 두 개를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+일반전화+인터넷전화+모바일",\n        "desc": "인터넷, TV, 일반전화, 인터넷전화, 모바일 서비스를 모두 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+인터넷전화+모바일",\n        "desc": "인터넷, TV, 인터넷전화, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+일반전화+인터넷전화+모바일",\n        "desc": "인터넷, 일반전화, 인터넷전화, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+인터넷전화",\n        "desc": "인터넷, TV, 인터넷전화 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+인터넷전화+모바일",\n        "desc": "인터넷, 인터넷전화, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+모바일",\n        "desc": "인터넷과 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "일반전화+인터넷전화",\n        "desc": "일반전화와 인터넷전화를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+일반전화+인터넷전화",\n        "desc": "인터넷, TV, 일반전화, 인터넷전화 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+인터넷전화",\n        "desc": "인터넷과 인터넷전화를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+일반전화",\n        "desc": "인터넷과 일반전화를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+일반전화+GiGAeyes",\n        "desc": "인터넷, 일반전화, GiGAeyes 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+일반전화+모바일",\n        "desc": "인터넷, 일반전화, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv+일반전화+모바일",\n        "desc": "인터넷, TV, 일반전화, 모바일 서비스를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+일반전화+인터넷전화",\n        "desc": "인터넷, 일반전화, 인터넷전화를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+tv",\n        "desc": "인터넷과 TV를 포함하는 결합 서비스입니다."\n      },\n      {\n        "value": "인터넷+TV+인터넷전화+GiGAeyes",\n        "desc": "인터넷, TV, 인터넷전화, GiGAeyes 서비스를 포함하는 결합 서비스입니다."\n      }\n    ]\n  },\n  {\n    "name": "comb_shap_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "결합 형태명. 가능한 값: [3개결합(TPS), 4개결합(QPS), 2개결합(DPS), 5개결합, None]"\n  },\n  {\n    "name": "comb_svc_st_date",\n    "type": "string",\n    "nullable": true,\n    "description": "결합 서비스 시작 일자, 값 형식 : YYYYMMDD)"\n  },\n  {\n    "name": "comb_svc_fns_pam_date",\n    "type": "string",\n    "nullable": true,\n    "description": "결합 서비스 종료 예정 일자, 값 형식 : YYYYMMDD"\n  },\n  {\n    "name": "comb_dc_type_itg_cd",\n    "type": "string",\n    "nullable": true,\n    "description": "결합 할인 유형 통합명, 가능한 값 : [None, (결합유형)구)기본료할인형:약정별 결합할인(이동 기본료, 가족통화) 제공, (결합유형)뭉치면 올레:1년약정 이상시 결합할인(이동 기본료) 제공, 으랏차차 패키지 결합, 우리가족 무선할인, (결합유형)가족할인형:1년약정 이상시 결합할인(이동 기본료, 가족통화) 제공, 따로 살아도 가족결합, 알뜰폰 결합, 친구사이 무선결합, 신)인터넷뭉치면 올레]"\n  },\n  {\n    "name": "bprod_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "기본 상품명(요금제 상품명)"\n  },\n  {\n    "name": "bprod_group_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "기본 상품 그룹명(LOB). 가능한 값 : [Internet, Mobile, PSTN, IPTV, SOIP]"\n  },\n  {\n    "name": "bfee_amt",\n    "type": "integer",\n    "nullable": true,\n    "description": "기본료 금액"\n  },\n  {\n    "name": "bprod_mctg_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "기본 상품 중 분류명",\n    "valid_values": [\n      {\n        "value": "(5G)정액형",\n        "desc": "5G 네트워크를 이용한 정액형 요금제 상품"\n      },\n      { "value": "이너텔", "desc": "이너텔 서비스 관련 상품" },\n      {\n        "value": "(LTE)태블릿/스마트기기",\n        "desc": "LTE 네트워크를 이용하는 태블릿과 스마트기기에 대한 상품"\n      },\n      {\n        "value": "기타(신규/미정의)",\n        "desc": "신규 또는 미정의된 기타 상품"\n      },\n      { "value": "인터넷 Premium", "desc": "인터넷 Premium 상품" },\n      {\n        "value": "(LTE)청소년/노인/장애인/군인",\n        "desc": "LTE 네트워크를 이용하는 청소년, 노인, 장애인, 군인을 위한 상품"\n      },\n      { "value": "인터넷 Ntopia", "desc": "인터넷 Ntopia 상품" },\n      {\n        "value": "(5G)MVNO/별정",\n        "desc": "5G 네트워크를 이용하는 MVNO/별정 통신 서비스 상품"\n      },\n      { "value": "(LTE)정액형", "desc": "LTE 네트워크 기반의 정액형 상품" },\n      { "value": "인터넷 Lite", "desc": "인터넷 Lite 상품" },\n      {\n        "value": "올레 기가 인터넷",\n        "desc": "올레 기가 인터넷 서비스 상품"\n      },\n      { "value": "SoIP서비스", "desc": "SoIP(인터넷 전화) 서비스 상품" },\n      { "value": "일반전화", "desc": "일반전화 서비스 상품" },\n      {\n        "value": "타지역서비스",\n        "desc": "특정 지역을 대상으로 하는 타지역 서비스"\n      },\n      {\n        "value": "(5G)청소년/노인/장애인/군인",\n        "desc": "5G 네트워크를 이용하는 청소년, 노인, 장애인, 군인을 위한 상품"\n      },\n      {\n        "value": "(LTE)MVNO/별정",\n        "desc": "LTE 네트워크를 이용하는 MVNO/별정 통신 서비스 상품"\n      }\n    ]\n  },\n  {\n    "name": "hndset_model_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "단말기 모델명",\n    "valid_values": [\n      {\n        "value": "OPENMODEL2",\n        "desc": "계약정보가 모바일인 경우 단말기정보 (SM - 삼성단말기, API-아이폰, …기타등등). 인터넷/IPTV 인 경우에는 접속단말, 모뎀"\n      },\n      {\n        "value": "SM-N981NG",\n        "desc": "삼성 단말기 모델명인 SM-N981NG입니다."\n      },\n      {\n        "value": "SM-F721NK512",\n        "desc": "삼성의 폴더블 단말기 모델명인 SM-F721NK512입니다."\n      },\n      {\n        "value": "AIP16-256",\n        "desc": "아이폰 모델명 AIP16-256으로, 특정 저장 용량을 지닌 아이폰 모델입니다."\n      },\n      {\n        "value": "SM-S928NSO",\n        "desc": "삼성 단말기 모델명인 SM-S928NSO입니다."\n      },\n      {\n        "value": "SM-S926NSOG",\n        "desc": "삼성 단말기 모델명인 SM-S926NSOG로, 특정 지역 또는 기능에 따라 차별화된 모델입니다."\n      },\n      {\n        "value": "DMR_MA4100",\n        "desc": "DMR_MA4100은 IPTV나 인터넷 모뎀 및 접속 단말을 가리킵니다."\n      },\n      {\n        "value": "SM-A155N-TAC",\n        "desc": "삼성 단말기 모델명 SM-A155N-TAC입니다."\n      },\n      {\n        "value": "APT_AT203-308W",\n        "desc": "APT_AT203-308W는 특정 인터넷이나 IPTV 접속 장비의 모델명을 나타냅니다."\n      },\n      {\n        "value": "SM-A245NK",\n        "desc": "삼성 단말기 모델명 SM-A245NK입니다."\n      },\n      {\n        "value": "KAO_KI1101_어반그레이",\n        "desc": "KAO_KI1101_어반그레이는 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      {\n        "value": "APT_AT05-704V",\n        "desc": "APT_AT05-704V는 특정 IPTV나 인터넷 서비스에 필요한 단말기 모델입니다."\n      },\n      {\n        "value": "SM-G781NK",\n        "desc": "삼성 단말기 모델명 SM-G781NK입니다."\n      },\n      {\n        "value": "SM-F741NK",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F741NK입니다."\n      },\n      {\n        "value": "NA1100",\n        "desc": "NA1100은 특정 IPTV나 인터넷 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "모뎀(에센스/베이직용)",\n        "desc": "모뎀(에센스/베이직용)은 특정 서비스 수준에 맞게 제공되는 모뎀 모델입니다."\n      },\n      {\n        "value": "SM-S928NG",\n        "desc": "삼성 단말기 모델명 SM-S928NG입니다."\n      },\n      {\n        "value": "SM-S721NK",\n        "desc": "삼성 단말기 모델명 SM-S721NK입니다."\n      },\n      {\n        "value": "SM-F936N",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F936N입니다."\n      },\n      {\n        "value": "KFT_EV202-003D",\n        "desc": "KFT_EV202-003D는 특정 인터넷 또는 IPTV 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "MMM_MS01-706V",\n        "desc": "MMM_MS01-706V는 특정 IPTV 또는 인터넷 장비에 필요한 모델명입니다."\n      },\n      {\n        "value": "SM-F711N",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F711N입니다."\n      },\n      {\n        "value": "LGN_LN202-003D",\n        "desc": "LG의 네트워크/단말기 모델명 LGN_LN202-003D입니다."\n      },\n      {\n        "value": "AIP16PS-TAC",\n        "desc": "아이폰 모델명 AIP16PS-TAC입니다."\n      },\n      {\n        "value": "AIP13PM-TAC",\n        "desc": "아이폰 모델명 AIP13PM-TAC입니다."\n      },\n      { "value": "SM-S921N", "desc": "삼성 단말기 모델명 SM-S921N입니다." },\n      {\n        "value": "SM-S928NK",\n        "desc": "삼성 단말기 모델명 SM-S928NK입니다."\n      },\n      {\n        "value": "IPHONE_13_MINI_128GW",\n        "desc": "아이폰 모델명 IPHONE_13_MINI_128GW로, 특정 저장 용량을 지닌 모델입니다."\n      },\n      { "value": "A2628-128", "desc": "아이폰 모델명 A2628-128입니다." },\n      {\n        "value": "WiFi 임대장비(고속AP)",\n        "desc": "WiFi 임대장비(고속AP)는 고속 인터넷 접속을 지원하는 WiFi 장비입니다."\n      },\n      {\n        "value": "OPENMODEL4",\n        "desc": "OPENMODEL4는 특정 단말기 정보의 유형으로서, 다양한 장치에 적용됩니다."\n      },\n      { "value": "AIP15P-TAC", "desc": "아이폰 모델명 AIP15P-TAC입니다." },\n      { "value": "AT-M120S", "desc": "단말기 모델 AT-M120S입니다." },\n      {\n        "value": "SM-A235NSO",\n        "desc": "삼성 단말기 모델명 SM-A235NSO입니다."\n      },\n      {\n        "value": "AIPSE2-TAC2",\n        "desc": "아이폰 모델명 AIPSE2-TAC2입니다."\n      },\n      {\n        "value": "AIP16PM-TAC",\n        "desc": "아이폰 모델명 AIP16PM-TAC입니다."\n      },\n      {\n        "value": "APT_AT204-505D",\n        "desc": "APT_AT204-505D는 특정 인터넷 또는 IPTV 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "KAO_NA2200",\n        "desc": "KAO_NA2200은 특정 접속 장비의 모델명을 나타냅니다."\n      },\n      {\n        "value": "SM-F936NE",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F936NE입니다."\n      },\n      { "value": "AIP14-TAC", "desc": "아이폰 모델명 AIP14-TAC입니다." },\n      { "value": "", "desc": "결합 회선으로 단말기 모델명이 미등록" },\n      { "value": "AIP16-128", "desc": "아이폰 모델명 AIP16-128입니다." },\n      {\n        "value": "SM-S926NSOY",\n        "desc": "삼성 단말기 모델명 SM-S926NSOY입니다."\n      },\n      {\n        "value": "APT_AT201-008W",\n        "desc": "APT_AT201-008W는 특정 인터넷 또는 IPTV 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "SM-A165NK",\n        "desc": "삼성 단말기 모델명 SM-A165NK입니다."\n      },\n      {\n        "value": "SM-S911NG",\n        "desc": "삼성 단말기 모델명 SM-S911NG입니다."\n      },\n      {\n        "value": "SM-F731NM",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F731NM입니다."\n      },\n      { "value": "AIP16P-256", "desc": "아이폰 모델명 AIP16P-256입니다." },\n      { "value": "SM-M366K", "desc": "삼성 단말기 모델명 SM-M366K입니다." },\n      { "value": "AIP16P-TAC", "desc": "아이폰 모델명 AIP16P-TAC입니다." },\n      {\n        "value": "SM-A256N00",\n        "desc": "삼성 단말기 모델명 SM-A256N00입니다."\n      },\n      {\n        "value": "MMM_IP-570H_Biz",\n        "desc": "MMM_IP-570H_Biz는 특정 IPTV 또는 인터넷 장비에 필요한 모델명입니다."\n      },\n      {\n        "value": "(패키지용)와이파이_GiGA WiFi home",\n        "desc": "(패키지용)와이파이_GiGA WiFi home은 특정 패키지 서비스에 포함된 와이파이 장비입니다."\n      },\n      {\n        "value": "SM-N986NK",\n        "desc": "삼성 단말기 모델명 SM-N986NK입니다."\n      },\n      { "value": "IP14_512GP", "desc": "아이폰 모델명 IP14_512GP입니다." },\n      {\n        "value": "AIP12PM-TAC",\n        "desc": "아이폰 모델명 AIP12PM-TAC입니다."\n      },\n      {\n        "value": "GiGA WiFi home",\n        "desc": "GiGA WiFi home은 특정 IPTV 또는 인터넷 서비스에 필요한 와이파이 장비입니다."\n      },\n      {\n        "value": "PTA-VOLTE_20221H",\n        "desc": "PTA-VOLTE_20221H는 특정 VoLTE 서비스에 필요한 장비의 모델명입니다."\n      },\n      {\n        "value": "SM-F731NL",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F731NL입니다."\n      },\n      {\n        "value": "IPHONE_12_PRO_256GBL",\n        "desc": "아이폰 모델명 IPHONE_12_PRO_256GBL입니다."\n      },\n      {\n        "value": "APT_AT203-003D",\n        "desc": "APT_AT203-003D는 특정 인터넷 또는 IPTV 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "MAU4800D_LW_릴리화이트",\n        "desc": "MAU4800D_LW_릴리화이트는 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      {\n        "value": "xDSL 모뎀",\n        "desc": "xDSL 모뎀은 특정 DSL 인터넷 서비스에 필요한 모뎀 모델명입니다."\n      },\n      {\n        "value": "SM-A235NB",\n        "desc": "삼성 단말기 모델명 SM-A235NB입니다."\n      },\n      {\n        "value": "SM-S937NK",\n        "desc": "삼성 단말기 모델명 SM-S937NK입니다."\n      },\n      { "value": "AIP13-128", "desc": "아이폰 모델명 AIP13-128입니다." },\n      { "value": "AIP15-TAC", "desc": "아이폰 모델명 AIP15-TAC입니다." },\n      {\n        "value": "SM-A102N-KF4",\n        "desc": "삼성 단말기 모델명 SM-A102N-KF4입니다."\n      },\n      {\n        "value": "SM-S931NK",\n        "desc": "삼성 단말기 모델명 SM-S931NK입니다."\n      },\n      {\n        "value": "SM-S926NV",\n        "desc": "삼성 단말기 모델명 SM-S926NV입니다."\n      },\n      {\n        "value": "SM-S931N512-00",\n        "desc": "삼성 단말기 모델명 SM-S931N512-00입니다."\n      },\n      { "value": "AIP11-TAC", "desc": "아이폰 모델명 AIP11-TAC입니다." },\n      {\n        "value": "UDC_UD201-012W",\n        "desc": "UDC_UD201-012W는 특정 접속 장비의 모델명을 나타냅니다."\n      },\n      { "value": "A2890-128", "desc": "아이폰 모델명 A2890-128입니다." },\n      {\n        "value": "KAO_KSTB6188",\n        "desc": "KAO_KSTB6188은 특정 IPTV 접속 장비의 모델명을 나타냅니다."\n      },\n      {\n        "value": "AP 홈허브 스페셜",\n        "desc": "AP 홈허브 스페셜은 특정 서비스에 필요한 홈허브 장비의 모델명입니다."\n      },\n      { "value": "SM-S926N", "desc": "삼성 단말기 모델명 SM-S926N입니다." },\n      {\n        "value": "LGN_LN202-007W",\n        "desc": "LG의 네트워크/단말기 모델명 LGN_LN202-007W입니다."\n      },\n      {\n        "value": "olleh WiFi home",\n        "desc": "olleh WiFi home은 특정 IPTV 또는 인터넷 서비스에 필요한 와이파이 장비입니다."\n      },\n      {\n        "value": "IPADM6-TAC",\n        "desc": "아이패드 모델명 IPADM6-TAC입니다."\n      },\n      {\n        "value": "KAO_KI1100_LG_어반그레이",\n        "desc": "KAO_KI1100_LG_어반그레이는 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      {\n        "value": "SM-A165N-TAC",\n        "desc": "삼성 단말기 모델명 SM-A165N-TAC입니다."\n      },\n      {\n        "value": "SM-S921NY",\n        "desc": "삼성 단말기 모델명 SM-S921NY입니다."\n      },\n      {\n        "value": "IP16P_512GS",\n        "desc": "아이폰 모델명 IP16P_512GS입니다."\n      },\n      { "value": "SM-A716S", "desc": "삼성 단말기 모델명 SM-A716S입니다." },\n      {\n        "value": "DMR_MA4000",\n        "desc": "DMR_MA4000은 특정 IPTV나 인터넷 모뎀 및 접속 단말을 가리킵니다."\n      },\n      {\n        "value": "KAO_KG3100_샌드그레이",\n        "desc": "KAO_KG3100_샌드그레이는 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      { "value": "A2403-128", "desc": "아이폰 모델명 A2403-128입니다." },\n      {\n        "value": "IPHONE_12_PRO_128GBL",\n        "desc": "아이폰 모델명 IPHONE_12_PRO_128GBL입니다."\n      },\n      {\n        "value": "IPHONE_13_128GBL",\n        "desc": "아이폰 모델명 IPHONE_13_128GBL입니다."\n      },\n      {\n        "value": "SM-S711NSOW",\n        "desc": "삼성 단말기 모델명 SM-S711NSOW입니다."\n      },\n      {\n        "value": "DMR_MAR4510C_샌드그레이",\n        "desc": "DMR_MAR4510C_샌드그레이는 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      { "value": "SM-A205S", "desc": "삼성 단말기 모델명 SM-A205S입니다." },\n      {\n        "value": "AIP16PE2-TAC",\n        "desc": "아이폰 모델명 AIP16PE2-TAC입니다."\n      },\n      {\n        "value": "PTA-VOLTE-PC",\n        "desc": "PTA-VOLTE-PC는 특정 VoLTE 서비스에 필요한 장비의 모델명입니다."\n      },\n      {\n        "value": "KFT_EV202-005W",\n        "desc": "KFT_EV202-005W는 특정 IPTV나 인터넷 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "SSE_SS204-003D",\n        "desc": "SSE_SS204-003D는 특정 IPTV나 인터넷 접속 장비의 모델명입니다."\n      },\n      {\n        "value": "SM-S938NK",\n        "desc": "삼성 단말기 모델명 SM-S938NK입니다."\n      },\n      {\n        "value": "PTA-DS-5G",\n        "desc": "PTA-DS-5G는 특정 5G 서비스에 필요한 장비의 모델명입니다."\n      },\n      {\n        "value": "AP 홈허브",\n        "desc": "AP 홈허브는 특정 서비스에 필요한 홈허브 장비의 모델명입니다."\n      },\n      { "value": "AIP15-R128", "desc": "아이폰 모델명 AIP15-R128입니다." },\n      {\n        "value": "SM-S926NY",\n        "desc": "삼성 단말기 모델명 SM-S926NY입니다."\n      },\n      {\n        "value": "SM-A315NSOW",\n        "desc": "삼성 단말기 모델명 SM-A315NSOW입니다."\n      },\n      {\n        "value": "SM-S936NK512",\n        "desc": "삼성 단말기 모델명 SM-S936NK512입니다."\n      },\n      {\n        "value": "SM-F711N-00",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F711N-00입니다."\n      },\n      {\n        "value": "RNC_RC102-811DW",\n        "desc": "RNC_RC102-811DW는 특정 접속 장비의 모델명을 나타냅니다."\n      },\n      {\n        "value": "MAU4800D_NG_네이처그린",\n        "desc": "MAU4800D_NG_네이처그린은 특정 색상으로 제공되는 단말기 또는 모뎀 장비입니다."\n      },\n      {\n        "value": "IP공유기",\n        "desc": "IP공유기는 인터넷 네트워크를 여러 장치에 공유할 수 있는 장비입니다."\n      },\n      {\n        "value": "SM-F731NM_512G",\n        "desc": "삼성의 폴더블 단말기 모델명 SM-F731NM_512G입니다."\n      },\n      {\n        "value": "SM-S921N-00",\n        "desc": "삼성 단말기 모델명 SM-S921N-00입니다."\n      }\n    ]\n  },\n  {\n    "name": "hndset_model_div_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "단말기 모델 구분명. 가능한 값 : [None, 스마트폰, 패드]"\n  },\n  {\n    "name": "mkng_yy",\n    "type": "string",\n    "nullable": true,\n    "description": "제조년도(YYYY)"\n  },\n  {\n    "name": "hndset_rmnd_insl_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 잔여 할부 개월 수. 가능한 값: 1~37"\n  },\n  {\n    "name": "hndset_rmnd_insl_amt",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 잔여 할부 금액"\n  },\n  {\n    "name": "hndset_tot_insl_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 총 할부 개월수. 가능한 값: 1~37"\n  },\n  {\n    "name": "hndset_tot_insl_amt",\n    "type": "integer",\n    "nullable": true,\n    "description": "단말기 총 할부금액"\n  },\n  {\n    "name": "makr_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "제조사명. 가능한 값 : [None, 주식회사 에이엘티, LG-Ericsson(엘지에릭슨), 전파연구소, APPLE(애플), (주)아프로텍, 유니데이타커뮤니케이션, (주)모임스톤, KTFT 케이티에프테크놀로지스, 삼성전자(주), ㈜아이리버 (구, 레인콤)]"\n  },\n  {\n    "name": "now_hndset_use_day_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "현 단말기 사용 일수"\n  },\n  {\n    "name": "use_purp_div_itg_cd",\n    "type": "string",\n    "nullable": true,\n    "description": "사용용도 구분 통합 코드. 가능한 값 : [주택용, 일반, 선불, 업무용]"\n  },\n  {\n    "name": "broad_sido_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "광역시도명. 가능한 값 : [None, 충남, 부산, 울산, 세종, 인천, 대구, 대전, 서울, 충북, 경남, 경기, 경북, 강원, 제주, 전북, 광주, 전남]"\n  },\n  {\n    "name": "sgg_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "시군구명. 가능한 값 : [None, 부천시 원미구, 나주시, 아산시, 서구, 달서구, 영덕군, 의령군, 김해시, 기장군, 수원시 장안구, 여수시, 횡성군, 부평구, 당진시, 장흥군, 양평군, 문경시, 울진군, 대덕구, 광주시, 구로구, 사하구, 성남시 분당구, 순천시, 보령시, 강화군, 진주시, 김제시, 창원시 진해구, 수원시 팔달구, 포천시, 의성군, 옥천군, 용인시 기흥구, 부천시 소사구, 안산시 상록구, 용인시 처인구, 파주시, 창원시 성산구, 수영구, 광산구, 강서구, 무안군, 정선군, 김천시, 광양시, 고흥군, 송파구, 북구, 포항시 남구, 성북구, 원주시, 연제구, 포항시 북구, 연천군, 경주시, 광명시, 영천시, 동두천시, 남동구, 유성구, 중랑구, 영암군, 김포시, 청원군, 남양주시, 동래구, 남원시, 중구, 구리시, 양주시, 안양시 동안구, 강동구, 산청군, 함평군, 춘천시, 남제주군, 군위군, 시흥시, 홍성군, 영등포구, 화성시, 울주군, 고성군, 관악구, 사상구, 오산시, 장성군, 금천구, 용산구, 의정부시, 부여군, 상주시, 마포구, 달성군, 남구, 동작구, 영주시, 수원시 권선구, 청양군, 동구, 청송군, 평창군, 목포시, 해운대구, 군산시, 수원시 영통구, 노원구, 양양군, 청주시 상당구, 거제시, 평택시, 서산시, 가평군, 양천구, 강진군, 서귀포시, 거창군, 영동군, 동대문구, 경산시, 칠곡군, 제주시, 전주시 완산구, 익산시, 여주군, 창원시 마산합포구, 괴산군, 제천시, 청주시 흥덕구, 서대문구, 부안군, 부산진구, 용인시 수지구, 서천군, 강남구, 용인시, 안동시, 이천시, 충주시, 고양시 덕양구, 수성구, 종로구, 속초시, 강릉시, 성남시 중원구, 청주시 서원구, 서초구, 성남시 수정구, 하남시, 안성시, 함안군, 예천군, 전주시 덕진구, 안산시 단원구, 광진구, 고양시 일산동구, 홍천군, 양산시]"\n  },\n  {\n    "name": "acpt_org_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "수용조직명. 가능한 값 : [용인지사(CS부), 언양지점, 연수지점, 해운대지점, 퇴계원국사, 남원지점(제주서귀포), 서초지점, 항동지점, 당진지점, 용전지점, 서대구지사(CS부), 순천지사(CS부), 서청주국사, 천안지사(CS부), 서울산국사, 보령지점, 서부산지사(CS부), 동광주국사, 경주지점, 영통국사, 여수지점, 청주지사(CS부), 춘천지사(CS부), 중부산지사, 인천지사(CS부), 경산지점, 공주지점, 동작국사, 구로지사(CS부), 정읍지점, 송파지사(CS부), 강화지사, 팔복국사, 모란국사, 남광주지점, 평창지점, 수완지점, 송도국사, 중동국사, 영주지점, 경북동부지사(CS부), 북울산지점, 남전주국사, 광안지점, 동수원국사, 동촌국사, 고양지사(CS부), 청송지점, 구리지사(CS부), 동래지점, 김포지점, 충북영동지사, 구포지점, 반포국사, 김해지점, 청량국사, 김제지점, 금천지점, 서광주지사(CS부), 서수원국사, 양산지점, 동군산지점, 부평지점, 광명지점, 북포항국사, 주안국사, 가야국사, 부여지점, 진영국사, 동부천국사, 일산국사, 가락국사, 만수국사, 북대구국사, 목동지점, 장림국사, 여수국사, 영월지사, 파주지점, 함창분실, 시화국사, 옥천지점, 강남지사(CS부), 서산지점, 울진지점, 안성지점, 하남지점, 일광지점, 울산지사(CS부), 강동국사, 노원지사(CS부), 칠곡지점, 상동국사, 청평지점, 신당국사, 장흥지사, 수원지사(CS부), 영등포지점, 동진주국사, 장성지점, 의령지사, 안심지점, 무안지사, 연천국사, 울산성남국사, 서안동국사, 횡성지사, 신촌국사, 함열지점, 서문경분실, 서천지사, 이천지점, 송탄국사, 중랑지점, 오산지점, 부송지점, 덕양국사, 중대구지점, 서면지점, 남부산지사(CS부), 영광지사, 가경국사, 신제주지점, 도봉지점, 양평지점, 함평지점, 분당지사(CS부), 수내국사, 문경지점, 서귀포지점, 평택지사(CS부), 조암지점, 북대전지사, 고덕국사, 익산지사(CS부), 동울산지점, 서광양지점, 덕소지점, 남청주국사, 신사국사, 군포지점, 좌동지점, 제천지점, 동대전국사, 정선지사, 영천지점, 관악지점, 양재지점, 영덕지사, 청양지사, 강북지점, 사음지점, 충주지사(CS부), 송우국사, 서인천지사(CS부), 홍성지사(CS부), 강서지사(CS부), 동목포국사, 남울산지점, 달서지사(CS부), 유성지점, 제주지사(CS부), 가양국사, 경북북부지사(CS부), 고흥지사, 계양지점, 온수지점, 남춘천지점, 세종지점, 여주지점, 나주지점, 북전주지점, 계룡지사, 서대전지점, 화전자국, 남원지점, 안산지점, 하당국사, 동순천국사, 김천지점, 신갈국사, 북대전지점, 중앙지사(CS부), 본촌국사, 상주지점, 광화문지사(CS부), 아산지점, 수지국사, 성남국사, 숭의지점, 성북국사, 홍제국사, 경기광주지점, 동두천지점, 전농국사, 개봉지점, 능곡국사, 광진지사(CS부), 의정부지사(CS부), 속초지점, 수산분실, 중앙국사, 원주지사(CS부), 통영지점, 마산국사, 홍천지점, 서강릉지점, 부안지사, 후포분실, 군위지사, 동전주국사, 칠원분실, 수성지점, 부천지사(CS부), 양양지사, 북광주지사(CS부), 의성지사, 경기서부지사(CS부), 창원지사(CS부), 진해지점, 여의도국사, 광산국사, None]"\n  },\n  {\n    "name": "new_date",\n    "type": "string",\n    "nullable": true,\n    "description": "신규 일자, 값 형식 : YYYYMMDD"\n  },\n  {\n    "name": "sale_cpnt_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "판매 접점명. 가능한 값 =[None, KTS서부_구로_금천, 프리넷_방문_기술영업, KT플라자 강남점, 에어링크_UIT동시판매, KT샵_KTCS_MCRM, 세종대왕폰, KT플라자 제천점, 하이프라자_광산본점, 모요_셀프개통, 충주휴대폰성지 옆커폰 연수점, KTS대구_구미_상주, KT 다이렉트, 에스비엠 주식회사, 스마트통신 운암점, 하이넷_수원_유무선기술, (주)창조, (주)민국정보통신_동부산_현장영업, KTS충청_충남_유케이(성환), 기업무선_KT임직원(가족)판매실적, (주)더드림_월평점, 호강정보 상동2호점, 주식회사 탐나넷, KT플라자 원주점, 행운통신, 넷코리아, 휴대폰백화점, 쇼준텔레콤 대안1호점, MVNO_에넥스, KT플라자 여주점, KT플라자 노원점, KT플라자 관악점, KT플라자 청주점, KTS강북_광진_중랑, 와이즈텔레콤, 다경_광주치평점, KT플라자 서초점, 미운영_ITS 경남, KT플라자 동순천점, M&S모래내직영점, KT플라자 구로점, 엠ITT충남서부_현장영업, 주식회사 두웰, 아싸통신, 하람모바일 장안구청점, 에이투젯 휴대폰, 홍스통신 휴대폰할인매장, 얌앤꼬 모바일, 연지IMT, 휴대폰성지 옆커폰 신정점, (주)피앤에프 평촌광장점, (주)더리더스 수원역중앙점, 스마트넷_동부산_방문_기술영업, 더원컴퍼니 봉명점, 양평우체국, 북부)알뜰할인, 마이더스 정보통신_현장영업, 헤이폰, e-편한통신, (주)우리정보통신_유선UIT, M&S대천중앙로직영점, KTS호남_현장지원, 미운영_1010002555, KT플라자 남울산점, 엠존(응암), 무한_상남점, 국대아이티_현장영업, M&S서현역직영점, KT플라자 북광주점, (주)누리정보통신 학산사거리점, (주)모요, 케이티넷_방문_기술영업, 자비스모바일스토어가평점, (주)ITS북부 일산지점, (주)엘에스컴퍼니_부산대2호점, KT플라자 중부산점, 엔플_서라벌점, KT샵_제휴_카카오페이, 프리모바일, (주)와이에이_로데오중앙점, 주식회사오션모바일 3호점, 와디즈, 아미고_삼성중앙역점, M모바일(직영온라인), 삼성전자판매_디지털시티2모바일, 성우네트웍스_방문_기술영업, 건국 천천점, (주)텔나라네트웍_가경점, 상권영업_kt플라자 용인점, 청솔텔레콤, 솔트네트워크_양천구청점, 에스비트_신규_유무선, 비즈넷_방문_기술영업, 고객셀프개통, 삼성전자판매_순천, (주)JYT_송라시장점, 재재모바일, 이레시스템_유선온라인, 중원아이티, 빛고을 정보통신, 홈페이지(일반), 더폰, KT플라자 강북점, 숲통신_신규_유무선, 수(SU)_증산점, 주식회사 백메가 온라인접점, 아정통신, KTS강원_원주_CS3팀(원주), 주식회사 엑스파워정보통신, 휴대폰 쇼핑몰(영서통신), K프로_신익호_10070751_은하네트웍스, KTS호남_익산_김제, M&S동탄호수공원직영점, 삼성전자판매_서울RND캠퍼스 모바일, KT샵_KTIS_MCRM, (주)월드_태전점, (주)세이브텔레콤_동부산_현장영업, 휴대폰1번가, 딸기통신, 키움, KT플라자 남대구점, 연세컴퍼니_신정네거리역점, KT플라자 경주점, 그린텔레콤 송파점, 쇼미래텔 둔포점, 케이스타_분당_유무선기술, 케이티씨에스_정평역점, (주)누리정보통신 커넬워크점, (주)쎈정보통신_동시판매, 도다텔_고양소매 행신점, 엠제이(MJ), KT플라자 양재점, KT플라자 성남점, 오렌지_네이버, 모바일컴퍼니, M&S정관로직영점, M&S찾아가는영업, KT플라자 익산점, VIKOF MOBILE, KT플라자 은평점, KTS강남_강남_강남, 한울정보통신_삼호한마음점, KT플라자 사하점, 거제맘통신, 이마트_안성점, 모바일이지, (주)에이치티엠_강남_현장시연, 동원_노형점, 전자랜드_보령점, 재홍텔레콤(더블류점), KT플라자 아산점, M&S상무직영점, 토탈영업_개통접점, 미래통신, 케이커머스_평택_유무선기술, 모요, DSMC3팀, KT플라자 시화점, KT플라자 둔산점, KT플라자 혜화점, 모요(간편개통), KT플라자 남원점, 삼성전자판매_신세계 센텀시티, 미라클_사무실, (주)텔나라네트웍_칠금점, KTS강남_송파_고덕, KT플라자 강서점, 통판 SMC 대전 H, 소망, KT플라자 군위점, 친구모바일 홍대점, 주식회사 케이티스, 온라인_쎈정보, 진주지사_거창지점, 개통센터, KT플라자 동래점, KT플라자 강화점, M&S시지애드샵직영점, 삼성전자판매_스마트라운지세교점, KT플라자 보령점]"\n  },\n  {\n    "name": "mphon_ch_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "판매접점 이동전화 채널 유형명. 가능한 값 : [None, 도매, 소매, ,비정형]"\n  },\n  {\n    "name": "mphon_sale_path_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "판매접점 이동전화 판매 경로명",\n    "valid_values": [\n      { "value": "", "desc": "판매경로 미등록 회선" },\n      {\n        "value": "대형양판",\n        "desc": "대형양판을 통해 다양한 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "사무실",\n        "desc": "사무실 기반의 이동전화 판매 경로를 나타냅니다."\n      },\n      {\n        "value": "플라자",\n        "desc": "플라자 매장에서 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "Biz판매",\n        "desc": "기업 고객 대상의 Biz 판매 경로입니다."\n      },\n      {\n        "value": "특판",\n        "desc": "특별한 단체나 이벤트에서 이동전화를 파는 특판 경로입니다."\n      },\n      {\n        "value": "판매점",\n        "desc": "일반적인 이동전화 판매점에서의 판매 경로입니다."\n      },\n      {\n        "value": "비대면",\n        "desc": "비대면 방식으로 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "제휴",\n        "desc": "제휴를 통해 협력 업체와 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "빌딩",\n        "desc": "빌딩 내에서의 이동전화 판매 경로입니다."\n      },\n      {\n        "value": "특수유통(과거)",\n        "desc": "특수유통(과거)을 통해 다양한 방식으로 이동전화를 판매하던 경로입니다."\n      },\n      {\n        "value": "CRM",\n        "desc": "CRM(Customer Relationship Management)을 활용한 이동전화 판매 경로입니다."\n      },\n      {\n        "value": "대형마트",\n        "desc": "대형마트에서 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "기타",\n        "desc": "기타 여러 방식의 이동전화 판매 경로입니다."\n      },\n      {\n        "value": "개통",\n        "desc": "개통을 통해 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "홈쇼핑(과거)",\n        "desc": "홈쇼핑(과거)을 통해 이동전화를 판매하던 경로입니다."\n      },\n      {\n        "value": "올레홈",\n        "desc": "올레홈을 통해 다양한 방식을 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "온라인몰(오픈마켓)",\n        "desc": "온라인몰(오픈마켓)을 통해 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "동시판매",\n        "desc": "동시판매를 통해 여러 제품과 함께 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "아파트",\n        "desc": "아파트 단지 등 특정 주거지역 중심의 이동전화 판매 경로입니다."\n      },\n      {\n        "value": "KT프로",\n        "desc": "KT프로를 통해 전문적인 이동전화 판매를 지원하는 경로입니다."\n      },\n      {\n        "value": "Smart Agent",\n        "desc": "Smart Agent를 활용한 이동전화 판매 경로입니다."\n      },\n      {\n        "value": "현장영업",\n        "desc": "현장영업을 통해 직접 고객을 대상으로 이동전화를 판매하는 경로입니다."\n      },\n      {\n        "value": "전속매장",\n        "desc": "전속매장에서 특정 브랜드나 제품군의 이동전화를 판매하는 경로입니다."\n      }\n    ]\n  },\n  {\n    "name": "mphon_sale_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "판매접점 이동전화 판매 유형명",\n    "valid_values": [\n      { "value": "", "desc": "판매유형이 등록되지 않은 회선" },\n      { "value": "매장", "desc": "매장에서의 이동전화 판매 유형입니다." },\n      {\n        "value": "판매점",\n        "desc": "일반적인 판매점에서의 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "법인판매",\n        "desc": "법인을 대상으로 한 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "가판",\n        "desc": "가판을 통해 이동전화를 판매하는 유형입니다."\n      },\n      {\n        "value": "방문판매",\n        "desc": "방문판매를 통한 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "준직영채널",\n        "desc": "준직영 채널을 통한 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "대형유통",\n        "desc": "대형 유통망을 이용한 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "고객센터",\n        "desc": "고객센터를 통해 이동전화를 판매하는 유형입니다."\n      },\n      {\n        "value": "기타",\n        "desc": "기타 여러 방식을 통한 이동전화 판매 유형입니다."\n      },\n      {\n        "value": "비매장",\n        "desc": "비매장 방식으로 이동전화를 판매하는 유형입니다."\n      },\n      { "value": "MOT", "desc": "MOT를 통한 이동전화 판매 유형입니다." },\n      {\n        "value": "소매2",\n        "desc": "소매 형태로 이동전화를 판매하는 두 번째 유형입니다."\n      },\n      {\n        "value": "온라인",\n        "desc": "온라인으로 이동전화를 판매하는 유형입니다."\n      },\n      {\n        "value": "현장영업",\n        "desc": "현장을 방문하여 직접 이동전화를 판매하는 유형입니다."\n      }\n    ]\n  },\n  {\n    "name": "sale_plcy_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "판매 정책명",\n    "valid_values": [\n      { "value": "", "desc": "판매정책으로 개통하지 않은 회선" },\n      {\n        "value": "기본판매_USIM단독_후불",\n        "desc": "기본 판매 정책으로 USIM 단독 후불 결제 방식입니다."\n      },\n      {\n        "value": "3G 사업용",\n        "desc": "3G 네트워크를 이용한 사업용 판매 정책입니다."\n      },\n      {\n        "value": "기본판매_신규_현금",\n        "desc": "기본 판매 정책으로 신규 계약 시 현금 결제 방식입니다."\n      },\n      {\n        "value": "USIM 단독개통_선불",\n        "desc": "USIM 단독 개통으로 선불 결제 방식입니다."\n      },\n      {\n        "value": "[★] 인터넷전화 재약정(24개월)판매정책",\n        "desc": "인터넷전화의 24개월 재약정 판매 정책입니다."\n      },\n      {\n        "value": "13년~14년 인터넷전화 신규(24개월)",\n        "desc": "13년~14년 인터넷전화 신규 계약을 위한 24개월 판매 정책입니다."\n      },\n      {\n        "value": "기본판매_신규_할부",\n        "desc": "기본 판매 정책으로 신규 계약 시 할부 결제 방식입니다."\n      },\n      {\n        "value": "2011년 6월 24개월 할부",\n        "desc": "2011년 6월 특정 시점의 24개월 할부 판매 정책입니다."\n      },\n      {\n        "value": "2011년7,8월 인터넷전화 24개월 할부정책",\n        "desc": "2011년 7, 8월 인터넷전화의 24개월 할부 정책입니다."\n      },\n      {\n        "value": "인터넷전화 재약정 정책 (36개월)",\n        "desc": "인터넷전화의 36개월 재약정 정책입니다."\n      },\n      {\n        "value": "USIM 단독개통_후불",\n        "desc": "USIM 단독 개통으로 후불 결제 방식입니다."\n      },\n      {\n        "value": "[★] 인터넷전화 재약정(24개월) 판매정책",\n        "desc": "인터넷전화의 24개월 재약정 판매 정책입니다."\n      },\n      {\n        "value": "인터넷전화 재약정 정책 (24개월)",\n        "desc": "인터넷전화의 24개월 재약정 정책입니다."\n      },\n      {\n        "value": "기본판매_중고/자급제/외산단말",\n        "desc": "기본 판매 정책으로 중고, 자급제, 외산 단말기를 대상으로 합니다."\n      },\n      {\n        "value": "2011년 6월 24개월 할부2",\n        "desc": "2011년 6월 특정 시점의 또 다른 24개월 할부 판매 정책입니다."\n      },\n      {\n        "value": "[★] 인터넷전화 재약정(36개월)판매정책",\n        "desc": "인터넷전화의 36개월 재약정 판매 정책입니다."\n      },\n      {\n        "value": "인터넷전화 재약정 정책 (12개월)",\n        "desc": "인터넷전화의 12개월 재약정 정책입니다."\n      }\n    ]\n  },\n  {\n    "name": "recnt_icg_date",\n    "type": "string",\n    "nullable": true,\n    "description": "최근 기기 변경일자, 값 형식 : YYYYMMDD"\n  },\n  {\n    "name": "tv_apd_terml_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "TV추가 단말여부. 가능한 값 : [Y=존재, N=미존재]"\n  },\n  {\n    "name": "in_forn_div_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "내외국인 구분명. 가능한 값 : [None, 내국인, 외국인]"\n  },\n  {\n    "name": "forn_citiz_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "외국인 국적명. 가능한 값 : [None, 대만, 베트남, 네팔, 필리핀, 영국, 몽골, 중국, 한국, 미국령 사모아]"\n  },\n  {\n    "name": "sojn_prps_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "체류 목적명. 가능한 값 : [None, 유학, 교수, 방문취업, 비전문취업, 특정활동, 재외동포, 결혼이민, 관광취업, 일반연수]"\n  }\n],\n"relations": [\n  {\n    "target_table": "abc_cont",\n    "join_type": "inner",\n    "join_spec": "bidw_camp_cont_txn.svc_cont_id = abc_cont.svc_cont_id",\n    "description": "서비스계약아이디를 기준으로 abc_cont 테이블과 조인"\n  },\n  {\n    "target_table": "rtd_cust",\n    "join_type": "inner",\n    "join_spec": "bidw_camp_cont_txn.src_cust_sorc_id = rtd_cust.src_cust_sorc_id",\n    "description": "원천고객소스아이디 기준으로 rtd_cust 테이블과 조인"\n  }\n]}',
          synonyms: ["캠페인 수행을 위한 고객 동의여부 테이블", "캠페인 수행을 위한 부수적인 회선 정보 테이블", "캠페인 수행을 위한 요금제 테이블", "캠페인 수행을 위한 상품 테이블"],
          created_at: '2024-01-10T09:15:00Z',
          updated_at: '2024-01-18T14:20:00Z'
        },
        {
          id: 3,
          name: 'rtd_cust',
          description: '고객 기본 정보 테이블',
          definition: '{\n"table_name": "rtd_cust",\n"description": "고객 기본 정보 테이블",\n"primary_key": {\n  "columns": ["src_cust_sorc_id"],\n  "description": "원천고객소스아이디"\n},\n"columns": [\n  {\n    "name": "src_cust_sorc_id",\n    "type": "string",\n    "nullable": false,\n    "description": "원천고객소스아이디"\n  },\n  {\n    "name": "inet_comb_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "인터넷결합여부. 가능한 값 : [Y=결합, N=미결합]"\n  },\n  {\n    "name": "iptv_comb_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "IPTV결합여부. 가능한 값 : [Y=결합, N=미결합]"\n  },\n  {\n    "name": "pstn_comb_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "PSTN결합여부. 가능한 값 : [Y=결합, N=미결합]"\n  },\n  {\n    "name": "mphon_comb_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "이동전화결합여부. 가능한 값 : [Y=결합, N=미결합]"\n  },\n  {\n    "name": "efct_pstn_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효PSTN가입건수"\n  },\n  {\n    "name": "efct_mphon_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효이동전화가입건수"\n  },\n  {\n    "name": "efct_soip_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효SOIP가입건수"\n  },\n  {\n    "name": "efct_inet_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효인터넷가입건수"\n  },\n  {\n    "name": "efct_iptv_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효IPTV가입건수"\n  },\n  {\n    "name": "efct_wibro_sbsc_cascnt",\n    "type": "integer",\n    "nullable": true,\n    "description": "유효와이브로가입건수"\n  },\n  {\n    "name": "mphon_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "이동전화가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "smph_use_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "스마트폰여부. 가능한 값 : [Y=스마트폰, N=스마트폰 아님]"\n  },\n  {\n    "name": "kids_adtn_svc_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "아동부가서비스가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "cust_age",\n    "type": "integer",\n    "nullable": true,\n    "description": "고객연령"\n  },\n  {\n    "name": "inet_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "인터넷가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "inet_engt_exp_rmnd_mons_num",\n    "type": "integer",\n    "nullable": true,\n    "description": "인터넷약정만료잔여개월수"\n  },\n  {\n    "name": "soip_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "SOIP가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "pstn_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "PSTN가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "pad_use_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "패드사용여부. 가능한 값 : [Y=사용, N=미사용]"\n  },\n  {\n    "name": "iptv_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "IPTV가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "sex_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "성별유형명. 가능한 값 : [None, 남자, 여자]"\n  },\n  {\n    "name": "cust_clas_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "고객등급명. 가능한 값 : [None, VIP, 일반, Silver, Gold, VVIP, White]"\n  },\n  {\n    "name": "npay_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "미납여부. 가능한 값 : [Y=미납, N=완납]"\n  },\n  {\n    "name": "cust_ctg_type_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "고객분류유형명. 가능한 값 : [개인, 개인사업자]"\n  },\n  {\n    "name": "ec_cust_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "EC고객여부. 가능한 값 : [Y=EC고객, N=EC고객 외 고객]"\n  },\n  {\n    "name": "tngr_sbscr_exist_hshld_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "가구내청소년자녀존재여부. 가능한 값 : [Y=존재, N=미존재]"\n  },\n  {\n    "name": "comb_prod_sbsc_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "결합상품가입여부. 가능한 값 : [Y=가입, N=미가입]"\n  },\n  {\n    "name": "iptv_infn_conts_use_yn",\n    "type": "string",\n    "nullable": true,\n    "description": "IPTV유아콘텐츠사용여부. 가능한 값 : [Y=사용, N=미사용]"\n  },\n  {\n    "name": "cust_tpind_sctg_nm",\n    "type": "string",\n    "nullable": true,\n    "description": "고객업종소분류명. 가능한 값 : [None, 학원, 병원, 음식점, 생활재 판매, 숙박업, 농업, 복지시설, 산업재 판매, 오락/문화 서비스업, 금속, 사업서비스업, 전기전자장비, 임대업, 건설, 음식료, 석유화학, 신문/잡지, 무역, 중개업, 부동산업, 기타 교육시설]"\n  }\n],\n"relations": [\n  {\n    "target_table": "abc_cont",\n    "join_type": "inner",\n    "join_spec": "rtd_cust.svc_cont_id = abc_cont.svc_cont_id",\n    "description": "원천고객소스아이디 기준으로 abc_cont 테이블과 조인"\n  },\n  {\n    "target_table": "bidw_camp_cont_txn",\n    "join_type": "inner",\n    "join_spec": "rtd_cust.src_cust_sorc_id = bidw_camp_cont_txn.src_cust_sorc_id",\n    "description": "원천고객소스아이디 기준으로 bidw_camp_cont_txn 테이블과 조인"\n  }\n]}',
          synonyms: [ "고객 기본 정보 테이블", "고객 속성 정보 테이블" ],
          created_at: '2024-01-10T09:15:00Z',
          updated_at: '2024-01-18T14:20:00Z'
        }
      ]

      sqlQueries.value = [
        {
          id: 1,
          title: '아이폰 신규 프로모션',
          type: 'SELECT',
          schema_id: 1,
          schema_name: 'abc_cont',
          query: "select abc_cont.*\n  from public.abc_cont\n where 1=1\n   and abc_cont.engt_yn = 'Y'\n   and abc_cont.now_hndset_use_day_num >= 540\n   and ( abc_cont.hndset_model_nm like 'AIP%'\n     or abc_cont.hndset_model_nm like 'IPHONE%');",
          description: '아이폰 장기 이용 고객을 조회',
          synonyms: ['아이폰을 1년 6개월 이상 사용한 고객','아이폰을 18개월 이상 보유한 이용자','아이폰 장기 사용 고객','아이폰 장기 이용자','아이폰 장기 고객군','아이폰 장기 유지 고객','아이폰 18개월 이상 가입자','아이폰 충성 고객','아이폰 유지 고객','아이폰 약정 기간 18개월 이상 경과 고객','아이폰 장기 약정 이용 고객'], // 추가
          created_at: '2024-01-16T11:00:00Z',
          updated_at: '2024-01-16T11:00:00Z'
        },
        {
          id: 2,
          title: '신규 고객 유치 케어',
          type: 'SELECT',
          schema_id: 2,
          schema_name: 'bidw_camp_cont_txn',
          query: "select abc_cont.*\n  from public.abc_cont\n       left join public.bidw_camp_cont_txn\n              on ( abc_cont.svc_cont_id = bidw_camp_cont_txn.svc_cont_id )\n where 1=1\n   and abc_cont.engt_yn = 'Y'\n   and abc_cont.no_mov_pre_bizr_itg_cd in ('10002','10005','10008','10009','10015','10040','10041','10049','10081','10082','10095','10107','10109','15131','15152','15168','15182','15184','10003','10007','10016','10045','10090','10094','10114','15118','15120','15121','15123','15124','15126','15127','15133','15135','15136','15138','15140','15141','15143','15145','15146','15147','15150','15153','15155','15156','15157','15158','15159','15160','15161','15165','15166','15167','15169','15171','15173','15186','15190','15192','15194')\n   and ( abc_cont.hndset_model_nm like 'AIP16%'\n     or abc_cont.hndset_model_nm like 'SM-S93%' );",
          description: '타사에서 번호 이동 후 최신 단말을 사용하고 있는 고객을 조회',
          synonyms: ['타사에서 번호 이동 후 최신 단말 (아이폰 XX 삼성 XX 버전 대상) 사용 고객','타사 번호 이동 후 최신 아이폰 또는 삼성 단말 사용자','번호 이동 후 최신 단말 장기 사용자','타사 번호 이동 후 최신 단말 이용자','번호 이동 후 최신 단말 고객군','타사 번호 이동 후 최신 단말 유지 고객','번호 이동 후 최신 단말 가입자','타사 번호 이동 후 최신 단말 고객','번호 이동 후 최신 단말 유지 고객','타사 번호 이동 후 최신 단말 약정 고객'], // 추가
          created_at: '2024-01-17T14:30:00Z',
          updated_at: '2024-01-17T14:30:00Z'
        },
        {
          id: 3,
          title: '결합 상품 유치',
          type: 'SELECT',
          schema_id: 3,
          schema_name: 'rtd_cust',
          query: "select abc_cont.*\n  from public.abc_cont\n       left join public.rtd_cust\n              on ( abc_cont.src_cust_sorc_id = rtd_cust.src_cust_sorc_id )\n where 1=1\n   and abc_cont.engt_yn = 'Y'\n   and abc_cont.inet_comb_circuit_num = 0\n   and rtd_cust.smph_use_yn = 'Y'\n   and rtd_cust.inet_sbsc_yn = 'N';",
          description: '고가 요금제를 장기 이용하고 있는 고객을 조회',
          synonyms: ['모바일고객 중 인턴넷 미사용 고객','모바일 서비스 이용 중 인터넷을 사용하지 않는 고객','인터넷 미사용 모바일 장기 사용자','인터넷을 사용하지 않는 모바일 이용자','인터넷 미사용 모바일 고객군','인터넷을 사용하지 않는 모바일 유지 고객','인터넷 미사용 모바일 가입자','인터넷을 사용하지 않는 모바일 고객','인터넷 미사용 모바일 유지 고객','인터넷 미사용 모바일 약정 고객'], // 추가
          created_at: '2024-01-17T14:30:00Z',
          updated_at: '2024-01-17T14:30:00Z'
        }
      ]
    }

    // Utility functions
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const resetSchemaForm = () => {
      Object.assign(schemaForm, {
        name: '',
        description: '',
        definition: '',
        synonyms: [''] // 동의어 초기화
      })
    }

    const resetSqlForm = () => {
      Object.assign(sqlForm, {
        title: '',
        type: '',
        schema_id: '',
        query: '',
        description: '',
        synonyms: ['']
      })
    }

    // Schema management functions
    const toggleSchemaForm = () => {
      if (showSchemaForm.value) {
        cancelSchemaForm()
      } else {
        showSchemaForm.value = true
        editingSchema.value = null
        resetSchemaForm()
      }
    }

    const cancelSchemaForm = () => {
      showSchemaForm.value = false
      editingSchema.value = null
      resetSchemaForm()
    }

    const saveSchema = async () => {
      // 동의어 검증 추가
      const filteredSynonyms = schemaForm.synonyms.filter(synonym => synonym.trim() !== '')
      
      if (filteredSynonyms.length === 0) {
        alert('동의어를 최소 1개 이상 입력해주세요.')
        return
      }

      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))

        if (editingSchema.value) {
          const index = schemas.value.findIndex(s => s.id === editingSchema.value.id)
          if (index !== -1) {
            schemas.value[index] = {
              ...schemas.value[index],
              // name은 제외 (수정 불가)
              description: schemaForm.description,
              definition: schemaForm.definition,
              synonyms: filteredSynonyms,
              updated_at: new Date().toISOString()
            }
          }
        } else {
          const newSchema = {
            id: Math.max(...schemas.value.map(s => s.id)) + 1,
            name: schemaForm.name,
            description: schemaForm.description,
            definition: schemaForm.definition,
            synonyms: filteredSynonyms,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
          schemas.value.push(newSchema)
        }
        
        cancelSchemaForm()
        alert(editingSchema.value ? '스키마가 수정되었습니다.' : '스키마가 추가되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const editSchema = (schema) => {
       viewSchema(schema)
    }

    const copySchema = async (schema) => {
      loading.value = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        const newSchema = {
          id: Math.max(...schemas.value.map(s => s.id)) + 1,
          name: schema.name + '_copy',
          description: schema.description + ' (복사본)',
          definition: schema.definition,
          synonyms: [...(schema.synonyms || [])],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        schemas.value.push(newSchema)
        alert('스키마가 복사되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const deleteSchema = async (id) => {
      if (!confirm('정말로 이 스키마를 삭제하시겠습니까?')) return
      
      loading.value = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        schemas.value = schemas.value.filter(s => s.id !== id)
        alert('스키마가 삭제되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 동의어 관련 함수들 추가
    const addSynonym = () => {
      schemaForm.synonyms.push('')
    }

    const removeSynonym = (index) => {
      if (schemaForm.synonyms.length > 1) {
        schemaForm.synonyms.splice(index, 1)
      } else {
        alert('최소 1개의 동의어 입력란이 필요합니다.')
      }
    }

    // SQL management functions
    const toggleSqlForm = () => {
      if (showSqlForm.value) {
        cancelSqlForm()
      } else {
        showSqlForm.value = true
        editingSql.value = null
        resetSqlForm()
      }
    }

    const cancelSqlForm = () => {
      showSqlForm.value = false
      editingSql.value = null
      resetSqlForm()
    }

    const saveSql = async () => {
      // 동의어 검증 추가
      const filteredSynonyms = sqlForm.synonyms.filter(synonym => synonym.trim() !== '')
      
      if (filteredSynonyms.length === 0) {
        alert('동의어를 최소 1개 이상 입력해주세요.')
        return
      }

      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const schemaName = schemas.value.find(s => s.id == sqlForm.schema_id)?.name || ''
        
        if (editingSql.value) {
          const index = sqlQueries.value.findIndex(s => s.id === editingSql.value.id)
          if (index !== -1) {
            sqlQueries.value[index] = {
              ...sqlQueries.value[index],
              ...sqlForm,
              synonyms: filteredSynonyms,
              schema_name: schemaName,
              updated_at: new Date().toISOString()
            }
          }
        } else {
          const newSql = {
            id: Math.max(...sqlQueries.value.map(s => s.id)) + 1,
            ...sqlForm,
            synonyms: filteredSynonyms,
            schema_name: schemaName,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
          sqlQueries.value.push(newSql)
        }
        
        cancelSqlForm()
        alert(editingSql.value ? 'SQL이 수정되었습니다.' : 'SQL이 추가되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const viewSql = (sql) => {
      viewingSql.value = sql
      showSqlView.value = true
      // showSqlViewModal.value = true
    }

    const closeSqlView = () => {
      showSqlView.value = false
      viewingSql.value = null
    }

    const editSql = (sql) => {
      editingSql.value = sql
      Object.assign(sqlForm, {
        title: sql.title,
        type: sql.type,
        schema_id: sql.schema_id,
        query: sql.query,
        description: sql.description,
        synonyms: (sql.synonyms && sql.synonyms.length > 0) ? [...sql.synonyms] : [''] // 최소 1개 유지
      })
      showSqlForm.value = true
    }

    const deleteSql = async (id) => {
      if (!confirm('정말로 이 SQL을 삭제하시겠습니까?')) return
      
      loading.value = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        sqlQueries.value = sqlQueries.value.filter(s => s.id !== id)
        alert('SQL이 삭제되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const searchSqlQueries = () => {
      if (!sqlSearchQuery.value.trim()) {
        filteredSqlQueries.value = sqlQueries.value
      } else {
        filteredSqlQueries.value = sqlQueries.value.filter(sql => 
          sql.title.toLowerCase().includes(sqlSearchQuery.value.toLowerCase())
        )
      }
    }

    const isEditingInView = ref(false)
    const viewEditForm = reactive({
      title: '',
      type: '',
      schema_id: '',
      query: '',
      description: '',
      synonyms: ['']
    })

    const startEditInView = () => {
      Object.assign(viewEditForm, {
        title: viewingSql.value.title,
        type: viewingSql.value.type,
        schema_id: viewingSql.value.schema_id,
        query: viewingSql.value.query,
        description: viewingSql.value.description || '',
        synonyms: (viewingSql.value.synonyms && viewingSql.value.synonyms.length > 0) 
          ? [...viewingSql.value.synonyms] 
          : [''] 
      })
      isEditingInView.value = true
    }

    const cancelEditInView = () => {
      isEditingInView.value = false
      Object.assign(viewEditForm, {
        title: '',
        type: '',
        schema_id: '',
        query: '',
        description: '',
        synonyms: [''] // 추가
      })
    }

    const saveEditInView = async () => {
      // 동의어 검증 추가
      const filteredSynonyms = viewEditForm.synonyms.filter(synonym => synonym.trim() !== '')
      
      if (filteredSynonyms.length === 0) {
        alert('동의어를 최소 1개 이상 입력해주세요.')
        return
      }

      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const schemaName = schemas.value.find(s => s.id == viewEditForm.schema_id)?.name || ''
        
        const index = sqlQueries.value.findIndex(s => s.id === viewingSql.value.id)
        if (index !== -1) {
          sqlQueries.value[index] = {
            ...sqlQueries.value[index],
            ...viewEditForm,
            synonyms: filteredSynonyms,
            schema_name: schemaName,
            updated_at: new Date().toISOString()
          }
          
          viewingSql.value = sqlQueries.value[index]
        }
        
        isEditingInView.value = false
        alert('SQL이 수정되었습니다.')
      } catch (error) {
        alert('오류가 발생했습니다: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // Other functions
    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value
    }

    const goToChat = () => {
      router.push('/chat')
    }

    const logout = () => {
      if (confirm('정말로 로그아웃하시겠습니까?')) {
        sessionStorage.removeItem('isLoggedIn')
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('sessionId')
        sessionStorage.removeItem('sessionToken')
        sessionStorage.removeItem('sessionCreatedAt')
        sessionStorage.removeItem('allowSkipPasswordChange')
        
        if (window.currentSession) {
          delete window.currentSession
        }
        
        router.replace('/login')
      }
    }
    
    const vectorizeData = async() => {
      if(!confirm('스키마 및 SQL 데이터 전체를 백터화 처리하시겠습니까?')) return
      
      loading.value = true
      try{
        const response = await fetch('',{
          method: 'POST',
          headers: {
            'Content-Type' : 'application/json',
          },
          body: JSON.stringify({
            schemas: schemas.value,
            sqlQueries: sqlQueries.value
          })
        })

        if(!response.ok){
          throw new Error('백터화 처리에 실패했습니다.')
        }

        const result = await response.json()
        alert('백터화 처리가 완료되었습니다.')
      } catch(error){
        alert('오류가 발생했습니다 : '+error.message)
      } finally{
        loading.value=false
      }
    }

    // Initialize data on mount
    onMounted(() => {
      initializeMockData()
      filteredSchemas.value = schemas.value
      filteredSqlQueries.value = sqlQueries.value
    })

    watch(schemas, () => {
      searchSchemas()
    }, { deep: true })

    watch(schemaSearchQuery, () => {
      searchSchemas()
    })

    watch(sqlQueries, () => {
      searchSqlQueries()
    }, { deep: true })

    watch(sqlSearchQuery, () => {
      searchSqlQueries()
    })

    return {
      // Reactive data
      loading,
      activeTab,
      isSidebarCollapsed,
      schemas,
      sqlQueries,
      showSchemaForm,
      showSqlForm,
      showSqlView,
      editingSchema,
      editingSql,
      viewingSql,
      schemaForm,
      sqlForm,
      isEditingInView,
      viewEditForm,
      schemaSearchQuery,
      filteredSchemas,
      sqlSearchQuery,
      filteredSqlQueries,
      showSchemaView,
      viewingSchema,
      isEditingInSchemaView,
      viewSchemaEditForm,
      
      // Functions
      formatDate,
      toggleSchemaForm,
      cancelSchemaForm,
      saveSchema,
      copySchema,
      editSchema,
      deleteSchema,
      toggleSqlForm,
      cancelSqlForm,
      saveSql,
      viewSql,
      closeSqlView,
      editSql,
      deleteSql,
      toggleSidebar,
      goToChat,
      logout,
      addSynonym,
      removeSynonym,
      startEditInView,
      cancelEditInView,
      saveEditInView,
      searchSchemas,
      searchSqlQueries,
      viewSchema,
      closeSchemaView,
      startEditInSchemaView,
      cancelEditInSchemaView,
      saveEditInSchemaView,
      copySchemaDefinition,
      vectorizeData,
    }
  }
}
</script>

<style src="@/css/sqlManage.css" scoped></style>