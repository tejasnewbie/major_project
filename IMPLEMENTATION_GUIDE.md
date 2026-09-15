# Aether Design System - Quick Implementation Guide

## Overview

This guide walks you through implementing the new Aether glassmorphism design system in your Council of Frontiers application.

## Quick Start (5 Minutes)

### Step 1: Import the New Styles

In `frontend/src/index.js`, replace the existing CSS imports:

```javascript
// OLD - Remove these:
// import './styles/variables.css';
// import './App.css';

// NEW - Add this:
import './styles/aether-design-system.css';
import './App.css'; // Keep for any custom overrides
```

### Step 2: Update App.jsx Structure

Replace your App.jsx header and layout with the new structure:

```jsx
// In your return statement:
<div className="app">
  {/* Connection Status */}
  <div className={`connection-status`}>
    <div className={`status-pill status-pill--${isConnected ? 'connected' : 'disconnected'}`}>
      <span className="status-dot"></span>
      <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
    </div>
  </div>

  {/* Header */}
  <header className={`header ${hasStarted ? 'header--compact' : ''}`}>
    <h1 className="brand-title">
      Council<span className="brand-title-accent">.</span>
    </h1>
    {!hasStarted && (
      <p className="brand-subtitle">
        Multi-agent verification through collaborative debate
      </p>
    )}
    {category && (
      <div className="category-badge">
        <span>◈</span>
        {category}
      </div>
    )}
  </header>

  {/* Main Content */}
  <main className="main-content">
    {/* Your existing components */}
  </main>
</div>
```

## Component Migration

### 1. QueryInput Component

Replace your QueryInput.jsx:

```jsx
import React, { useState, useRef, useEffect } from 'react';

const QueryInput = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [query]);

  return (
    <div className="query-container">
      <form onSubmit={handleSubmit} className="query-input-wrapper">
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter your query here..."
          className="query-input"
          rows={1}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="submit-btn"
          disabled={!query.trim() || isLoading}
        >
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default QueryInput;
```

**Delete QueryInput.css** - styles are now in the design system.

### 2. ThinkingBar Component

Update ThinkingBar.jsx with new glass styling:

```jsx
import React from 'react';

const ThinkingBar = ({ stage, message, agents, progress }) => {
  const getStageLabel = () => {
    const labels = {
      classification: 'Analyzing Input',
      round1_start: 'Generating Responses',
      round1_progress: 'Generating Responses',
      evaluation: 'Scoring Outputs',
      execution: 'Executing Code',
      winner_selected: 'Refining Answer',
      refinement_start: 'Refining Answer',
      refinement_progress: 'Refining Answer',
      synthesis_start: 'Synthesizing Final Answer',
      complete: 'Process Complete'
    };
    return labels[stage] || 'Processing';
  };

  return (
    <div className="thinking-panel animate-glass">
      {/* Header */}
      <div className="thinking-header">
        <div className="thinking-stage">
          <div className="stage-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5" />
            </svg>
          </div>
          <span className="stage-label">{getStageLabel()}</span>
        </div>
        <span className="thinking-timer">{progress || 0}s</span>
      </div>

      {/* Progress Bar */}
      <div className="progress-track">
        <div className="progress-fill" style={{ width: '100%' }} />
      </div>

      {/* Message */}
      {message && (
        <div style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-secondary)' }}>
          {message}
        </div>
      )}

      {/* Agent Status Grid */}
      {agents && agents.length > 0 && (
        <div className="agent-status-grid">
          {agents.map((agent, i) => (
            <div
              key={i}
              className={`agent-status ${agent.done ? 'agent-status--done' : agent.active ? 'agent-status--active' : ''}`}
            >
              <div className="agent-status-avatar">
                {agent.name.charAt(0)}
              </div>
              <div className="agent-status-info">
                <div className="agent-status-name">{agent.name}</div>
                <div className="agent-status-state">
                  {agent.done ? 'Complete' : agent.active ? 'Working...' : 'Waiting'}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThinkingBar;
```

**Delete ThinkingBar.css** - styles are in the design system.

### 3. Empty State

Add the empty state to your App.jsx when no query is active:

