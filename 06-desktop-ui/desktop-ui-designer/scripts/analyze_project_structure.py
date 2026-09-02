#!/usr/bin/env python3
"""
Project Structure Analyzer for Desktop UI
Analyzes project structure, detects framework, and identifies UI components
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def detect_framework(project_path: str) -> Dict[str, Any]:
    """Detect the UI framework being used in the project"""
    
    frameworks = {
        'react': {
            'indicators': ['package.json', 'react', 'react-dom', 'jsx'],
            'files': ['package.json', 'src/App.jsx', 'src/App.tsx', 'src/main.jsx'],
            'config_files': ['vite.config.js', 'webpack.config.js', 'next.config.js']
        },
        'vue': {
            'indicators': ['package.json', 'vue', '.vue'],
            'files': ['package.json', 'src/App.vue', 'src/main.js'],
            'config_files': ['vite.config.js', 'vue.config.js']
        },
        'angular': {
            'indicators': ['package.json', '@angular/core', '.ts'],
            'files': ['package.json', 'angular.json', 'src/app/app.component.ts'],
            'config_files': ['angular.json']
        },
        'qt': {
            'indicators': ['.pro', '.qml', 'CMakeLists.txt'],
            'files': ['CMakeLists.txt', '*.pro', 'main.qml'],
            'config_files': ['CMakeLists.txt', '*.pro']
        },
        'dotnet': {
            'indicators': ['.csproj', '.sln', 'WPF', 'WinForms'],
            'files': ['*.csproj', '*.sln', 'App.xaml', 'MainWindow.xaml'],
            'config_files': ['app.config', 'App.config']
        },
        'electron': {
            'indicators': ['package.json', 'electron', 'main.js'],
            'files': ['package.json', 'main.js', 'preload.js'],
            'config_files': ['package.json', 'electron-builder.json']
        },
        'tauri': {
            'indicators': ['package.json', '@tauri-apps', 'tauri.conf.json'],
            'files': ['tauri.conf.json', 'src-tauri/Cargo.toml'],
            'config_files': ['tauri.conf.json']
        }
    }
    
    detected = []
    project_path = Path(project_path)
    
    for framework, info in frameworks.items():
        score = 0
        
        # Check for indicator files
        for file_pattern in info['files']:
            if '*' in file_pattern:
                if list(project_path.glob(file_pattern)):
                    score += 3
            elif (project_path / file_pattern).exists():
                score += 3
        
        # Check package.json dependencies if exists
        package_json = project_path / 'package.json'
        if package_json.exists():
            try:
                import json as json_lib
                with open(package_json) as f:
                    pkg = json_lib.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    
                    for indicator in info['indicators']:
                        if indicator in deps or indicator in str(deps):
                            score += 2
            except:
                pass
        
        # Check config files
        for config in info['config_files']:
            if (project_path / config).exists():
                score += 1
        
        if score > 0:
            detected.append({
                'framework': framework,
                'confidence': min(score / 10, 1.0),
                'score': score
            })
    
    # Sort by confidence
    detected.sort(key=lambda x: x['confidence'], reverse=True)
    
    if detected and detected[0]['confidence'] > 0.3:
        return detected[0]
    else:
        return {'framework': 'unknown', 'confidence': 0, 'score': 0}


def find_ui_components(project_path: str, framework: str) -> List[Dict[str, Any]]:
    """Find UI components in the project"""
    
    components = []
    project_path = Path(project_path)
    
    # Patterns for different frameworks
    patterns = {
        'react': ['*.jsx', '*.tsx', 'src/**/*.jsx', 'src/**/*.tsx'],
        'vue': ['*.vue', 'src/**/*.vue'],
        'angular': ['*.component.ts', '*.component.html', 'src/**/*.component.ts'],
        'qt': ['*.qml', '*.ui', '*.qml', '**/*.qml'],
        'dotnet': ['*.xaml', '*.xaml.cs', '**/*.xaml'],
        'electron': ['*.html', '*.css', 'renderer/**/*.js'],
        'tauri': ['*.html', '*.css', 'src/**/*.jsx', 'src/**/*.vue']
    }
    
    # Get patterns for detected framework or use common ones
    search_patterns = patterns.get(framework, ['*.html', '*.css', '*.js', '*.jsx', '*.vue', '*.qml', '*.xaml'])
    
    for pattern in search_patterns:
        for file_path in project_path.glob(f"**/{pattern}"):
            if 'node_modules' not in str(file_path) and '.git' not in str(file_path):
                components.append({
                    'path': str(file_path),
                    'name': file_path.stem,
                    'type': file_path.suffix[1:],
                    'size_kb': file_path.stat().st_size / 1024
                })
    
    return components[:50]  # Limit to 50 components


def find_stylesheets(project_path: str) -> List[Dict[str, Any]]:
    """Find CSS/stylesheet files in the project"""
    
    stylesheets = []
    project_path = Path(project_path)
    
    style_patterns = ['*.css', '*.scss', '*.sass', '*.less', '*.styled.js', '*.module.css']
    
    for pattern in style_patterns:
        for file_path in project_path.glob(f"**/{pattern}"):
            if 'node_modules' not in str(file_path):
                stylesheets.append({
                    'path': str(file_path),
                    'name': file_path.stem,
                    'type': pattern,
                    'size_kb': file_path.stat().st_size / 1024
                })
    
    return stylesheets[:30]


def analyze_project(project_path: str) -> Dict[str, Any]:
    """Main analysis function"""
    
    if not os.path.exists(project_path):
        return {'error': f'Path does not exist: {project_path}'}
    
    # Detect framework
    framework_info = detect_framework(project_path)
    
    # Find components
    components = find_ui_components(project_path, framework_info['framework'])
    
    # Find stylesheets
    stylesheets = find_stylesheets(project_path)
    
    # Calculate project stats
    total_files = 0
    total_size_kb = 0
    for root, dirs, files in os.walk(project_path):
        if 'node_modules' not in root and '.git' not in root:
            total_files += len(files)
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    total_size_kb += os.path.getsize(file_path) / 1024
                except:
                    pass
    
    result = {
        'project_path': str(project_path),
        'detected_framework': framework_info,
        'components': {
            'total': len(components),
            'list': components[:20]  # First 20 components
        },
        'stylesheets': {
            'total': len(stylesheets),
            'list': stylesheets[:15]  # First 15 stylesheets
        },
        'statistics': {
            'total_files': total_files,
            'total_size_mb': round(total_size_kb / 1024, 2),
            'ui_components_count': len(components),
            'stylesheets_count': len(stylesheets)
        }
    }
    
    return result


def main():
    """Main function"""
    
    # Get project path from argument or use current directory
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = os.getcwd()
    
    # Analyze
    result = analyze_project(project_path)
    
    # Output
    if len(sys.argv) > 2 and sys.argv[2] == '--json':
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print("Project Structure Analysis")
        print("=" * 60)
        print(f"Project Path: {result['project_path']}")
        print(f"\nDetected Framework: {result['detected_framework']['framework']}")
        print(f"Confidence: {result['detected_framework']['confidence'] * 100:.0f}%")
        print(f"\nStatistics:")
        print(f"  Total Files: {result['statistics']['total_files']}")
        print(f"  Total Size: {result['statistics']['total_size_mb']} MB")
        print(f"  UI Components: {result['statistics']['ui_components_count']}")
        print(f"  Stylesheets: {result['statistics']['stylesheets_count']}")
        
        if result['components']['list']:
            print(f"\nSample Components (first {len(result['components']['list'])}):")
            for comp in result['components']['list'][:5]:
                print(f"  - {comp['name']}.{comp['type']} ({comp['size_kb']:.1f} KB)")
        
        if result['stylesheets']['list']:
            print(f"\nStylesheets Found ({len(result['stylesheets']['list'])}):")
            for sheet in result['stylesheets']['list'][:5]:
                print(f"  - {sheet['name']}.{sheet['type']} ({sheet['size_kb']:.1f} KB)")
        
        print("=" * 60)
    
    return result


if __name__ == "__main__":
    main()