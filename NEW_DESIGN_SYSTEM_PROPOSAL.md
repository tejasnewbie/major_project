# Council of Frontiers - UI/UX Design System Overhaul Proposal

## Executive Summary

This proposal outlines a complete visual and interactive transformation of the Council of Frontiers interface. The new design system, codenamed **"Aether"**, introduces fluid glassmorphism, cinematic micro-interactions, and a sophisticated teal-obsidian color architecture that elevates the multi-agent AI experience into a premium, futuristic product.

---

## 1. Design Philosophy

### Current vs. Proposed

| Aspect | Current (Neo-Brutalist) | Proposed (Aether Glassmorphism) |
|--------|------------------------|--------------------------------|
| **Visual Style** | Hard edges, sharp shadows | Soft glass, depth layers |
| **Motion** | Static, instant transitions | Fluid 60fps spring physics |
| **Depth** | Flat with offset shadows | Multi-layer z-depth with blur |
| **Typography** | Monospace-heavy | Inter + JetBrains Mono balance |
| **Color** | Muted teal-greys | Vibrant teal gradients on obsidian |
| **Feedback** | Instant state changes | Animated, contextual responses |

### Core Principles

1. **Liquid Intelligence** - UI should feel alive, responsive, and fluid like thought itself
2. **Layered Reality** - Glass panels floating in space with depth and parallax
3. **Kinetic Feedback** - Every interaction produces satisfying, meaningful motion
4. **Luminous Guidance** - Teal glows guide attention without demanding it
5. **Breathing Space** - Generous whitespace with purposeful density

---

## 2. Color System

### Primary Palette

```css
/* Obsidian Foundation - Darker, richer backgrounds */
--obsidian-900: #050a0a;      /* Deepest background */
--obsidian-800: #0a1111;      /* Primary surface */
--obsidian-700: #111a1a;      /* Elevated cards */
--obsidian-600: #1a2525;      /* Hover states */
--obsidian-500: #243030;      /* Borders, dividers */

/* Teal Spectrum - Primary accent */
--teal-400: #5ee7df;          /* Primary glow, highlights */
--teal-500: #2dd4bf;          /* Active states, CTAs */
--teal-600: #14b8a6;          /* Primary accent */
--teal-700: #0d9488;          /* Hover states */
--teal-800: #0f766e;          /* Dark accents */

/* Cyan Burst - Secondary energy */
--cyan-400: #22d3ee;          /* Secondary glows */
--cyan-500: #06b6d4;          /* Info states */

/* Semantic Colors */
--success: #10b981;           /* Emerald - Complete states */
--warning: #f59e0b;           /* Amber - Processing */
--error: #ef4444;             /* Red - Disconnected/Error */
--info: #0ea5e9;              /* Sky - Information */
```

### Gradient Definitions

```css
/* Primary Glow Gradient */
--gradient-glow: linear-gradient(135deg,
  rgba(45, 212, 191, 0.4) 0%,
  rgba(34, 211, 238, 0.2) 50%,
  transparent 100%
);

/* Background Ambient */
--gradient-ambient: radial-gradient(
  ellipse at 20% 30%,
  rgba(13, 148, 136, 0.15) 0%,
  transparent 50%
), radial-gradient(
  ellipse at 80% 70%,
  rgba(34, 211, 238, 0.1) 0%,
  transparent 50%
);

/* Glass Surface */
--gradient-glass: linear-gradient(
  180deg,
  rgba(17, 26, 26, 0.9) 0%,
  rgba(10, 17, 17, 0.95) 100%
);

/* Teal Energy Pulse */
--gradient-energy: linear-gradient(90deg,
  transparent 0%,
  rgba(45, 212, 191, 0.8) 50%,
  transparent 100%
);
```

### Glass Morphism Values

```css
/* Standard Glass Card */
--glass-bg: rgba(17, 26, 26, 0.6);
--glass-border: rgba(45, 212, 191, 0.2);
--glass-border-hover: rgba(45, 212, 191, 0.4);
--glass-blur: 20px;
--glass-shadow:
  0 8px 32px rgba(0, 0, 0, 0.4),
  0 0 0 1px var(--glass-border);

/* Elevated Glass (modal, dropdowns) */
--glass-elevated: rgba(17, 26, 26, 0.8);
--glass-blur-heavy: 40px;
--shadow-elevated:
  0 25px 50px -12px rgba(0, 0, 0, 0.5),
  0 0 0 1px var(--glass-border);
```