```jsx
{!hasStarted && (
  <div className="empty-state">
    <div className="empty-icon">◈</div>
    <h2 className="empty-title">What would you like to solve?</h2>
    <p className="empty-description">
      The Council brings together multiple AI models to debate and refine solutions.
    </p>
  </div>
)}
```

### 4. Glass Card Wrapper

For any content sections, wrap them in glass cards:

```jsx
// Instead of:
<div className="rounds-container">
  <CollapsibleRound ... />
</div>

// Use:
<div className="glass-card">
  <CollapsibleRound ... />
</div>

// Or for active states:
<div className={`glass-card ${isActive ? 'glass-card--active' : ''}`}>
  ...
</div>
```

## Animation Hooks

### Optional: useAnimatedPresence Hook

Create `frontend/src/hooks/useAnimatedPresence.js`:

```javascript
import { useEffect, useState } from 'react';

export const useAnimatedPresence = (isPresent, duration = 300) => {
  const [isVisible, setIsVisible] = useState(isPresent);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isPresent) {
      setIsVisible(true);
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), duration);
      return () => clearTimeout(timer);
    } else {
      setIsAnimating(true);
      const timer = setTimeout(() => {
        setIsVisible(false);
        setIsAnimating(false);
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [isPresent, duration]);

  return { isVisible, isAnimating };
};
```

### Optional: useReducedMotion Hook

Create `frontend/src/hooks/useReducedMotion.js`:

```javascript
import { useEffect, useState } from 'react';

export const useReducedMotion = () => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);

    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
};
```

## Gradual Migration Strategy

If you want to migrate gradually instead of all at once:

### Phase 1: Foundation (Day 1)
1. Import `aether-design-system.css` alongside existing styles
2. Update the App container and header only
3. Keep existing component styles

### Phase 2: Key Components (Day 2-3)
1. Migrate QueryInput
2. Migrate ThinkingBar
3. Migrate FinalAnswer

### Phase 3: Remaining Components (Day 4-5)
1. Migrate CollapsibleRound
2. Migrate AgentBubble
3. Migrate CodeBlock

### Phase 4: Cleanup (Day 6)
1. Remove old CSS files
2. Consolidate any remaining custom styles
3. Test all interactions

## Troubleshooting

### Issue: Backdrop blur not working
**Solution**: Check that the element has a semi-transparent background. Blur only works on elements with `background` that has alpha < 1.

### Issue: Animations feel sluggish
**Solution**:
- Check for `layout` property animations (width, height, top, left)
- Use only `transform` and `opacity` for animations
- Add `will-change: transform` to animated elements

### Issue: Text hard to read on glass cards
**Solution**:
- Increase backdrop blur: `--glass-blur: 30px`
- Darken glass background: `--glass-bg: rgba(10, 17, 17, 0.8)`
- Add text shadow: `text-shadow: 0 1px 2px rgba(0,0,0,0.5)`

### Issue: Gradient border not showing
**Solution**: Ensure the parent has `position: relative` and the pseudo-element has proper `z-index`.

## Customization

### Changing Accent Color

Edit the CSS variables at the top of `aether-design-system.css`:

```css
:root {
  /* Change teal to purple for example */
  --teal-400: #c084fc;
  --teal-500: #a855f7;
  --teal-600: #9333ea;
  /* etc... */
}
```

### Adjusting Animation Speed

```css
:root {
  --duration-fast: 100ms;  /* Faster */
  --duration-slow: 500ms;  /* Slower */
}
```

### Glass Effect Intensity

```css
:root {
  --glass-blur: 10px;        /* Less blur */
  --glass-bg: rgba(17, 26, 26, 0.9);  /* More opaque */
}
```

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | Full |
| Firefox | 88+ | Full |
| Safari | 14+ | Full (with -webkit-) |
| Edge | 90+ | Full |

For older browsers, the design gracefully degrades to solid backgrounds without blur effects.

## Next Steps

1. Try the quick start steps above
2. Review the full proposal document for advanced features
3. Customize colors to match your brand
4. Add your own component variations
5. Test on various devices and screen sizes

## Need Help?

Refer to the full proposal document: `NEW_DESIGN_SYSTEM_PROPOSAL.md`

Key sections:
- Section 6: Complete component specifications
- Section 10: Implementation roadmap
- Appendix A: Animation presets
- Appendix B: Color contrast ratios (accessibility)
