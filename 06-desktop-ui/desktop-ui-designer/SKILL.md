---
name: desktop-ui-designer
description: Advanced desktop UI design and development with modern aesthetics, glassmorphism effects, smooth animations, and exceptional performance. Automatically detects project framework, OS capabilities (including Windows 7 32-bit), and existing themes. Use when user wants to: (1) redesign/improve existing desktop application UI, (2) create modern UI with animations and glass effects, (3) apply latest themes, (4) optimize UI performance, or any desktop interface design task.
---

# Desktop UI Designer

This skill provides guidance for creating modern, high-performance desktop application interfaces with glassmorphism effects, smooth animations, and adaptive design based on target OS capabilities.

## When This Skill Is Active

This skill activates when working on desktop application UI tasks. It automatically:
- Detects the current project framework (React, Vue, Qt, .NET, etc.)
- Detects target OS and its capabilities (especially Windows 7 32-bit limitations)
- Extracts existing theme and color scheme
- Chooses appropriate design system based on project context

## Core Workflow

### Step 1: Analyze Environment
Run detection scripts to understand the project context:
- Framework detection
- OS capability detection
- Existing theme extraction

### Step 2: Choose Appropriate Patterns
Based on detected OS:
- **Windows 7 32-bit**: Use fallback patterns (no backdrop-filter, limited animations)
- **Modern OS**: Use full modern effects (glassmorphism, advanced animations)

### Step 3: Apply Design
Implement UI with selected patterns, ensuring performance optimization.

## Bundled Resources

### Scripts
- `detect_os_capabilities.py` - Detect OS and its UI capabilities
- `analyze_project_structure.py` - Analyze existing project structure
- `extract_theme.py` - Extract current theme from project
- `performance_audit.py` - Audit UI performance

### References
- `windows7_32bit_limits.md` - Windows 7 32-bit limitations and solutions
- `glassmorphism.md` - Glass effect implementation
- `glassmorphism_fallback.md` - Fallback for older systems
- `animations.md` - Smooth animation patterns
- `performance.md` - Performance optimization techniques
- `accessibility.md` - Accessibility guidelines
- `fallback_patterns.md` - Fallback patterns for limited systems

### Assets
- `animation_templates/` - Ready-to-use animation CSS/JS
- `glass_bg_templates/` - Glass background templates (modern + fallback)
- `win7_compatible/` - Windows 7 compatible boilerplates

## Performance Requirements

Always ensure:
- No unnecessary re-renders
- Lazy loading for heavy components
- Memory optimization for Windows 7 32-bit (<2GB RAM usage)