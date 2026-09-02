# Accessibility (a11y) for Desktop UI

Guidelines for creating inclusive desktop interfaces that work for everyone, including users with disabilities.

## Core Standards (WCAG 2.1)

### Compliance Levels

| Level | Description | Target |
|-------|-------------|--------|
| **A** | Essential accessibility | Minimum requirement |
| **AA** | Standard compliance | ✅ **Target for this skill** |
| **AAA** | Enhanced accessibility | Optional for specialized apps |

## 1. Color Contrast

### Minimum Contrast Ratios (WCAG AA)

| Element | Contrast Ratio | Example |
|---------|---------------|---------|
| Normal text | 4.5:1 | Body text, labels |
| Large text (18pt+) | 3:1 | Headings |
| UI components | 3:1 | Buttons, borders |
| Icons | 3:1 | Action icons |

### Testing Colors
```css
/* ✅ GOOD - Passes AA */
.text-light-on-dark {
    color: #FFFFFF;      /* White */
    background: #2C3E50; /* Dark blue */
    /* Contrast: 9.5:1 */
}

/* ❌ BAD - Fails AA */
.text-light-on-light {
    color: #CCCCCC;      /* Light gray */
    background: #FFFFFF; /* White */
    /* Contrast: 1.5:1 */
}
Quick Contrast Check Formula
javascript
function getContrastRatio(color1, color2) {
    const lum1 = getLuminance(color1);
    const lum2 = getLuminance(color2);
    const brightest = Math.max(lum1, lum2);
    const darkest = Math.min(lum1, lum2);
    return (brightest + 0.05) / (darkest + 0.05);
}
// Passes AA if ratio >= 4.5 for text
2. Keyboard Navigation
Required Keyboard Interactions
Key	Action	When
Tab	Move forward	Interactive elements
Shift+Tab	Move backward	Interactive elements
Enter / Space	Activate	Buttons, links
Arrow keys	Navigate	Menus, lists, sliders
Escape	Close	Modals, dropdowns
Home / End	First/last	Lists, tables
Focus Management
html
<!-- ✅ Always show focus indicator -->
<button class="btn">
    Click me
</button>

<style>
/* Never do this */
.btn:focus {
    outline: none; /* ❌ BAD */
}

/* ✅ Better focus style */
.btn:focus-visible {
    outline: 2px solid #0066CC;
    outline-offset: 2px;
}
</style>
Skip Navigation Link
html
<!-- Allows keyboard users to skip to main content -->
<a href="#main-content" class="skip-link">
    Skip to main content
</a>

<style>
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
}
.skip-link:focus {
    top: 0;
}
</style>
3. Screen Reader Support
ARIA Labels
html
<!-- Icon-only button needs label -->
<button aria-label="Close dialog">
    <svg>...</svg>
</button>

<!-- Describe complex elements -->
<div role="region" aria-label="User profile section">
    <!-- content -->
</div>

<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
    {{ notificationMessage }}
</div>
Semantic HTML (Better than ARIA)
html
<!-- ✅ GOOD - Semantic -->
<nav>
    <ul>
        <li><a href="/">Home</a></li>
    </ul>
</nav>

<!-- ❌ BAD - Needs ARIA -->
<div class="nav">
    <div class="nav-item" role="link">Home</div>
</div>
Role Attributes
html
<!-- Common roles -->
<button>Already semantic</button>
<div role="button" tabindex="0">Needs role</div>
<div role="alert">Important message</div>
<div role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
4. Focus Order Management
Modal Dialog Focus Trap
javascript
function trapFocus(element) {
    const focusable = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusable[0];
    const lastFocusable = focusable[focusable.length - 1];
    
    element.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                lastFocusable.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                firstFocusable.focus();
                e.preventDefault();
            }
        }
    });
    
    firstFocusable.focus();
}
5. Windows 7 Accessibility
High Contrast Mode Detection
javascript
// Detect Windows High Contrast Mode
const isHighContrast = window.matchMedia('(forced-colors: active)').matches;

if (isHighContrast) {
    document.body.classList.add('high-contrast');
}
css
/* High contrast friendly styles */
@media (forced-colors: active) {
    .card {
        border: 2px solid CanvasText;
        background: Canvas;
    }
    .button {
        border: 2px solid ButtonText;
        background: ButtonFace;
    }
}
Magnifier Considerations
css
/* Ensure text is readable when magnified */
.text {
    font-size: 1rem; /* Use rem, not px */
    line-height: 1.5;
    max-width: 80ch; /* Readable line length */
}
6. Framework-Specific Implementation
React
jsx
// Focus management with useRef
const modalRef = useRef(null);

useEffect(() => {
    if (isOpen) {
        modalRef.current?.focus();
    }
}, [isOpen]);

return (
    <div 
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
    >
        <h2 id="dialog-title">Modal Title</h2>
    </div>
);
Vue
vue
<template>
    <div 
        ref="modal"
        role="dialog"
        aria-modal="true"
        :aria-label="title"
    >
        <h2>{{ title }}</h2>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const modal = ref(null)

watch(() => isOpen, (open) => {
    if (open) {
        modal.value?.focus()
    }
})
</script>
7. Accessibility Testing Checklist
markdown
### Keyboard Testing
- [ ] Can navigate all interactive elements with Tab
- [ ] Focus indicator is clearly visible
- [ ] Can close modals with Escape
- [ ] Dropdowns work with arrow keys
- [ ] No keyboard traps

### Screen Reader Testing (NVDA on Windows)
- [ ] All images have alt text
- [ ] Form fields have associated labels
- [ ] ARIA labels are announced correctly
- [ ] Dynamic content updates are announced
- [ ] Page structure is logical

### Visual Testing
- [ ] Color contrast meets AA standards
- [ ] Information not conveyed only by color
- [ ] Text resizes without breaking layout
- [ ] High contrast mode support
- [ ] Focus order follows visual order

### Windows 7 Specific
- [ ] Works with built-in Magnifier
- [ ] High Contrast mode support
- [ ] Screen reader (NVDA) compatibility
8. Common ARIA Patterns
Accordion
html
<div class="accordion">
    <button 
        aria-expanded="false"
        aria-controls="section1"
        id="accordion1"
    >
        Section Title
    </button>
    <div 
        id="section1"
        role="region"
        aria-labelledby="accordion1"
        hidden
    >
        Content here
    </div>
</div>
Tab Panel
html
<div role="tablist" aria-label="Sample Tabs">
    <button role="tab" aria-selected="true" aria-controls="panel1" id="tab1">
        Tab 1
    </button>
    <button role="tab" aria-selected="false" aria-controls="panel2" id="tab2">
        Tab 2
    </button>
</div>
<div role="tabpanel" aria-labelledby="tab1" id="panel1">
    Panel 1 content
</div>
Quick Reference
html
<!-- Essential accessibility attributes -->
<img alt="Description of image">
<label for="inputId">Form label</label>
<button aria-label="Icon button description">
<main id="main-content">
<nav aria-label="Main navigation">
<div role="alert" aria-live="assertive">
<table aria-label="Data table description">