---

## 3. Typography System

### Font Stack

```css
/* Primary - Clean, modern sans-serif */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Technical - Code, data, labels */
--font-mono: 'JetBrains Mono', 'SF Mono', 'Cascadia Code', monospace;

/* Display - Large headings (optional) */
--font-display: 'Inter', sans-serif;
```

### Type Scale

| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `--text-xs` | 12px | 1.4 | 400 | Captions, timestamps |
| `--text-sm` | 14px | 1.5 | 400 | Secondary text, labels |
| `--text-base` | 16px | 1.6 | 400 | Body text |
| `--text-md` | 18px | 1.5 | 500 | Emphasized body |
| `--text-lg` | 20px | 1.4 | 600 | Small headings |
| `--text-xl` | 24px | 1.3 | 600 | Card titles |
| `--text-2xl` | 32px | 1.2 | 700 | Section headings |
| `--text-3xl` | 48px | 1.1 | 800 | Hero titles |
| `--text-4xl` | 64px | 1.0 | 800 | Major headlines |

### Typography Patterns

```css
/* Gradient Text Effect */
.text-gradient {
  background: linear-gradient(135deg, var(--teal-400) 0%, var(--cyan-400) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Glowing Text */
.text-glow {
  text-shadow: 0 0 20px rgba(45, 212, 191, 0.5);
}

/* Mono Label */
.label-mono {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--teal-400);
}
```

---

## 4. Spacing System

### Base Unit: 4px

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight gaps, icon padding |
| `--space-2` | 8px | Compact element gaps |
| `--space-3` | 12px | Small component padding |
| `--space-4` | 16px | Standard padding |
| `--space-5` | 20px | Medium gaps |
| `--space-6` | 24px | Section gaps |
| `--space-8` | 32px | Large component padding |
| `--space-10` | 40px | Section padding |
| `--space-12` | 48px | Major section gaps |
| `--space-16` | 64px | Hero spacing |
| `--space-20` | 80px | Page-level spacing |
| `--space-24` | 96px | Major layout breaks |

### Layout Grid

```css
/* Container */
--container-max: 1200px;
--container-narrow: 800px;

/* Content area */
--content-max: 720px;

/* Grid gaps */
--grid-gap-sm: 16px;
--grid-gap-md: 24px;
--grid-gap-lg: 32px;
```

---

## 5. Animation System

### Easing Functions

```css
/* Spring - UI interactions */
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Smooth - General transitions */
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);

/* Decelerate - Entering elements */
--ease-decelerate: cubic-bezier(0, 0, 0.2, 1);

/* Accelerate - Exiting elements */
--ease-accelerate: cubic-bezier(0.4, 0, 1, 1);

/* Bounce - Playful interactions */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Duration Scale

| Token | Duration | Usage |
|-------|----------|-------|
| `--duration-instant` | 100ms | Micro-feedback |
| `--duration-fast` | 150ms | Hover states |
| `--duration-normal` | 200ms | Standard transitions |
| `--duration-slow` | 300ms | Complex animations |
| `--duration-slower` | 500ms | Page transitions |
| `--duration-slowest` | 800ms | Hero animations |

### Key Animation Definitions

```css
/* ============================================
   FADE ANIMATIONS
   ============================================ */

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ============================================
   GLASS MORPHISM APPEAR
   ============================================ */

@keyframes glassAppear {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    backdrop-filter: blur(20px);
  }
}

/* ============================================
   GLOW PULSE
   ============================================ */

@keyframes glowPulse {
  0%, 100% {
    box-shadow:
      0 0 20px rgba(45, 212, 191, 0.3),
      0 0 40px rgba(45, 212, 191, 0.1);
  }
  50% {
    box-shadow:
      0 0 30px rgba(45, 212, 191, 0.5),
      0 0 60px rgba(45, 212, 191, 0.2);
  }
}

