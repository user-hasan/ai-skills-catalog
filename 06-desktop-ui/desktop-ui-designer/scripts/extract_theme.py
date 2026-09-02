#!/usr/bin/env python3
"""
Theme Extractor for Desktop UI
Extracts colors, fonts, and design tokens from existing projects
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter


# Color patterns (hex, rgb, hsl)
HEX_PATTERN = r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'
RGB_PATTERN = r'rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)'
RGBA_PATTERN = r'rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*([0-9.]+)\)'
HSL_PATTERN = r'hsl\((\d{1,3}),\s*(\d{1,3})%,\s*(\d{1,3})%\)'


def extract_colors_from_css(content: str) -> List[str]:
    """Extract color codes from CSS content"""
    colors = []
    
    # Find all hex colors
    hex_colors = re.findall(HEX_PATTERN, content)
    colors.extend([f'#{c}' for c in hex_colors])
    
    # Find all rgb/rgba colors
    rgb_colors = re.findall(RGB_PATTERN, content)
    colors.extend([f'rgb({r},{g},{b})' for r, g, b in rgb_colors])
    
    rgba_colors = re.findall(RGBA_PATTERN, content)
    colors.extend([f'rgba({r},{g},{b},{a})' for r, g, b, a in rgba_colors])
    
    # Find all hsl colors
    hsl_colors = re.findall(HSL_PATTERN, content)
    colors.extend([f'hsl({h},{s}%,{l}%)' for h, s, l in hsl_colors])
    
    return colors


def extract_css_variables(content: str) -> Dict[str, str]:
    """Extract CSS custom properties (variables)"""
    variables = {}
    
    # Pattern for CSS variables: --name: value;
    var_pattern = r'--([a-zA-Z0-9-]+):\s*([^;]+);'
    matches = re.findall(var_pattern, content)
    
    for name, value in matches:
        variables[f'--{name}'] = value.strip()
    
    return variables


def extract_fonts(content: str) -> List[str]:
    """Extract font families from CSS content"""
    fonts = []
    
    # Pattern for font-family
    font_pattern = r'font-family:\s*([^;]+);'
    matches = re.findall(font_pattern, content)
    
    for match in matches:
        # Split by commas and clean
        for font in match.split(','):
            cleaned = font.strip().strip("'").strip('"')
            if cleaned and cleaned not in ['inherit', 'initial', 'unset']:
                fonts.append(cleaned)
    
    return fonts


def detect_color_theme(colors: List[str]) -> Dict[str, Any]:
    """Detect if theme is light or dark based on colors"""
    
    def is_dark_color(color: str) -> bool:
        """Simple check if a color is dark"""
        # Extract hex
        hex_match = re.search(HEX_PATTERN, color)
        if hex_match:
            hex_color = hex_match.group(0).lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            return luminance < 128
        
        # Check rgb
        rgb_match = re.search(RGB_PATTERN, color)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            return luminance < 128
        
        return False
    
    if not colors:
        return {'type': 'unknown', 'confidence': 0}
    
    # Sample first 20 colors
    sample_colors = colors[:20]
    dark_count = sum(1 for c in sample_colors if is_dark_color(c))
    dark_ratio = dark_count / len(sample_colors)
    
    if dark_ratio > 0.6:
        return {'type': 'dark', 'confidence': dark_ratio}
    elif dark_ratio < 0.4:
        return {'type': 'light', 'confidence': 1 - dark_ratio}
    else:
        return {'type': 'mixed', 'confidence': 0.5}


def get_primary_colors(colors: List[str], limit: int = 5) -> List[Dict[str, Any]]:
    """Get most frequent colors"""
    color_counts = Counter(colors)
    
    primary = []
    for color, count in color_counts.most_common(limit):
        primary.append({
            'color': color,
            'frequency': count,
            'usage_percentage': round(count / len(colors) * 100, 1) if colors else 0
        })
    
    return primary


def extract_theme_from_file(file_path: str) -> Dict[str, Any]:
    """Extract theme information from a single file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return {}
    
    colors = extract_colors_from_css(content)
    variables = extract_css_variables(content)
    fonts = extract_fonts(content)
    
    return {
        'file': file_path,
        'colors': colors,
        'variables': variables,
        'fonts': fonts,
        'color_count': len(colors),
        'variable_count': len(variables)
    }


