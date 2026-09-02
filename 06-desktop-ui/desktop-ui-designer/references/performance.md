# Performance Optimization for Desktop UI

Comprehensive guide for achieving 60 FPS and optimal memory usage in desktop applications.

## Core Performance Principles

### The 60 FPS Goal
- Frame budget: **16.67ms** per frame
- Keep UI thread work under **10ms** to leave room for rendering
- Aim for consistent frames, not peak speed

### Critical Metrics

| Metric | Target (Modern) | Target (Win7 32-bit) |
|--------|----------------|----------------------|
| First Paint | < 500ms | < 800ms |
| Time to Interactive | < 2s | < 3s |
| Memory (idle) | < 100MB | < 150MB |
| Memory (peak) | < 500MB | < 1.5GB |
| Frame rate | 60 FPS | 30-45 FPS |
| Bundle size | < 1MB | < 500KB |

## 1. Avoid Unnecessary Re-renders

### React - useMemo and useCallback
```jsx
// ❌ BAD - Recalculates on every render
function Component({ items }) {
    const total = items.reduce((sum, i) => sum + i.value, 0);
    return <div>{total}</div>;
}

// ✅ GOOD - Memoized calculation
function Component({ items }) {
    const total = useMemo(() => 
        items.reduce((sum, i) => sum + i.value, 0),
        [items]
    );
    return <div>{total}</div>;
}
React - React.memo
jsx
// Prevent re-renders when props haven't changed
const ExpensiveComponent = React.memo(({ data }) => {
    return <div>{/* complex UI */}</div>;
});
Vue - computed properties
vue
<script setup>
import { computed } from 'vue'

// ✅ GOOD - Cached until dependencies change
const total = computed(() => 
    items.value.reduce((sum, i) => sum + i.value, 0)
)
</script>
2. Lazy Loading
Code Splitting (React)
jsx
// Load component only when needed
const Dashboard = React.lazy(() => import('./Dashboard'));

function App() {
    return (
        <Suspense fallback={<Loading />}>
            <Dashboard />
        </Suspense>
    );
}
Route-based Lazy Loading
jsx
const routes = [
    {
        path: '/dashboard',
        component: () => import('./pages/Dashboard')
    },
    {
        path: '/settings',
        component: () => import('./pages/Settings')
    }
];
Image Lazy Loading
html
<!-- Native lazy loading -->
<img src="large-image.jpg" loading="lazy" alt="description" />

<!-- Intersection Observer -->
<img data-src="image.jpg" class="lazy" alt="description" />
javascript
// Intersection Observer implementation
const lazyImages = document.querySelectorAll('.lazy');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});
lazyImages.forEach(img => observer.observe(img));
3. Virtual Scrolling
For lists with > 100 items, use virtual scrolling.

React Virtual (react-window)
jsx
import { FixedSizeList } from 'react-window';

const VirtualList = ({ items }) => (
    <FixedSizeList
        height={600}
        itemCount={items.length}
        itemSize={50}
        width="100%"
    >
        {({ index, style }) => (
            <div style={style}>
                {items[index].name}
            </div>
        )}
    </FixedSizeList>
);
Vue Virtual (vue-virtual-scroller)
vue
<template>
    <RecycleScroller
        :items="items"
        :item-size="50"
        key-field="id"
        v-slot="{ item }"
    >
        <div>{{ item.name }}</div>
    </RecycleScroller>
</template>
4. Debouncing and Throttling
Debounce (for search input)
javascript
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Usage
const handleSearch = debounce((query) => {
    fetchResults(query);
}, 300);
Throttle (for scroll events)
javascript
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Usage
const handleScroll = throttle(() => {
    updateScrollPosition();
}, 100);
5. Memory Management
Clean Up Event Listeners
javascript
// React
useEffect(() => {
    const handleResize = () => updateSize();
    window.addEventListener('resize', handleResize);
    
    // ✅ Cleanup
    return () => window.removeEventListener('resize', handleResize);
}, []);
javascript
// Vue
onMounted(() => {
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
});
Avoid Memory Leaks in SetInterval
javascript
useEffect(() => {
    const interval = setInterval(() => {
        updateData();
    }, 1000);
    
    // ✅ Always clear intervals
    return () => clearInterval(interval);
}, []);
6. Bundle Optimization
Production Build Checklist
bash
# Analyze bundle size
npm run build -- --analyze

# Remove unused dependencies
npm prune --production

# Enable tree shaking (ensure ES modules)
Import Optimization
javascript
// ❌ BAD - Imports entire library
import _ from 'lodash';

// ✅ GOOD - Import only what you need
import debounce from 'lodash/debounce';
7. CSS Performance
Reduce Repaints and Reflows
css
/* ❌ BAD - Triggers layout reflow */
.element {
    width: 100px;
    height: 100px;
    left: 50px;
    top: 50px;
}

/* ✅ GOOD - Uses compositor only */
.element {
    transform: translateX(50px) translateY(50px);
    width: 100px;
    height: 100px;
}
Critical CSS
html
<!-- Inline critical CSS for first paint -->
<style>
    /* Critical styles here */
    .hero { background: #f0f0f0; }
    .button { padding: 10px 20px; }
</style>

<!-- Load non-critical CSS later -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
8. Windows 7 Specific Optimizations
Memory Monitoring
javascript
// Check memory usage (Electron)
if (process.getProcessMemoryInfo) {
    const memInfo = await process.getProcessMemoryInfo();
    if (memInfo.workingSetSize > 1.5 * 1024 * 1024 * 1024) {
        console.warn('Memory usage high, consider cleanup');
    }
}
Reduce Renderer Process Load
javascript
// Offload heavy work to main process
// Electron example
ipcRenderer.invoke('heavy-computation', data);
Performance Testing Tools
Tool	Purpose	Command
Lighthouse	Web performance	Chrome DevTools
React DevTools	Component renders	Browser extension
Vue DevTools	Component performance	Browser extension
Windows Performance Monitor	System resources	perfmon.msc
Chrome Task Manager	Tab memory usage	Shift+Esc
Quick Performance Checklist
markdown
### Before Launch
- [ ] Run Lighthouse performance audit (score > 90)
- [ ] Test on target hardware (especially Win7)
- [ ] Monitor memory usage for leaks
- [ ] Implement lazy loading for images
- [ ] Code split route-based components
- [ ] Debounce search/resize inputs
- [ ] Virtual scroll for large lists
- [ ] Clean up all event listeners
- [ ] Minify CSS and JS
- [ ] Enable gzip compression

### Windows 7 Specific
- [ ] Test with 2GB RAM limit
- [ ] Disable heavy GPU effects
- [ ] Use fallback animations
- [ ] Monitor CPU usage
Performance Budget Template
json
{
    "budgets": [
        {
            "resourceType": "script",
            "budget": 500
        },
        {
            "resourceType": "stylesheet",
            "budget": 100
        },
        {
            "resourceType": "total",
            "budget": 1000
        }
    ],
    "timings": {
        "firstPaint": 500,
        "interactive": 2000
    }
}
