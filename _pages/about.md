---
layout: page
title: About
permalink: /about
---

<div class="about-hero">
  <div class="about-hero-bg">
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="shape shape-4"></div>
    </div>
  </div>
  
  <div class="about-hero-content">
    <div class="profile-container">
      <div class="profile-image-wrapper">
        <img src="{{ site.baseurl }}/assets/profile-avatar.png" alt="Profile" class="profile-image">
        <div class="profile-status">
          <span class="status-dot"></span>
          <span class="status-text">Available</span>
        </div>
      </div>
      
      <div class="profile-info">
        <h1 class="profile-name">
          <span class="wave">👋</span> 안녕하세요, takjakim입니다
        </h1>
        <p class="profile-tagline">투자 · 개발 · AI에 관심이 많은 지식 탐험가</p>
        
        <div class="social-links">
          <a href="https://github.com/takjakim" class="social-link" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span>GitHub</span>
          </a>
          <a href="mailto:your.email@example.com" class="social-link">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
            </svg>
            <span>Email</span>
          </a>
          <a href="{{ site.baseurl }}/tags" class="social-link">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z"/>
            </svg>
            <span>Tags</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

<section class="about-section">
  <div class="section-header-about">
    <h2>🎯 What I Do</h2>
  </div>
  
  <div class="expertise-grid">
    <div class="expertise-card expertise-investing">
      <div class="expertise-icon">
        <svg viewBox="0 0 24 24" width="32" height="32">
          <path fill="currentColor" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
        </svg>
      </div>
      <h3>지수 투자</h3>
      <p>미국 지수 투자 전략을 연구하고 매일의 투자 로그를 기록합니다. 장기적 관점에서 꾸준한 성장을 추구합니다.</p>
      <div class="expertise-tags">
        <span class="tag-small">ETF</span>
        <span class="tag-small">Long-term</span>
        <span class="tag-small">Market Analysis</span>
      </div>
    </div>
    
    <div class="expertise-card expertise-dev">
      <div class="expertise-icon">
        <svg viewBox="0 0 24 24" width="32" height="32">
          <path fill="currentColor" d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
        </svg>
      </div>
      <h3>소프트웨어 개발</h3>
      <p>웹 개발과 시스템 아키텍처에 관심이 많습니다. 클린 코드와 효율적인 솔루션을 지향합니다.</p>
      <div class="expertise-tags">
        <span class="tag-small">Web Development</span>
        <span class="tag-small">Architecture</span>
        <span class="tag-small">Best Practices</span>
      </div>
    </div>
    
    <div class="expertise-card expertise-ai">
      <div class="expertise-icon">
        <svg viewBox="0 0 24 24" width="32" height="32">
          <path fill="currentColor" d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/>
        </svg>
      </div>
      <h3>AI 활용</h3>
      <p>AI 도구를 활용하여 생산성을 높이고 새로운 가능성을 탐구합니다. 실용적인 적용에 집중합니다.</p>
      <div class="expertise-tags">
        <span class="tag-small">GPT</span>
        <span class="tag-small">Automation</span>
        <span class="tag-small">Productivity</span>
      </div>
    </div>
    
    <div class="expertise-card expertise-theory">
      <div class="expertise-icon">
        <svg viewBox="0 0 24 24" width="32" height="32">
          <path fill="currentColor" d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/>
        </svg>
      </div>
      <h3>이론과 개념</h3>
      <p>복잡한 개념을 단순하게 이해하고, 다양한 분야의 지식을 연결하는 것을 즐깁니다.</p>
      <div class="expertise-tags">
        <span class="tag-small">Learning</span>
        <span class="tag-small">Concepts</span>
        <span class="tag-small">Knowledge</span>
      </div>
    </div>
  </div>
</section>

<section class="about-section">
  <div class="section-header-about">
    <h2>🚀 Journey Timeline</h2>
  </div>
  
  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-content">
        <div class="timeline-date">2026</div>
        <h3>Digital Garden 시작</h3>
        <p>투자, 개발, AI에 대한 생각과 기록을 연결하는 개인 지식 베이스를 구축하기 시작했습니다.</p>
      </div>
    </div>
    
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-content">
        <div class="timeline-date">Ongoing</div>
        <h3>지속적인 학습</h3>
        <p>매일 새로운 것을 배우고 기록하며, 지식의 연결고리를 만들어가고 있습니다.</p>
      </div>
    </div>
    
    <div class="timeline-item timeline-item-future">
      <div class="timeline-dot"></div>
      <div class="timeline-content">
        <div class="timeline-date">Future</div>
        <h3>더 넓은 탐험</h3>
        <p>앞으로도 호기심을 가지고 다양한 분야를 탐험하며 성장해 나가겠습니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="about-section">
  <div class="section-header-about">
    <h2>💭 Philosophy</h2>
  </div>
  
  <div class="philosophy-cards">
    <div class="philosophy-card">
      <div class="philosophy-number">01</div>
      <h3>꾸준함의 힘</h3>
      <p>작은 것이라도 매일 꾸준히 하는 것이 큰 변화를 만듭니다. 지속가능한 성장을 추구합니다.</p>
    </div>
    
    <div class="philosophy-card">
      <div class="philosophy-number">02</div>
      <h3>연결의 가치</h3>
      <p>개별 지식보다 지식 간의 연결이 더 큰 통찰을 만들어냅니다. 모든 것은 연결되어 있습니다.</p>
    </div>
    
    <div class="philosophy-card">
      <div class="philosophy-number">03</div>
      <h3>실용적 적용</h3>
      <p>이론만으로는 부족합니다. 실제로 적용하고 실험하며 배운 것을 검증합니다.</p>
    </div>
  </div>