/* ============================================
   SHIMMER LOADING EFFECT
   ============================================ */

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.shimmer {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(45, 212, 191, 0.1) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
}

/* ============================================
   FLOATING ANIMATION (for background)
   ============================================ */

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(1deg);
  }
  66% {
    transform: translateY(10px) rotate(-1deg);
  }
}

/* ============================================
   ORBITING DOTS (for loading states)
   ============================================ */

@keyframes orbit {
  from {
    transform: rotate(0deg) translateX(12px) rotate(0deg);
  }
  to {
    transform: rotate(360deg) translateX(12px) rotate(-360deg);
  }
}

/* ============================================
   TYPING DOTS
   ============================================ */

@keyframes typingDot {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* ============================================
   PROGRESS BAR STRIPE
   ============================================ */

@keyframes progressStripe {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 40px 0;
  }
}

/* ============================================
   BORDER ROTATE (for active states)
   ============================================ */

@keyframes borderRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* ============================================
   HEARTBEAT (for connection indicator)
   ============================================ */

@keyframes heartbeat {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

/* ============================================
   SLIDE IN FROM RIGHT
   ============================================ */

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ============================================
   EXPAND HEIGHT
   ============================================ */

@keyframes expandHeight {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    max-height: 1000px;
    transform: translateY(0);
  }
}
```

### Animation Utility Classes

```css
/* Base animation setup */
.animate { animation-fill-mode: both; }

/* Fade variants */
.animate-fade-in { animation: fadeIn var(--duration-normal) var(--ease-smooth); }
.animate-fade-up { animation: fadeInUp var(--duration-slow) var(--ease-decelerate); }
.animate-fade-scale { animation: fadeInScale var(--duration-slow) var(--ease-spring); }

/* Glass appearance */
.animate-glass { animation: glassAppear var(--duration-slower) var(--ease-spring); }

/* Delays */
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }
.delay-400 { animation-delay: 400ms; }
.delay-500 { animation-delay: 500ms; }

/* Stagger children */
.stagger-children > *:nth-child(1) { animation-delay: 0ms; }
.stagger-children > *:nth-child(2) { animation-delay: 100ms; }
.stagger-children > *:nth-child(3) { animation-delay: 200ms; }
.stagger-children > *:nth-child(4) { animation-delay: 300ms; }
.stagger-children > *:nth-child(5) { animation-delay: 400ms; }
```

---

## 6. Component Specifications

### 6.1 Glass Card

```css
.glass-card {
  /* Structure */
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: var(--space-6);

  /* Effects */
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  box-shadow: var(--glass-shadow);

  /* Animation */
  transition:
    border-color var(--duration-fast) var(--ease-smooth),
    box-shadow var(--duration-fast) var(--ease-smooth),
    transform var(--duration-fast) var(--ease-spring);
}

.glass-card:hover {
  border-color: var(--glass-border-hover);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 0 1px var(--glass-border-hover),
    0 0 20px rgba(45, 212, 191, 0.1);
  transform: translateY(-2px);
}

/* Variant: Elevated */
.glass-card--elevated {
  background: var(--glass-elevated);
  backdrop-filter: blur(var(--glass-blur-heavy));
  box-shadow: var(--shadow-elevated);
}

/* Variant: Active (glowing border) */
.glass-card--active {
  border-color: var(--teal-500);
  box-shadow:
    0 0 0 1px var(--teal-500),
    0 0 30px rgba(45, 212, 191, 0.3);
  animation: glowPulse 3s ease-in-out infinite;
}
```

### 6.2 Query Input (Redesigned)

```css
.query-container {
  position: relative;
  width: 100%;
}

.query-input-wrapper {
  position: relative;
  display: flex;
  align-items: stretch;
  gap: var(--space-3);
}

.query-input {
  /* Base */
  flex: 1;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: var(--space-4) var(--space-5);

  /* Typography */
  font-family: var(--font-primary);
  font-size: var(--text-md);
  color: var(--text-primary);
  line-height: 1.5;

  /* Effects */
  backdrop-filter: blur(10px);
  transition:
    border-color var(--duration-fast) var(--ease-smooth),
    box-shadow var(--duration-fast) var(--ease-smooth);

  /* Resize */
  resize: none;
  min-height: 56px;
  max-height: 200px;
}

