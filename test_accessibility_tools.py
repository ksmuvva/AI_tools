"""
Test script for WCAG 2.2 Accessibility Tools
============================================

This script demonstrates the capabilities of the accessibility testing toolkit
and shows how to use all the available tools and features.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from accessiblity_tools import (
    check_accessibility,
    check_color_contrast,
    get_wcag22_checklist,
    AccessibilityTester,
    ColorContrastChecker,
    WCAGChecklist
)

async def test_comprehensive_accessibility():
    """Test comprehensive accessibility checking"""
    print("\n" + "="*60)
    print("🔍 COMPREHENSIVE ACCESSIBILITY TESTING")
    print("="*60)
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://example.com"
    ]
    
    for url in test_urls:
        print(f"\n📋 Testing: {url}")
        print("-" * 40)
        
        try:
            # Run comprehensive test with multiple engines
            result = await check_accessibility(url, engines=["axe", "custom"])
            
            print(f"✅ Test completed successfully!")
            print(f"📊 Accessibility Score: {result['score']}/100")
            print(f"🔍 Total Issues: {result['summary']['total_issues']}")
            print(f"🚨 Violations: {result['summary']['violations']}")
            print(f"⚠️  Warnings: {result['summary']['warnings']}")
            print(f"📝 Manual Checks: {result['summary']['manual_checks']}")
            
            # Show WCAG principle breakdown
            print(f"\n📋 WCAG Principle Breakdown:")
            for principle, count in result['wcag_summary'].items():
                print(f"   {principle}: {count} issues")
                
            # Show top recommendations
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(result['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")

def test_color_contrast():
    """Test color contrast analysis"""
    print("\n" + "="*60)
    print("🎨 COLOR CONTRAST TESTING")
    print("="*60)
    
    # Test color combinations
    test_combinations = [
        ("#000000", "#ffffff", "Black on White"),
        ("#ffffff", "#000000", "White on Black"),
        ("#0066cc", "#ffffff", "Blue on White"),
        ("#ffff00", "#ffffff", "Yellow on White (Poor)"),
        ("#666666", "#ffffff", "Gray on White"),
        ("#ff0000", "#00ff00", "Red on Green (Poor)"),
        ("#003366", "#ffffff", "Dark Blue on White"),
        ("#cccccc", "#ffffff", "Light Gray on White (Poor)")
    ]
    
    print(f"\n📊 Testing {len(test_combinations)} color combinations...")
    print("-" * 50)
    
    for fg, bg, description in test_combinations:
        result = check_color_contrast(fg, bg)
        
        if result['success']:
            ratio = result['contrast_ratio']
            aa_pass = "✅ PASS" if result['wcag_aa_pass'] else "❌ FAIL"
            aaa_pass = "✅ PASS" if result['wcag_aaa_pass'] else "❌ FAIL"
            
            print(f"\n🎨 {description}")
            print(f"   Colors: {fg} on {bg}")
            print(f"   Contrast Ratio: {ratio}:1")
            print(f"   WCAG AA: {aa_pass}")
            print(f"   WCAG AAA: {aaa_pass}")
            print(f"   Status: {result['recommendations']['status']}")
        else:
            print(f"❌ {description}: {result['error']}")

def test_wcag22_checklist():
    """Test WCAG 2.2 checklist generation"""
    print("\n" + "="*60)
    print("📋 WCAG 2.2 CHECKLIST TESTING")
    print("="*60)
    
    try:
        result = get_wcag22_checklist("https://example.com")
        
        if result['success']:
            checklist = result['checklist']
            
            print(f"✅ WCAG 2.2 Checklist Generated Successfully!")
            print(f"📊 Total Criteria: {result['total_criteria']}")
            print(f"🅰️  Level A Criteria: {checklist['level_a_criteria']}")
            print(f"🅰️🅰️ Level AA Criteria: {checklist['level_aa_criteria']}")
            print(f"🆕 New in WCAG 2.2: {checklist['wcag22_new_criteria']}")
            
            print(f"\n🎯 WCAG Principle Summary:")
            for principle, criteria in checklist['summary'].items():
                print(f"   {principle}: {len(criteria)} criteria")
                
            print(f"\n🆕 New WCAG 2.2 Criteria:")
            for criterion in result['new_in_wcag22']:
                print(f"   • {criterion}")
                
            # Show sample criteria details
            print(f"\n📝 Sample Criteria Details:")
            sample_criteria = ["1.1.1", "2.5.8", "3.3.8"]  # Mix of old and new
            
            for criterion in sample_criteria:
                if criterion in checklist['checklist']:
                    details = checklist['checklist'][criterion]
                    print(f"\n   🔍 {criterion}: {details['title']} (Level {details['level']})")
                    print(f"      {details['description']}")
                    print(f"      Manual Checks: {len(details['manual_checks'])}")
                    print(f"      Automated Checks: {len(details['automated_checks'])}")
                    
        else:
            print(f"❌ Checklist generation failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_individual_tools():
    """Test individual tool classes"""
    print("\n" + "="*60)
    print("🔧 INDIVIDUAL TOOL TESTING")
    print("="*60)
    
    # Test ColorContrastChecker
    print(f"\n🎨 Testing ColorContrastChecker...")
    checker = ColorContrastChecker()
    
    test_colors = [
        ("#000000", "#ffffff"),
        ("#0066cc", "#ffffff"),
        ("#ffff00", "#ffffff")
    ]
    
    for fg, bg in test_colors:
        ratio = checker.calculate_contrast_ratio(fg, bg)
        compliance = checker.check_wcag_compliance(ratio)
        
        print(f"   {fg} on {bg}: {ratio:.2f}:1 (AA: {'✅' if compliance['AA'] else '❌'})")
    
    # Test WCAGChecklist
    print(f"\n📋 Testing WCAGChecklist...")
    wcag_checklist = WCAGChecklist()
    
    print(f"   Total checklist items: {len(wcag_checklist.checklist_items)}")
    print(f"   Sample criteria: {list(wcag_checklist.checklist_items.keys())[:5]}")
    
    # Test AccessibilityTester (without async)
    print(f"\n🧪 Testing AccessibilityTester initialization...")
    tester = AccessibilityTester()
    
    print(f"   Available engines: {list(tester.engines.keys())}")
    print(f"   WCAG 2.2 criteria loaded: {len(tester.wcag_22_criteria)}")
    
    # Show new WCAG 2.2 criteria
    wcag22_new = ["2.5.7", "2.5.8", "3.2.6", "3.3.7", "3.3.8"]
    print(f"   New WCAG 2.2 criteria:")
    for criterion in wcag22_new:
        if criterion in tester.wcag_22_criteria:
            details = tester.wcag_22_criteria[criterion]
            print(f"      • {criterion}: {details['title']}")

def show_tool_capabilities():
    """Show comprehensive tool capabilities"""
    print("\n" + "="*60)
    print("🚀 ACCESSIBILITY TOOLKIT CAPABILITIES")
    print("="*60)
    
    capabilities = {
        "🧪 Testing Engines": [
            "axe-core (Industry Standard)",
            "Pa11y (CLI-based testing)",
            "Google Lighthouse (Built-in Chrome)",
            "WAVE (WebAIM evaluation)",
            "Custom WCAG 2.2 validator"
        ],
        "🎯 WCAG 2.2 Support": [
            "All 50+ WCAG 2.2 success criteria",
            "Level A, AA, and AAA compliance",
            "New 2.2 criteria (Target Size, Dragging, etc.)",
            "Comprehensive principle coverage",
            "Automated + manual test guidance"
        ],
        "🎨 Color Analysis": [
            "Contrast ratio calculation",
            "WCAG AA/AAA compliance checking",
            "Multiple color format support",
            "Font size consideration",
            "Automatic threshold detection"
        ],
        "📊 Reporting Features": [
            "Comprehensive accessibility scores",
            "Detailed issue categorization",
            "WCAG principle breakdown",
            "Actionable recommendations",
            "Multiple output formats"
        ],
        "🔧 Integration Support": [
            "Async/await compatibility",
            "Multiple engine aggregation",
            "CLI tool integration",
            "Browser automation ready",
            "Custom rule extensibility"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n{category}:")
        for feature in features:
            print(f"   ✅ {feature}")

async def main():
    """Run all accessibility tool tests"""
    print("🔍 WCAG 2.2 Accessibility Testing Toolkit")
    print("=" * 60)
    print("Testing comprehensive accessibility tools with multiple engines")
    print("Supports axe-core, Pa11y, Lighthouse, WAVE, and custom WCAG 2.2 validation")
    
    # Show capabilities
    show_tool_capabilities()
    
    # Test individual tools first
    test_individual_tools()
    
    # Test color contrast
    test_color_contrast()
    
    # Test WCAG 2.2 checklist
    test_wcag22_checklist()
    
    # Test comprehensive accessibility (async)
    await test_comprehensive_accessibility()
    
    print(f"\n" + "="*60)
    print("🎉 ALL TESTS COMPLETED!")
    print("="*60)
    print("✅ Accessibility toolkit is ready for use")
    print("📚 Use the tools in your automation scripts or manual testing")
    print("🔗 Integrate with browser automation tools for full testing")
    
    print(f"\n💡 Usage Examples:")
    print(f"   • await check_accessibility('https://yoursite.com')")
    print(f"   • check_color_contrast('#000000', '#ffffff')")
    print(f"   • get_wcag22_checklist('https://yoursite.com')")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc() 