</section>

<section class="about-section stats-section">
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon">📝</div>
      <div class="stat-value">{{ site.notes | size }}</div>
      <div class="stat-label">Total Notes</div>
    </div>
    
    <div class="stat-card">
      <div class="stat-icon">🏷️</div>
      <div class="stat-value">
        {% assign all_tags = "" | split: "" %}
        {% for note in site.notes %}
          {% if note.tags %}
            {% for tag in note.tags %}
              {% assign all_tags = all_tags | push: tag %}
            {% endfor %}
          {% endif %}
        {% endfor %}
        {{ all_tags | uniq | size }}
      </div>
      <div class="stat-label">Unique Tags</div>
    </div>
    
    <div class="stat-card">
      <div class="stat-icon">🔗</div>
      <div class="stat-value">∞</div>
      <div class="stat-label">Connections</div>
    </div>
    
    <div class="stat-card">
      <div class="stat-icon">🌱</div>
      <div class="stat-value">Growing</div>
      <div class="stat-label">Status</div>
    </div>
  </div>
</section>

<section class="about-section cta-section">
  <div class="cta-card">
    <h2>함께 성장해요</h2>
    <p>Digital Garden을 탐험하고 지식의 연결고리를 따라가보세요</p>
    <div class="cta-buttons">
      <a href="{{ site.baseurl }}/" class="cta-btn cta-primary">
        <span>홈으로 가기</span>
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
        </svg>
      </a>
      <a href="{{ site.baseurl }}/tags" class="cta-btn cta-secondary">
        <span>태그 탐색</span>
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
        </svg>
      </a>
    </div>
  </div>
</section>

<style>
/* ===== About Page Hero ===== */
.about-hero {
  position: relative;
  margin: -4vh -6vw 3rem;
  min-height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  
  @media (min-width: 1200px) {
    margin: -4vh -4vw 3rem;
  }
}

.about-hero-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #4ECDC4, #556270);
  bottom: -80px;
  right: -80px;
  animation-delay: -7s;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #F59E0B, #FF6B6B);
  top: 50%;
  right: 10%;
  animation-delay: -14s;
}

.shape-4 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #8B5CF6, #4ECDC4);
  bottom: 20%;
  left: 15%;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  33% {
    transform: translate(30px, -30px) rotate(120deg);
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg);
  }
}

.about-hero-content {
  position: relative;
  z-index: 1;
  padding: 3rem 2rem;
  width: 100%;
  max-width: 900px;
}

/* ===== Profile Section ===== */
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  
  @media (min-width: 768px) {
    flex-direction: row;
    gap: 3rem;
  }
}

.profile-image-wrapper {
  position: relative;
  flex-shrink: 0;
}

.profile-image {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.05) rotate(5deg);
  }
}

.profile-status {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 0.75rem;
  font-weight: 600;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #10B981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-text {
  color: #10B981;
}

.profile-info {
  flex: 1;
  text-align: center;
  
  @media (min-width: 768px) {
    text-align: left;
  }
}

.profile-name {
  font-size: clamp(1.8rem, 5vw, 2.5rem);
  font-weight: 800;
  margin: 0 0 0.5rem;
  line-height: 1.2;
  color: #1a1a2e;
}

.wave {
  display: inline-block;
  animation: wave 2.5s infinite;
  transform-origin: 70% 70%;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  10%, 30% { transform: rotate(14deg); }
  20% { transform: rotate(-8deg); }
  40%, 100% { transform: rotate(0deg); }
}

.profile-tagline {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0 0 2rem;
  line-height: 1.6;
}

.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  
  @media (min-width: 768px) {
    justify-content: flex-start;
  }
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1.2rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 50px;
  text-decoration: none;
  color: #1a1a2e;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    background: white !important;
    border-color: #FF6B6B;
  }
  
  &:after {
    content: '' !important;
  }
  
  svg {
    flex-shrink: 0;
  }
}

