# Smooth Animations for Desktop UI

Animation guidelines and ready-to-use code for modern desktop interfaces.

## Performance Principles

### Always Use GPU-Accelerated Properties
```css
/* ✅ GOOD - GPU accelerated */
.element {
    transform: translateX(100px);
    opacity: 0.5;
}

/* ❌ BAD - Causes repaint */
.element {
    left: 100px;
    top: 50px;
}
 Use will-change Sparingly
css
.element {
    will-change: transform, opacity;
}
/* Remove after animation */
.element.animated {
    will-change: auto;
}
Fade Animations
Fade In
css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}
Fade Out
css
@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}

.fade-out {
    animation: fadeOut 0.3s ease-in-out;
}
Fade In Up
css
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

.fade-in-up {
    animation: fadeInUp 0.4s ease-out;
}
Slide Animations
Slide In Left
css
@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.slide-left {
    animation: slideInLeft 0.3s ease-out;
}
Slide In Right
css
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.slide-right {
    animation: slideInRight 0.3s ease-out;
}
Scale Animations
Scale In (Modal/Popup)
css
@keyframes scaleIn {
    from {
        transform: scale(0.9);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

.modal-enter {
    animation: scaleIn 0.2s cubic-bezier(0.34, 1.2, 0.64, 1);
}
Hover Scale
css
.button-hover {
    transition: transform 0.2s ease;
}

.button-hover:hover {
    transform: scale(1.05);
}
Page Transitions
Crossfade
css
.page-enter {
    animation: fadeIn 0.3s ease;
}

.page-exit {
    animation: fadeOut 0.2s ease;
}
Slide + Fade
css
.page-transition {
    animation: fadeInUp 0.4s ease-out;
}
Skeleton Loading Animation
css
@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

.skeleton {
    background: linear-gradient(
        90deg,
        #f0f0f0 25%,
        #e0e0e0 50%,
        #f0f0f0 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
}
Notification/Toast Animation
css
@keyframes slideInNotification {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOutNotification {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

.notification-enter {
    animation: slideInNotification 0.3s ease-out;
}

.notification-exit {
    animation: slideOutNotification 0.3s ease-in;
}
List Item Stagger Animation
css
.list-item {
    opacity: 0;
    transform: translateX(-20px);
    animation: slideInLeft 0.3s ease forwards;
}

/* Stagger children */
.list-item:nth-child(1) { animation-delay: 0.05s; }
.list-item:nth-child(2) { animation-delay: 0.10s; }
.list-item:nth-child(3) { animation-delay: 0.15s; }
.list-item:nth-child(4) { animation-delay: 0.20s; }
.list-item:nth-child(5) { animation-delay: 0.25s; }
React Implementation Examples
With Framer Motion
jsx
import { motion, AnimatePresence } from 'framer-motion';

const FadeIn = ({ children }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
    >
        {children}
    </motion.div>
);
With CSS Modules
jsx
import styles from './Component.module.css';

const Component = ({ show }) => (
    <div className={show ? styles.fadeIn : styles.fadeOut}>
        Content
    </div>
);
Vue Implementation Examples
With Vue Transitions
vue
<template>
    <transition name="fade">
        <div v-if="show">Content</div>
    </transition>
</template>

<style>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>
Windows 7 Performance Notes
Animation Type	Performance on Win7	Recommendation
opacity	✅ Excellent	Use freely
transform	✅ Good	Use for slide/scale
width/height	⚠️ Moderate	Avoid when possible
box-shadow	⚠️ Moderate	Use sparingly
backdrop-filter	❌ Not supported	Use fallback
Win7 Optimized Animation
css
/* Use these properties for best Win7 performance */
.win7-animation {
    transition: transform 0.2s ease, opacity 0.2s ease;
    /* Avoid transitions on width, height, left, top */
}
Animation Duration Guidelines
Interaction	Duration	Easing
Micro-interaction (hover)	0.1-0.2s	ease
Component show/hide	0.2-0.3s	ease-out
Page transition	0.3-0.4s	ease-in-out
Modal open/close	0.2-0.3s	cubic-bezier
Loading skeleton	1.5s	infinite linear
Quick Reference
css
/* Most common animation combo */
.animate-enter {
    animation: fadeInUp 0.3s ease-out;
}

/* Most common exit */
.animate-exit {
    animation: fadeOut 0.2s ease-in;
}

/* Most common hover */
.hover-lift {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}