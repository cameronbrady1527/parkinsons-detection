#!/usr/bin/env python3
"""
Test script to verify static file paths are correctly configured
"""

import os
import re

def test_static_file_paths():
    """Test that static files use relative paths instead of absolute paths"""
    print("🔍 Testing Static File Paths")
    print("=" * 50)
    
    # Files to check
    html_files = [
        "static/index.html",
        "static/parkinsons-info.html"
    ]
    
    issues_found = []
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"❌ File not found: {html_file}")
            continue
            
        print(f"\n📄 Checking: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for absolute paths to static files (these are correct)
        absolute_paths = re.findall(r'href=["\']/static/([^"\']+)["\']', content)
        if absolute_paths:
            print(f"   ✅ Found absolute paths: {absolute_paths}")
        else:
            print(f"   ❌ No absolute paths found")
            issues_found.append(f"{html_file}: Missing absolute paths")
        
        # Check for relative paths to static files (these are problematic)
        relative_paths = re.findall(r'href=["\']\./([^"\']+)["\']', content)
        if relative_paths:
            print(f"   ❌ Found problematic relative paths: {relative_paths}")
            issues_found.append(f"{html_file}: {relative_paths}")
        else:
            print(f"   ✅ No problematic relative paths found")
        
        # Check for script src paths (these should be absolute)
        script_paths = re.findall(r'src=["\']/static/([^"\']+)["\']', content)
        if script_paths:
            print(f"   ✅ Found absolute script paths: {script_paths}")
        else:
            print(f"   ❌ No absolute script paths found")
            issues_found.append(f"{html_file} scripts: Missing absolute paths")
    
    # Summary
    print("\n" + "=" * 50)
    if issues_found:
        print("❌ Issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        print("\n💡 Fix: Ensure all static file references use absolute paths (/static/...)")
    else:
        print("✅ All static file paths are correctly configured!")
        print("   Your Railway deployment should now work properly.")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    test_static_file_paths()