/* ===== About Sections ===== */
.about-section {
  margin: 4rem 0;
}

.section-header-about {
  text-align: center;
  margin-bottom: 3rem;
  
  h2 {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 800;
    color: #1a1a2e;
    margin: 0;
  }
}

/* ===== Expertise Grid ===== */
.expertise-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.expertise-card {
  padding: 2rem;
  border-radius: 20px;
  background: white;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    padding: 2px;
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    &::before {
      opacity: 1;
    }
    
    .expertise-icon {
      transform: scale(1.1) rotate(5deg);
    }
  }
  
  h3 {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 1rem 0 0.8rem;
    color: #1a1a2e;
  }
  
  p {
    color: #6b7280;
    line-height: 1.7;
    margin: 0 0 1.2rem;
  }
}

.expertise-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.expertise-investing .expertise-icon {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
}

.expertise-dev .expertise-icon {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
}

.expertise-ai .expertise-icon {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
}

.expertise-theory .expertise-icon {
  background: linear-gradient(135deg, #3B82F6, #2563EB);
  color: white;
}

.expertise-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-small {
  padding: 0.3rem 0.8rem;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 20px;
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

/* ===== Timeline ===== */
.timeline {
  position: relative;
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem 0;
  
  &::before {
    content: '';
    position: absolute;
    left: 20px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(180deg, #FF6B6B, #4ECDC4);
    
    @media (min-width: 768px) {
      left: 50%;
      transform: translateX(-50%);
    }
  }
}

.timeline-item {
  position: relative;
  padding-left: 60px;
  margin-bottom: 3rem;
  
  @media (min-width: 768px) {
    width: 50%;
    padding-left: 0;
    padding-right: 40px;
    
    &:nth-child(even) {
      margin-left: 50%;
      padding-right: 0;
      padding-left: 40px;
      
      .timeline-content {
        text-align: left;
      }
      
      .timeline-dot {
        left: -13px;
      }
    }
  }
}

.timeline-dot {
  position: absolute;
  left: 13px;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  box-shadow: 0 0 0 4px white, 0 0 0 6px rgba(255, 107, 107, 0.3);
  
  @media (min-width: 768px) {
    left: auto;
    right: -13px;
  }
}

.timeline-item-future .timeline-dot {
  background: linear-gradient(135deg, #4ECDC4, #8B5CF6);
  box-shadow: 0 0 0 4px white, 0 0 0 6px rgba(78, 205, 196, 0.3);
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% {
    box-shadow: 0 0 0 4px white, 0 0 0 6px rgba(78, 205, 196, 0.3);
  }
  50% {
    box-shadow: 0 0 0 4px white, 0 0 0 12px rgba(78, 205, 196, 0.1);
  }
}

.timeline-content {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  }
  
  h3 {
    margin: 0.5rem 0;
    font-size: 1.2rem;
    color: #1a1a2e;
  }
  
  p {
    margin: 0.5rem 0 0;
    color: #6b7280;
    line-height: 1.6;
  }
}

.timeline-date {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  color: white;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* ===== Philosophy Cards ===== */
.philosophy-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(3, 1fr);
  }
}

.philosophy-card {
  padding: 2rem;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.05), rgba(78, 205, 196, 0.05));
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    background: white;
  }
  
  h3 {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0.8rem 0;
    color: #1a1a2e;
  }
  
  p {
    color: #6b7280;
    line-height: 1.7;
    margin: 0;
  }
}

.philosophy-number {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

/* ===== Stats Section ===== */
.stats-section {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.03), rgba(78, 205, 196, 0.03));
  padding: 3rem 2rem;
  border-radius: 24px;
  margin: 4rem 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(4, 1fr);
  }
}

.stat-card {
  text-align: center;
  padding: 1.5rem 1rem;
  background: white;
  border-radius: 16px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  }
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0.3rem 0;
}

.stat-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ===== CTA Section ===== */
.cta-section {
  margin: 5rem 0 3rem;
}

.cta-card {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 24px;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 107, 107, 0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
  }
  
  h2 {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 800;
    margin: 0 0 1rem;
    position: relative;
    z-index: 1;
  }
  
  p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0 0 2rem;
    position: relative;
    z-index: 1;
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.cta-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  
  &:after {
    content: '' !important;
  }
  
  svg {
    transition: transform 0.3s ease;
  }
  
  &:hover svg {
    transform: translateX(4px);
  }
}

.cta-primary {
  background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  color: white;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(255, 107, 107, 0.4);
    background: linear-gradient(135deg, #ff5555, #3dbbb3) !important;
  }
}

.cta-secondary {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-3px);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .about-hero {
    min-height: 400px;
  }
  
  .shape {
    display: none;
  }
  
  .about-section {
    margin: 3rem 0;
  }
  
  .section-header-about {
    margin-bottom: 2rem;
  }
}
</style>