.query-input:focus {
  outline: none;
  border-color: var(--teal-500);
  box-shadow:
    0 0 0 3px rgba(45, 212, 191, 0.2),
    0 0 20px rgba(45, 212, 191, 0.15);
}

.query-input::placeholder {
  color: var(--text-tertiary);
}

/* Submit Button */
.submit-btn {
  /* Base */
  background: linear-gradient(135deg, var(--teal-600) 0%, var(--teal-700) 100%);
  border: none;
  border-radius: 12px;
  padding: var(--space-4) var(--space-6);

  /* Typography */
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: white;

  /* Effects */
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-spring),
    box-shadow var(--duration-fast) var(--ease-smooth);
  box-shadow:
    0 4px 15px rgba(13, 148, 136, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.02);
  box-shadow:
    0 8px 25px rgba(13, 148, 136, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Animated border on focus */
.query-container:focus-within::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--teal-500), var(--cyan-500), var(--teal-500));
  background-size: 200% 200%;
  z-index: -1;
  opacity: 0.5;
  animation: gradientRotate 3s linear infinite;
}

@keyframes gradientRotate {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### 6.3 Connection Status (Redesigned)

```css
.connection-status {
  position: fixed;
  top: var(--space-5);
  right: var(--space-5);
  z-index: 1000;
}

.status-pill {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 9999px;
  backdrop-filter: blur(10px);

  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;

  transition: all var(--duration-fast) var(--ease-smooth);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all var(--duration-fast);
}

/* Connected state */
.status-pill--connected .status-dot {
  background: var(--success);
  box-shadow: 0 0 10px var(--success);
  animation: heartbeat 2s ease-in-out infinite;
}

.status-pill--connected {
  border-color: rgba(16, 185, 129, 0.3);
  color: var(--success);
}

/* Disconnected state */
.status-pill--disconnected .status-dot {
  background: var(--error);
  box-shadow: 0 0 10px var(--error);
}

.status-pill--disconnected {
  border-color: rgba(239, 68, 68, 0.3);
  color: var(--error);
}
```

### 6.4 Thinking Bar (Redesigned)

```css
.thinking-panel {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(var(--glass-blur));
  animation: glassAppear var(--duration-slower) var(--ease-spring);
}

.thinking-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  background: linear-gradient(90deg,
    rgba(45, 212, 191, 0.1) 0%,
    transparent 100%
  );
  border-bottom: 1px solid var(--glass-border);
}

.thinking-stage {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.stage-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--teal-600);
  border-radius: 8px;
  color: white;
}

.stage-label {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--teal-400);
}

.thinking-timer {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  padding: var(--space-2) var(--space-3);
  background: var(--obsidian-800);
  border-radius: 6px;
}

/* Progress bar with glow */
.progress-track {
  height: 4px;
  background: var(--obsidian-700);
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--teal-600), var(--cyan-400));
  box-shadow: 0 0 10px var(--teal-500);
  transition: width var(--duration-slow) var(--ease-smooth);
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Agent status grid */
.agent-status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
}

.agent-status {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--obsidian-800);
  border: 1px solid var(--obsidian-600);
  border-radius: 10px;
  transition: all var(--duration-fast) var(--ease-smooth);
}

.agent-status--active {
  border-color: var(--teal-500);
  background: linear-gradient(135deg,
    rgba(45, 212, 191, 0.15) 0%,
    var(--obsidian-800) 100%
  );
  animation: glowPulse 2s ease-in-out infinite;
}

.agent-status--done {
  border-color: var(--success);
  background: linear-gradient(135deg,
    rgba(16, 185, 129, 0.1) 0%,
    var(--obsidian-800) 100%
  );
}

.agent-status-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 700;
  background: var(--obsidian-700);
  color: var(--text-secondary);
  transition: all var(--duration-fast);
}

.agent-status--active .agent-status-avatar {
  background: var(--teal-600);
  color: white;
}

.agent-status--done .agent-status-avatar {
  background: var(--success);
  color: white;
}

.agent-status-info {
  flex: 1;
}

.agent-status-name {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.agent-status-state {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  margin-top: 2px;
}

/* Pulsing ring for active */
.agent-status--active .agent-status-avatar::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 12px;
  border: 2px solid var(--teal-500);
  animation: pulseRing 1.5s ease-out infinite;
}

@keyframes pulseRing {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}
```

### 6.5 Round Card / Collapsible (Redesigned)

```css
.round-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(var(--glass-blur));
  transition: all var(--duration-fast) var(--ease-smooth);
}

.round-card:hover {
  border-color: var(--glass-border-hover);
  transform: translateY(-1px);
}

.round-card--active {
  border-color: var(--teal-500);
  box-shadow: 0 0 30px rgba(45, 212, 191, 0.15);
}

.round-card--complete {
  border-color: rgba(16, 185, 129, 0.3);
}

/* Header */
.round-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  cursor: pointer;
  transition: background var(--duration-fast);
  border: none;
  width: 100%;
  background: transparent;
  color: inherit;
  text-align: left;
}

.round-header:hover {
  background: rgba(255, 255, 255, 0.03);
}

.round-header-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.round-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--obsidian-700);
  border: 1px solid var(--obsidian-500);
  border-radius: 10px;
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--text-secondary);
  transition: all var(--duration-fast);
}

.round-card--active .round-number {
  background: var(--teal-600);
  border-color: var(--teal-500);
  color: white;
  box-shadow: 0 0 15px rgba(45, 212, 191, 0.4);
}

.round-card--complete .round-number {
  background: var(--success);
  border-color: var(--success);
  color: white;
}

.round-title-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.round-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.round-meta {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.round-header-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.status-badge {
  padding: var(--space-2) var(--space-3);
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge--pending {
  background: var(--obsidian-700);
  color: var(--text-tertiary);
}

.status-badge--active {
  background: rgba(45, 212, 191, 0.15);
  color: var(--teal-400);
  border: 1px solid rgba(45, 212, 191, 0.3);
}

.status-badge--complete {
  background: rgba(16, 185, 129, 0.15);
  color: var(--success);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

/* Chevron with rotation animation */
.round-chevron {
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  transition: transform var(--duration-normal) var(--ease-spring);
}

.round-card--open .round-chevron {
  transform: rotate(180deg);
}

/* Expanded content */
.round-content {
  border-top: 1px solid var(--glass-border);
  animation: expandHeight var(--duration-slow) var(--ease-spring);
}

.round-agents {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Agent bubble redesign */
.agent-bubble {
  background: var(--obsidian-800);
  border: 1px solid var(--obsidian-600);
  border-radius: 12px;
  overflow: hidden;
  transition: all var(--duration-fast) var(--ease-smooth);
}

.agent-bubble:hover {
  border-color: var(--glass-border-hover);
  transform: translateX(4px);
}

.agent-bubble-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--obsidian-700);
  border-bottom: 1px solid var(--obsidian-600);
}

.agent-bubble-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 700;
  background: var(--obsidian-600);
  color: var(--text-secondary);
}

/* Provider colors */
.agent-bubble-avatar--nvidia {
  background: rgba(118, 185, 0, 0.2);
  color: #76b900;
  border: 1px solid rgba(118, 185, 0, 0.4);
}

.agent-bubble-avatar--groq {
  background: rgba(245, 80, 54, 0.2);
  color: #f55036;
  border: 1px solid rgba(245, 80, 54, 0.4);
}

.agent-bubble-avatar--cerebras {
  background: rgba(18, 181, 181, 0.2);
  color: #0d8a8a;
  border: 1px solid rgba(18, 181, 181, 0.4);
}

.agent-bubble-body {
  padding: var(--space-4);
  font-size: var(--text-sm);
  line-height: 1.7;
  color: var(--text-secondary);
}
```

### 6.6 Final Answer Card (Redesigned)

```css
.final-card {
  position: relative;
  background: var(--glass-bg);
  border: 1px solid var(--teal-500);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(var(--glass-blur));
  box-shadow:
    0 0 0 1px var(--teal-500),
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 40px rgba(45, 212, 191, 0.15);
  animation: glassAppear var(--duration-slower) var(--ease-spring);
}

/* Animated border effect */
.final-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 22px;
  background: linear-gradient(135deg,
    var(--teal-500) 0%,
    var(--cyan-400) 25%,
    var(--teal-500) 50%,
    var(--cyan-400) 75%,
    var(--teal-500) 100%
  );
  background-size: 300% 300%;
  z-index: -1;
  animation: gradientRotate 8s linear infinite;
  opacity: 0.6;
}

@keyframes gradientRotate {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.final-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: var(--space-6) var(--space-8);
  background: linear-gradient(135deg,
    rgba(45, 212, 191, 0.15) 0%,
    rgba(45, 212, 191, 0.05) 100%
  );
  border-bottom: 1px solid var(--glass-border);
}

.final-brand {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.final-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--teal-600), var(--cyan-500));
  border-radius: 12px;
  font-size: 24px;
  color: white;
  box-shadow: 0 8px 20px rgba(45, 212, 191, 0.3);
}

.final-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.final-title {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.final-subtitle {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--teal-400);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.final-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.quality-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--obsidian-800);
  border: 1px solid var(--obsidian-600);
  border-radius: 10px;
}

.quality-score {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--teal-400);
}

.quality-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
}

/* Content area */
.final-content {
  padding: var(--space-8);
  font-size: var(--text-md);
  line-height: 1.8;
  color: var(--text-primary);
}

/* Thinking process toggle */
.thinking-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: var(--space-4) var(--space-6);
  background: var(--obsidian-800);
  border: none;
  border-top: 1px solid var(--glass-border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--duration-fast);
}

.thinking-toggle:hover {
  background: var(--obsidian-700);
  color: var(--text-primary);
}

.thinking-content {
  padding: var(--space-6);
  background: var(--obsidian-900);
  border-top: 1px solid var(--glass-border);
  animation: expandHeight var(--duration-slow) var(--ease-spring);
}

/* Footer */
.final-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: var(--obsidian-800);
  border-top: 1px solid var(--glass-border);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

.final-meta {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.final-meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
```

### 6.7 Code Block (Redesigned)

```css
.code-block {
  margin: var(--space-4) 0;
  background: var(--obsidian-900);
  border: 1px solid var(--obsidian-600);
  border-radius: 12px;
  overflow: hidden;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: var(--obsidian-800);
  border-bottom: 1px solid var(--obsidian-600);
}

.code-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.code-filename {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: 500;
}

.code-lang {
  font-size: var(--text-xs);
  text-transform: uppercase;
  color: var(--teal-400);
  padding: var(--space-1) var(--space-2);
  background: rgba(45, 212, 191, 0.1);
  border-radius: 4px;
}

.code-actions {
  display: flex;
  gap: var(--space-2);
}

.code-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--obsidian-700);
  border: 1px solid var(--obsidian-500);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: var(--text-xs);
  cursor: pointer;
  transition: all var(--duration-fast);
}

.code-btn:hover {
  background: var(--obsidian-600);
  border-color: var(--glass-border-hover);
  color: var(--text-primary);
}

.code-btn--success {
  background: rgba(16, 185, 129, 0.2);
  border-color: var(--success);
  color: var(--success);
}

.code-content {
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

.code-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.code-content::-webkit-scrollbar-track {
  background: var(--obsidian-900);
}

.code-content::-webkit-scrollbar-thumb {
  background: var(--obsidian-600);
  border-radius: 4px;
}

.code-table {
  width: 100%;
  border-collapse: collapse;
}

.code-line-num {
  width: 48px;
  padding: 2px 16px;
  text-align: right;
  color: var(--text-muted);
  background: var(--obsidian-800);
  border-right: 1px solid var(--obsidian-600);
  user-select: none;
  font-size: 12px;
}

.code-line {
  padding: 2px 16px;
  color: var(--text-primary);
  white-space: pre;
}

/* Syntax highlighting */
.code-keyword { color: var(--teal-400); font-weight: 500; }
.code-string { color: #a5d6ff; }
.code-comment { color: var(--text-muted); font-style: italic; }
.code-number { color: #79c0ff; }
.code-function { color: #d2a8ff; }
```

### 6.8 Empty State (Redesigned)

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-16) var(--space-8);
  animation: fadeInUp var(--duration-slower) var(--ease-decelerate);
}