def find_theme_files(project_path: str) -> List[str]:
    """Find theme-related files in project"""
    theme_files = []
    project_path = Path(project_path)
    
    # Theme file patterns
    patterns = [
        '**/*.css',
        '**/*.scss',
        '**/theme*.*',
        '**/variables*.*',
        '**/colors*.*',
        '**/tailwind.config.*',
        '**/*.theme.*'
    ]
    
    for pattern in patterns:
        for file_path in project_path.glob(pattern):
            if 'node_modules' not in str(file_path):
                theme_files.append(str(file_path))
    
    return theme_files[:30]  # Limit to 30 files


def generate_theme_summary(theme_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary of extracted theme"""
    
    all_colors = []
    all_fonts = []
    all_variables = {}
    
    for data in theme_data:
        all_colors.extend(data.get('colors', []))
        all_fonts.extend(data.get('fonts', []))
        all_variables.update(data.get('variables', {}))
    
    # Remove duplicates while preserving order
    unique_colors = list(dict.fromkeys(all_colors))
    unique_fonts = list(dict.fromkeys(all_fonts))
    
    theme_type = detect_color_theme(unique_colors)
    primary_colors = get_primary_colors(all_colors)
    
    return {
        'theme_type': theme_type,
        'total_colors_found': len(unique_colors),
        'primary_colors': primary_colors[:5],
        'fonts_used': unique_fonts[:10],
        'css_variables': all_variables,
        'variable_count': len(all_variables)
    }


def main():
    """Main function"""
    
    # Get project path
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print(f"Error: Path does not exist - {project_path}")
        return
    
    print("=" * 60)
    print("Theme Extraction Tool")
    print("=" * 60)
    print(f"Analyzing: {project_path}")
    print()
    
    # Find theme files
    theme_files = find_theme_files(project_path)
    
    if not theme_files:
        print("No theme-related files found.")
        print("Suggestions:")
        print("  - Check if the project has CSS/SCSS files")
        print("  - Look for theme configuration files")
        return
    
    print(f"Found {len(theme_files)} theme-related files")
    
    # Extract theme from each file
    theme_data = []
    for file_path in theme_files:
        data = extract_theme_from_file(file_path)
        if data and data.get('color_count', 0) > 0:
            theme_data.append(data)
    
    # Generate summary
    summary = generate_theme_summary(theme_data)
    
    # Output results
    if len(sys.argv) > 2 and sys.argv[2] == '--json':
        result = {
            'files_analyzed': len(theme_files),
            'summary': summary
        }
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 60)
        print("Extracted Theme Summary")
        print("=" * 60)
        
        print(f"\nTheme Type: {summary['theme_type']['type'].upper()}")
        print(f"Confidence: {summary['theme_type']['confidence'] * 100:.0f}%")
        
        print(f"\nPrimary Colors:")
        for color in summary['primary_colors'][:5]:
            print(f"  {color['color']} (used {color['frequency']} times, {color['usage_percentage']}%)")
        
        if summary['fonts_used']:
            print(f"\nFonts Used:")
            for font in summary['fonts_used'][:5]:
                print(f"  - {font}")
        
        if summary['css_variables']:
            print(f"\nCSS Variables Found: {summary['variable_count']}")
            # Show first 5 variables
            for var, value in list(summary['css_variables'].items())[:5]:
                print(f"  {var}: {value}")
        
        print("\n" + "=" * 60)
        
        # Provide recommendations
        print("\nRecommendations:")
        if summary['theme_type']['type'] == 'dark':
            print("  - Use light-colored text for contrast")
            print("  - Consider glassmorphism with dark backgrounds")
        elif summary['theme_type']['type'] == 'light':
            print("  - Use dark-colored text for readability")
            print("  - Semi-transparent backgrounds work well")
        
        if not summary['css_variables']:
            print("  - Consider using CSS variables for better theme management")
        
        print("=" * 60)


if __name__ == "__main__":
    main()