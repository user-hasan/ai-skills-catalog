#!/usr/bin/env python3
"""
Performance Audit Tool for Desktop UI
Audits UI performance and provides optimization recommendations
"""

import os
import sys
import json
import time
import psutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class PerformanceAudit:
    """Main performance audit class"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results = {
            'bundle_analysis': {},
            'memory_analysis': {},
            'performance_scores': {},
            'recommendations': [],
            'issues_found': []
        }
    
    def analyze_bundle_size(self) -> Dict[str, Any]:
        """Analyze bundle/package sizes"""
        
        bundle_info = {
            'total_size_mb': 0,
            'largest_files': [],
            'file_count': 0,
            'warnings': []
        }
        
        # Patterns to analyze
        patterns = [
            '**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx',
            '**/*.css', '**/*.scss', '**/*.html',
            '**/dist/**/*', '**/build/**/*', '**/out/**/*'
        ]
        
        file_sizes = []
        
        for pattern in patterns:
            for file_path in self.project_path.glob(pattern):
                if 'node_modules' not in str(file_path):
                    try:
                        size_bytes = file_path.stat().st_size
                        size_mb = size_bytes / (1024 * 1024)
                        file_sizes.append({
                            'path': str(file_path),
                            'size_mb': size_mb,
                            'size_bytes': size_bytes
                        })
                        bundle_info['total_size_mb'] += size_mb
                        bundle_info['file_count'] += 1
                    except:
                        pass
        
        # Sort by size and get largest files
        file_sizes.sort(key=lambda x: x['size_mb'], reverse=True)
        bundle_info['largest_files'] = file_sizes[:10]
        
        # Check for warnings
        if bundle_info['total_size_mb'] > 5:
            bundle_info['warnings'].append(f"Total bundle size is {bundle_info['total_size_mb']:.2f} MB (recommended < 5MB)")
        
        for file in bundle_info['largest_files'][:3]:
            if file['size_mb'] > 1:
                bundle_info['warnings'].append(f"Large file: {Path(file['path']).name} ({file['size_mb']:.2f} MB)")
        
        # Check for source maps in production
        source_maps = list(self.project_path.glob('**/*.map'))
        if source_maps:
            bundle_info['warnings'].append(f"Found {len(source_maps)} source map files (remove in production)")
        
        self.results['bundle_analysis'] = bundle_info
        return bundle_info
    
    def check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage patterns"""
        
        memory_info = {
            'estimated_usage_mb': 0,
            'memory_leak_risk': 'low',
            'issues': []
        }
        
        # Check for common memory issues in code
        code_patterns = {
            'event_listeners': r'addEventListener',
            'intervals': r'setInterval',
            'timeouts': r'setTimeout',
            'closures': r'function\s*\([^)]*\)\s*{[^}]*return\s+function',
            'large_arrays': r'new Array\([0-9]{5,}\)'
        }
        
        issues_count = defaultdict(int)
        
        # Scan files for memory-related patterns
        for file_path in self.project_path.glob('**/*.{js,jsx,ts,tsx,vue}'):
            if 'node_modules' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for pattern_name, pattern in code_patterns.items():
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        issues_count[pattern_name] += len(matches)
            except:
                pass
        
        # Estimate memory usage based on bundle size
        bundle_size_mb = self.results['bundle_analysis'].get('total_size_mb', 0)
        estimated_memory = bundle_size_mb * 10  # Rough estimate: 10x bundle size
        
        memory_info['estimated_usage_mb'] = round(estimated_memory, 2)
        
        # Determine risk level
        if issues_count['intervals'] > 20 or issues_count['event_listeners'] > 100:
            memory_info['memory_leak_risk'] = 'high'
            memory_info['issues'].append("Many event listeners/intervals found without cleanup")
        elif issues_count['intervals'] > 10 or issues_count['event_listeners'] > 50:
            memory_info['memory_leak_risk'] = 'medium'
            memory_info['issues'].append("Consider cleaning up event listeners and intervals")
        
        if estimated_memory > 200:
            memory_info['issues'].append(f"Estimated memory usage is high ({estimated_memory:.0f}MB)")
        
        self.results['memory_analysis'] = memory_info
        return memory_info
    
    def check_performance_patterns(self) -> Dict[str, Any]:
        """Check for performance anti-patterns"""
        
        performance_info = {
            'score': 100,
            'issues': [],
            'good_practices': []
        }
        
        # Check for common performance issues
        patterns_to_check = {
            'inline_styles': {
                'pattern': r'style=\{\{',
                'message': 'Inline styles may cause re-renders',
                'penalty': 5
            },
            'large_images': {
                'pattern': r'\.(jpg|jpeg|png)["\']\s*(?!.*loading="lazy")',
                'message': 'Large images without lazy loading',
                'penalty': 10
            },
            'unoptimized_loops': {
                'pattern': r'\.forEach\(.*=>\s*\{[^}]*\.forEach\(',
                'message': 'Nested loops may cause performance issues',
                'penalty': 15
            },
            'missing_memoization': {
                'pattern': r'useState\([^)]+\)(?!.*useMemo)',
                'message': 'Consider using useMemo for expensive calculations',
                'penalty': 5
            }
        }
        
        for file_path in self.project_path.glob('**/*.{js,jsx,ts,tsx,vue,html}'):
            if 'node_modules' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for check_name, check_info in patterns_to_check.items():
                        if re.search(check_info['pattern'], content, re.IGNORECASE):
                            if check_info['message'] not in [i['message'] for i in performance_info['issues']]:
                                performance_info['issues'].append({
                                    'type': check_name,
                                    'message': check_info['message'],
                                    'penalty': check_info['penalty']
                                })
                                performance_info['score'] -= check_info['penalty']
            except:
                pass
        
        # Check for good practices
        for file_path in self.project_path.glob('**/*.{js,jsx,ts,tsx}'):
            if 'node_modules' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if 'React.lazy' in content or 'lazy(' in content:
                        if 'Code splitting detected' not in performance_info['good_practices']:
                            performance_info['good_practices'].append('Code splitting detected')
                            performance_info['score'] += 5
                    
                    if 'memo(' in content or 'useMemo' in content:
                        if 'Memoization detected' not in performance_info['good_practices']:
                            performance_info['good_practices'].append('Memoization detected')
                            performance_info['score'] += 5
            except:
                pass
        
        performance_info['score'] = max(0, min(100, performance_info['score']))
        
        self.results['performance_scores'] = performance_info
        return performance_info
    
    def generate_recommendations(self):
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Bundle recommendations
        bundle = self.results['bundle_analysis']
        if bundle.get('warnings'):
            for warning in bundle['warnings']:
                recommendations.append({
                    'category': 'bundle',
                    'priority': 'high' if 'MB' in warning else 'medium',
                    'recommendation': warning,
                    'action': 'Reduce bundle size through code splitting and tree shaking'
                })
        
        # Memory recommendations
        memory = self.results['memory_analysis']
        if memory.get('memory_leak_risk') in ['high', 'medium']:
            recommendations.append({
                'category': 'memory',
                'priority': 'high',
                'recommendation': f"Memory leak risk is {memory['memory_leak_risk']}",
                'action': 'Clean up event listeners, intervals, and subscriptions in useEffect/onUnmounted'
            })
        
        # Performance recommendations
        perf = self.results['performance_scores']
        for issue in perf.get('issues', []):
            recommendations.append({
                'category': 'performance',
                'priority': 'high' if issue['penalty'] > 10 else 'medium',
                'recommendation': issue['message'],
                'action': f"Fix: {issue['message'].lower()}"
            })
        
        # Additional recommendations based on score
        if perf.get('score', 100) < 70:
            recommendations.append({
                'category': 'general',
                'priority': 'high',
                'recommendation': f"Performance score is low ({perf['score']}/100)",
                'action': 'Run Lighthouse audit and address critical issues'
            })
        
        # Windows 7 specific recommendations
        if self.results['bundle_analysis'].get('total_size_mb', 0) > 3:
            recommendations.append({
                'category': 'windows7',
                'priority': 'high',
                'recommendation': 'Large bundle size may cause issues on Windows 7 32-bit',
                'action': 'Implement aggressive code splitting and lazy loading'
            })
        
        self.results['recommendations'] = recommendations
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete performance audit"""
        
        print("Running performance audit...")
        
        print("  - Analyzing bundle size...")
        self.analyze_bundle_size()
        
        print("  - Checking memory patterns...")
        self.check_memory_usage()
        
        print("  - Scanning for performance issues...")
        self.check_performance_patterns()
        
        print("  - Generating recommendations...")
        self.generate_recommendations()
        
        # Calculate overall score
        bundle_score = max(0, 100 - (self.results['bundle_analysis'].get('total_size_mb', 0) * 10))
        memory_score = 100 if self.results['memory_analysis'].get('memory_leak_risk') == 'low' else 50
        perf_score = self.results['performance_scores'].get('score', 100)
        
        overall_score = (bundle_score + memory_score + perf_score) / 3
        
        self.results['overall_score'] = round(overall_score, 1)
        self.results['grade'] = self._get_grade(overall_score)
        
        return self.results
    
    def _get_grade(self, score: float) -> str:
        """Get letter grade for score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


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
    
    # Run audit
    audit = PerformanceAudit(project_path)
    results = audit.run_full_audit()
    
    # Output results
    if len(sys.argv) > 2 and sys.argv[2] == '--json':
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "=" * 60)
        print("PERFORMANCE AUDIT RESULTS")
        print("=" * 60)
        
        print(f"\nOverall Score: {results['overall_score']}/100")
        print(f"Grade: {results['grade']}")
        
        print(f"\n📦 Bundle Analysis:")
        print(f"  Total Size: {results['bundle_analysis'].get('total_size_mb', 0):.2f} MB")
        print(f"  Files Count: {results['bundle_analysis'].get('file_count', 0)}")
        
        if results['bundle_analysis'].get('largest_files'):
            print(f"  Largest File: {Path(results['bundle_analysis']['largest_files'][0]['path']).name} "
                  f"({results['bundle_analysis']['largest_files'][0]['size_mb']:.2f} MB)")
        
        print(f"\n💾 Memory Analysis:")
        print(f"  Estimated Usage: {results['memory_analysis'].get('estimated_usage_mb', 0)} MB")
        print(f"  Leak Risk: {results['memory_analysis'].get('memory_leak_risk', 'unknown').upper()}")
        
        print(f"\n⚡ Performance Score: {results['performance_scores'].get('score', 100)}/100")
        
        if results['performance_scores'].get('good_practices'):
            print(f"\n✅ Good Practices Found:")
            for practice in results['performance_scores']['good_practices']:
                print(f"  + {practice}")
        
        if results.get('recommendations'):
            print(f"\n📋 Recommendations ({len(results['recommendations'])}):")
            high_priority = [r for r in results['recommendations'] if r.get('priority') == 'high']
            for rec in high_priority[:5]:
                print(f"\n  🔴 [{rec['category'].upper()}] {rec['recommendation']}")
                print(f"     → {rec['action']}")
        
        print("\n" + "=" * 60)


# Import re for the module
import re

if __name__ == "__main__":
    main()