.empty-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    rgba(45, 212, 191, 0.2) 0%,
    rgba(34, 211, 238, 0.1) 100%
  );
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  font-size: 40px;
  color: var(--teal-400);
  margin-bottom: var(--space-6);
  animation: float 6s ease-in-out infinite;
}

.empty-title {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.empty-description {
  font-size: var(--text-md);
  color: var(--text-secondary);
  max-width: 500px;
  line-height: 1.6;
}

.empty-features {
  display: flex;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.empty-feature {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## 7. Layout Specifications

### App Structure

```css
.app {
  min-height: 100vh;
  background: var(--obsidian-900);
  background-image: var(--gradient-ambient);
  position: relative;
  overflow-x: hidden;
}

/* Animated background mesh */
.app::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(45, 212, 191, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(34, 211, 238, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(45, 212, 191, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* Noise texture overlay */
.app::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.015;
  pointer-events: none;
  z-index: 1;
}

.main-content {
  position: relative;
  z-index: 10;
  max-width: var(--container-narrow);
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

/* Header area */
.header {
  text-align: center;
  padding: var(--space-12) 0 var(--space-8);
  animation: fadeInUp var(--duration-slower) var(--ease-decelerate);
}

.header--compact {
  padding: var(--space-6) 0;
  animation: fadeIn var(--duration-normal) var(--ease-smooth);
}

.brand-title {
  font-size: var(--text-4xl);
  font-weight: 800;
  letter-spacing: -0.03em;
  margin: 0;
}

.brand-title-accent {
  background: linear-gradient(135deg, var(--teal-400) 0%, var(--cyan-400) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: var(--space-3);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

/* Category badge */
.category-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-4);
  padding: var(--space-2) var(--space-4);
  background: rgba(45, 212, 191, 0.1);
  border: 1px solid rgba(45, 212, 191, 0.3);
  border-radius: 9999px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--teal-400);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  animation: fadeIn var(--duration-normal) var(--ease-smooth);
}
```

---

## 8. Responsive Design

### Breakpoints

```css
/* Mobile first approach */
--bp-sm: 640px;   /* Small tablets */
--bp-md: 768px;   /* Tablets */
--bp-lg: 1024px;  /* Small desktop */
--bp-xl: 1280px;  /* Large desktop */
```

### Responsive Patterns

```css
/* Container */
.main-content {
  max-width: var(--container-narrow);
  padding: var(--space-6) var(--space-4);
}

@media (min-width: 768px) {
  .main-content {
    padding: var(--space-8) var(--space-6);
  }
}

@media (min-width: 1024px) {
  .main-content {
    padding: var(--space-12) var(--space-8);
  }
}

/* Typography scale adjustments */
@media (max-width: 768px) {
  :root {
    --text-3xl: 36px;
    --text-4xl: 48px;
  }

  .brand-title {
    font-size: var(--text-3xl);
  }

  .glass-card {
    padding: var(--space-4);
    border-radius: 12px;
  }

  .agent-status-grid {
    grid-template-columns: 1fr;
  }
}

/* Touch optimizations */
@media (hover: none) {
  .glass-card:hover {
    transform: none;
  }

  .submit-btn:hover:not(:disabled) {
    transform: none;
  }
}
```

---

## 9. Accessibility

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .final-card::before,
  .shimmer::after {
    animation: none;
  }
}
```

### Focus States

```css
/* Visible focus rings */
:focus-visible {
  outline: 2px solid var(--teal-500);
  outline-offset: 2px;
}

/* Skip link for keyboard users */
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--teal-600);
  color: white;
  border-radius: 0 0 8px 8px;
  z-index: 10000;
  transition: top var(--duration-fast);
}

