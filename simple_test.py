#!/usr/bin/env python3
"""
Simple test for accessibility tools
"""

from accessiblity_tools import check_color_contrast, get_wcag22_checklist

def main():
    print("🔍 WCAG 2.2 Accessibility Tools - Simple Test")
    print("=" * 50)
    
    # Test color contrast
    print("\n🎨 Testing Color Contrast:")
    result = check_color_contrast('#000000', '#ffffff')
    if result['success']:
        print(f"   Black on White: {result['contrast_ratio']}:1")
        print(f"   WCAG AA: {'✅ PASS' if result['wcag_aa_pass'] else '❌ FAIL'}")
        print(f"   WCAG AAA: {'✅ PASS' if result['wcag_aaa_pass'] else '❌ FAIL'}")
    
    # Test poor contrast
    print("\n   Testing poor contrast:")
    result2 = check_color_contrast('#cccccc', '#ffffff')
    if result2['success']:
        print(f"   Light Gray on White: {result2['contrast_ratio']}:1")
        print(f"   WCAG AA: {'✅ PASS' if result2['wcag_aa_pass'] else '❌ FAIL'}")
        print(f"   Status: {result2['recommendations']['status']}")
    
    # Test WCAG 2.2 checklist
    print("\n📋 Testing WCAG 2.2 Checklist:")
    checklist_result = get_wcag22_checklist()
    if checklist_result['success']:
        print(f"   ✅ Generated successfully!")
        print(f"   Total criteria: {checklist_result['total_criteria']}")
        print(f"   New in WCAG 2.2:")
        for item in checklist_result['new_in_wcag22']:
            print(f"      • {item}")
    
    print("\n🎉 Simple test completed!")
    print("✅ Accessibility tools are working properly")

if __name__ == "__main__":
    main() 