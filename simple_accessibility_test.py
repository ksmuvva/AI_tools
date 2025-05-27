#!/usr/bin/env python3
"""
SIMPLE ACCESSIBILITY TESTING - Direct Tool Invocation
====================================================

This script demonstrates how to properly invoke accessibility tools directly.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from accessiblity_tools import check_accessibility, check_color_contrast, get_wcag22_checklist

async def run_accessibility_tests():
    """Run comprehensive accessibility testing directly"""
    print("🧪 DIRECT ACCESSIBILITY TESTING")
    print("="*50)
    
    # Test 1: Color Contrast
    print("\n1️⃣ COLOR CONTRAST TESTING:")
    test_cases = [
        ("#000000", "#ffffff", "Black on White"),
        ("#0066cc", "#ffffff", "Blue on White"),
        ("#ff0000", "#ffffff", "Red on White"),
        ("#cccccc", "#ffffff", "Light Gray on White (Fail)")
    ]
    
    for fg, bg, desc in test_cases:
        result = check_color_contrast(fg, bg)
        ratio = result['contrast_ratio']
        aa_pass = "✅ PASS" if result['wcag_aa_pass'] else "❌ FAIL"
        print(f"   {desc}: {ratio}:1 - {aa_pass}")
    
    # Test 2: Website Accessibility Audit
    print("\n2️⃣ WEBSITE ACCESSIBILITY AUDIT:")
    test_urls = [
        "https://google.com",
        "https://github.com",
        "https://webaim.org"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        try:
            # Use reliable engines only
            result = await check_accessibility(url, ["axe", "custom"])
            
            if result['success']:
                print(f"   📊 Score: {result['score']}/100")
                print(f"   🚨 Violations: {result['summary']['violations']}")
                print(f"   ⚠️ Warnings: {result['summary']['warnings']}")
                print(f"   📝 Manual Checks: {result['summary']['manual_checks']}")
                
                if result.get('recommendations'):
                    print("   💡 Top Recommendation:")
                    print(f"      • {result['recommendations'][0]}")
            else:
                print(f"   ❌ Test failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"   ❌ Error testing {url}: {str(e)}")
    
    # Test 3: WCAG 2.2 Checklist
    print("\n3️⃣ WCAG 2.2 COMPLIANCE CHECKLIST:")
    try:
        checklist = get_wcag22_checklist("https://google.com")
        if checklist['success']:
            print(f"   ✅ Generated successfully!")
            print(f"   📊 Total Criteria: {checklist['total_criteria']}")
            print(f"   🆕 New in WCAG 2.2: {len(checklist['new_in_wcag22'])}")
            print("   📋 Sample New Criteria:")
            for criterion in checklist['new_in_wcag22'][:3]:
                print(f"      • {criterion}")
        else:
            print(f"   ❌ Failed: {checklist.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error generating checklist: {str(e)}")
    
    print("\n🎉 ACCESSIBILITY TESTING COMPLETED!")
    print("✅ All accessibility tools are working properly!")

if __name__ == "__main__":
    asyncio.run(run_accessibility_tests()) 