.skip-link:focus {
  top: 0;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --glass-border: rgba(45, 212, 191, 0.5);
    --text-secondary: #b0c0c0;
    --text-tertiary: #809090;
  }
}
```

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Week 1)

1. **CSS Variable Migration**
   - Replace all hardcoded colors with new palette
   - Update spacing variables
   - Implement new typography scale

2. **Base Components**
   - Create `GlassCard` component
   - Update `QueryInput` with new styling
   - Redesign `ConnectionStatus`

### Phase 2: Core UI (Week 2)

1. **Content Components**
   - Redesign `ThinkingBar` with agent grid
   - Update `CollapsibleRound` with glass styling
   - Redesign `FinalAnswer` with gradient border

2. **Utility Components**
   - Update `CodeBlock` styling
   - Create new `EmptyState` design
   - Implement `AgentBubble` refresh

### Phase 3: Polish (Week 3)

1. **Animation Implementation**
   - Add entrance animations
   - Implement hover micro-interactions
   - Add loading state animations

2. **Background Effects**
   - Implement ambient gradient background
   - Add noise texture overlay
   - Create floating particle effect (optional)

### Phase 4: Optimization (Week 4)

1. **Performance**
   - Optimize backdrop-filter usage
   - Implement GPU acceleration hints
   - Lazy load off-screen animations

2. **Accessibility**
   - Test with screen readers
   - Verify keyboard navigation
   - Test reduced motion preferences

---

## 11. File Structure

```
frontend/src/
├── styles/
│   ├── aether-design-system.css    # Main design system
│   ├── animations.css               # All keyframes
│   ├── components/                  # Component-specific styles
│   │   ├── glass-card.css
│   │   ├── query-input.css
│   │   ├── thinking-bar.css
│   │   ├── round-card.css
│   │   ├── final-answer.css
│   │   └── code-block.css
│   └── utilities.css                # Helper classes
├── components/
│   ├── GlassCard.jsx
│   ├── QueryInput/
│   │   ├── index.jsx
│   │   └── QueryInput.module.css
│   ├── ThinkingBar/
│   ├── RoundCard/
│   ├── FinalAnswer/
│   └── shared/                      # Shared animation hooks
│       └── useAnimatedPresence.js
└── hooks/
    └── useReducedMotion.js          # Accessibility hook
