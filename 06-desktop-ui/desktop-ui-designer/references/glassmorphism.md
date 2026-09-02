# Glassmorphism Effect - Modern Systems

Glassmorphism is a design trend that creates a "frosted glass" effect using transparency, blur, and subtle borders.

---

## Basic Glassmorphism CSS

.glass-card {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

---

## Dark Theme Glass

.glass-card-dark {
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

---

## Glassmorphism with Gradient

.glass-card-gradient {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.2) 0%,
        rgba(255, 255, 255, 0.05) 100%
    );
    backdrop-filter: blur(12px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

---

## Interactive Glass (Hover Effect)

.glass-interactive {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.glass-interactive:hover {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

---

## Performance Optimization

### GPU Acceleration

.glass-optimized {
    backdrop-filter: blur(10px);
    will-change: transform;
    transform: translateZ(0);
}

### Avoid Overuse

- Use glass effect on 2–3 elements max per screen
- Avoid nesting glass elements (performance heavy)
- Keep blurred areas small when possible

---

## Framework-Specific Implementations

### React + TailwindCSS

<div className="bg-white/20 backdrop-blur-lg rounded-2xl border border-white/30 shadow-lg">
    {/* Content */}
</div>

### Vue + TailwindCSS

<div class="bg-white/20 backdrop-blur-lg rounded-2xl border border-white/30 shadow-lg">
    <!-- Content -->
</div>

### Qt (QML)

Rectangle {
    color: Qt.rgba(255, 255, 255, 0.2)
    radius: 16
    layer.enabled: true
    layer.effect: FastBlur {
        radius: 10
    }
    border.color: Qt.rgba(255, 255, 255, 0.3)
    border.width: 1
}

### .NET WPF (with BlurEffect)

<Border Background="#33FFFFFF" CornerRadius="16">
    <Border.Effect>
        <BlurEffect Radius="10" KernelType="Gaussian"/>
    </Border.Effect>
</Border>

---

## Color Combinations That Work Well

Background       | Glass Color               | Text Color
-----------------|---------------------------|---------------
Dark image       | rgba(0,0,0,0.4)           | White
Light image      | rgba(255,255,255,0.3)     | Dark gray
Gradient         | rgba(255,255,255,0.2)     | White
Solid dark       | rgba(255,255,255,0.1)     | Light gray
Solid light      | rgba(0,0,0,0.1)           | Dark gray

---

## Do's and Don'ts

✅ Do

- Use on cards, modals, navigation bars
- Ensure text contrast (minimum 4.5:1)
- Test on different backgrounds
- Provide fallback for non-supported browsers

❌ Don't

- Apply to small text elements
- Use on entire page background
- Nest multiple glass elements
- Forget accessibility (screen readers)

---

## Browser Support (Modern)

Browser   | Support     | Version
----------|-------------|---------
Chrome    | ✅ Full     | 76+
Firefox   | ✅ Full     | 103+
Safari    | ✅ Full     | 15+
Edge      | ✅ Full     | 79+
IE11      | ❌ None     | -