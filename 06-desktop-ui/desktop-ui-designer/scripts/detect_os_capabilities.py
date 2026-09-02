#!/usr/bin/env python3
"""
OS Capability Detection for Desktop UI
Detects operating system, version, and UI capabilities
Supports Windows, Linux, macOS
"""

import sys
import platform
import subprocess
import json
from typing import Dict, Any


def detect_windows_version() -> Dict[str, Any]:
    """Detect Windows version and capabilities"""
    version = platform.version()
    release = platform.release()
    
    # Windows version mapping
    version_map = {
        '10.0': {'name': 'Windows 10/11', 'modern': True, 'glass_support': True},
        '6.3': {'name': 'Windows 8.1', 'modern': False, 'glass_support': False},
        '6.2': {'name': 'Windows 8', 'modern': False, 'glass_support': False},
        '6.1': {'name': 'Windows 7', 'modern': False, 'glass_support': False},
        '6.0': {'name': 'Windows Vista', 'modern': False, 'glass_support': False},
    }
    
    # Get major.minor version
    version_parts = version.split('.')
    major_minor = f"{version_parts[0]}.{version_parts[1]}" if len(version_parts) > 1 else version
    
    info = version_map.get(major_minor, {
        'name': f'Windows {release}',
        'modern': True,
        'glass_support': True
    })
    
    # Check for 32-bit
    is_32bit = platform.machine().endswith('32') or sys.maxsize <= 2**32
    architecture = '32-bit' if is_32bit else '64-bit'
    
    # Memory limit for 32-bit
    memory_limit_mb = 2048 if is_32bit else None  # 2GB for 32-bit
    
    return {
        'os': 'windows',
        'name': info['name'],
        'version': release,
        'architecture': architecture,
        'is_32bit': is_32bit,
        'memory_limit_mb': memory_limit_mb,
        'glass_support': info['glass_support'],
        'modern_os': info['modern']
    }


def detect_linux_capabilities() -> Dict[str, Any]:
    """Detect Linux distribution and capabilities"""
    try:
        # Try to get distribution info
        with open('/etc/os-release', 'r') as f:
            content = f.read()
        
        distro = 'Unknown'
        for line in content.splitlines():
            if line.startswith('NAME='):
                distro = line.split('=', 1)[1].strip('"')
                break
    except FileNotFoundError:
        distro = platform.system()
    
    return {
        'os': 'linux',
        'name': distro,
        'version': platform.release(),
        'architecture': platform.machine(),
        'is_32bit': platform.machine().endswith('32'),
        'glass_support': True,  # Modern Linux supports glass effects
        'modern_os': True
    }


def detect_macos_capabilities() -> Dict[str, Any]:
    """Detect macOS version and capabilities"""
    version = platform.mac_ver()[0]
    version_parts = version.split('.')
    major_version = int(version_parts[0]) if version_parts else 0
    
    # Glass support from macOS Big Sur (11.0) and later
    glass_support = major_version >= 11
    
    return {
        'os': 'darwin',
        'name': f'macOS {version}',
        'version': version,
        'architecture': platform.machine(),
        'is_32bit': False,  # macOS hasn't supported 32-bit since Catalina
        'glass_support': glass_support,
        'modern_os': major_version >= 10  # 10.15+ is modern enough
    }


def get_recommended_ui_mode(capabilities: Dict[str, Any]) -> Dict[str, Any]:
    """Get recommended UI mode based on capabilities"""
    
    # Windows 7 32-bit specific
    if (capabilities['os'] == 'windows' and 
        capabilities['name'] == 'Windows 7' and 
        capabilities['is_32bit']):
        return {
            'mode': 'legacy',
            'glass_effect': 'fallback',
            'animations': 'simple',
            'layout': 'flexbox',
            'performance': 'conservative'
        }
    
    # Other older Windows
    if capabilities['os'] == 'windows' and not capabilities['modern_os']:
        return {
            'mode': 'compatibility',
            'glass_effect': 'fallback',
            'animations': 'simple',
            'layout': 'flexbox',
            'performance': 'balanced'
        }
    
    # Modern systems
    if capabilities['glass_support']:
        return {
            'mode': 'modern',
            'glass_effect': 'full',
            'animations': 'full',
            'layout': 'grid',
            'performance': 'optimal'
        }
    
    # Default fallback
    return {
        'mode': 'standard',
        'glass_effect': 'fallback',
        'animations': 'moderate',
        'layout': 'flexbox',
        'performance': 'balanced'
    }


def main():
    """Main detection function"""
    system = platform.system().lower()
    
    if system == 'windows':
        capabilities = detect_windows_version()
    elif system == 'linux':
        capabilities = detect_linux_capabilities()
    elif system == 'darwin':
        capabilities = detect_macos_capabilities()
    else:
        capabilities = {
            'os': system,
            'name': platform.system(),
            'version': platform.release(),
            'architecture': platform.machine(),
            'is_32bit': False,
            'glass_support': True,
            'modern_os': True
        }
    
    # Add UI recommendations
    capabilities['recommended_ui'] = get_recommended_ui_mode(capabilities)
    
    # Output as JSON
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(capabilities, indent=2))
    else:
        print("=" * 50)
        print("OS Capability Detection Results")
        print("=" * 50)
        print(f"Operating System: {capabilities['name']}")
        print(f"Architecture: {capabilities['architecture']}")
        print(f"Glass Effect Support: {'Yes' if capabilities['glass_support'] else 'No'}")
        print(f"Modern OS: {'Yes' if capabilities['modern_os'] else 'No'}")
        if capabilities.get('memory_limit_mb'):
            print(f"Memory Limit: {capabilities['memory_limit_mb']} MB")
        print("\nRecommended UI Mode:")
        for key, value in capabilities['recommended_ui'].items():
            print(f"  {key}: {value}")
        print("=" * 50)
    
    return capabilities


if __name__ == "__main__":
    main()