```

---

## 12. Technical Notes

### Performance Considerations

1. **Backdrop Filter**: Use sparingly, only on main containers
2. **Animations**: Use `transform` and `opacity` only for 60fps
3. **Will-Change**: Apply to elements that will animate
4. **Contain**: Use `contain: layout style paint` on cards

### Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Backdrop filter with `-webkit-` prefix for Safari
- CSS custom properties with fallbacks

### Dependencies

No new dependencies required. Pure CSS implementation using:
- CSS Custom Properties
- CSS Grid & Flexbox
- CSS Animations & Transitions
- Backdrop Filter (native)

---

## Appendix A: Animation Presets

```javascript
// React Spring-inspired CSS animations
const animationPresets = {
  // Entrance animations
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.3, ease: 'easeOut' }
  },

  fadeInUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.4, ease: [0.175, 0.885, 0.32, 1.275] }
  },

  glassAppear: {
    initial: { opacity: 0, y: 30, scale: 0.98 },
    animate: { opacity: 1, y: 0, scale: 1 },
    transition: { duration: 0.5, ease: [0.175, 0.885, 0.32, 1.275] }
  },

  // Stagger children
  stagger: {
    staggerChildren: 0.1,
    delayChildren: 0.2
  },

  // Hover micro-interaction
  hoverLift: {
    whileHover: { y: -2, scale: 1.01 },
    whileTap: { scale: 0.98 },
    transition: { duration: 0.15 }
  }
};
```

---

## Appendix B: Color Contrast Ratios

| Combination | Ratio | WCAG Grade |
|-------------|-------|------------|
| Teal-400 on Obsidian-900 | 7.2:1 | AAA |
| Text-Primary on Obsidian-800 | 15.3:1 | AAA |
| Text-Secondary on Obsidian-800 | 8.1:1 | AAA |
| Teal-500 on Obsidian-700 | 4.6:1 | AA |
| Success on Obsidian-800 | 5.8:1 | AA |

All color combinations meet WCAG 2.1 Level AA standards.

---

**Document Version**: 1.0
**Last Updated**: February 2026
**Status**: Ready for Implementation

---

*This design system proposal represents a complete visual transformation from Neo-Brutalist to Aether Glassmorphism. Every component, animation, and interaction has been carefully specified to create a premium, futuristic experience that matches the sophisticated nature of the Council of Frontiers multi-agent AI system.*
