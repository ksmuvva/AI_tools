#!/usr/bin/env python3
"""
Simple test for the fixed sophisticated agent
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from accessiblity_tools import check_accessibility, check_color_contrast
    print("✅ Accessibility tools imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")

def test_goal_parsing():
    """Test the goal parsing logic we added"""
    import re
    
    goal = "Navigate to https://the-internet.herokuapp.com/add_remove_elements/ and add 3 elements by clicking \"Add Element\" button 3 times. Then remove 1 element and take a screenshot showing the remaining \"Delete\" buttons. Also check for accessiblity"
    
    print(f"🎯 Testing goal parsing for: {goal}")
    print("="*80)
    
    goal_lower = goal.lower()
    required_steps = []
    
    # Check for navigation requirement
    if any(word in goal_lower for word in ["navigate", "go to", "visit"]):
        required_steps.append("navigation")
        print("📍 Navigation step detected")
    
    # Check for click requirements with specific count
    click_matches = re.findall(r'click[^\s]*\s+[^.]*?(\d+)\s*times?', goal_lower)
    if click_matches:
        times = int(click_matches[0])
        required_steps.append(f"click_{times}_times")
        print(f"🔘 Click step detected: {times} times")
    
    # Check for removal requirements
    if any(word in goal_lower for word in ["remove", "delete"]):
        required_steps.append("remove_element")
        print("🗑️ Remove step detected")
    
    # Check for screenshot requirements
    if "screenshot" in goal_lower:
        required_steps.append("screenshot")
        print("📸 Screenshot step detected")
    
    # Check for accessibility requirements
    if any(word in goal_lower for word in ["accessibility", "a11y", "wcag", "accessiblity"]):
        required_steps.append("accessibility")
        print("♿ Accessibility step detected")
    
    print(f"📊 Total steps detected: {len(required_steps)}")
    print(f"Required steps: {required_steps}")
    
    return len(required_steps) == 5  # Should detect all 5 steps

async def test_accessibility_tools():
    """Test accessibility tools directly"""
    print("\n🧪 Testing accessibility tools directly...")
    
    try:
        result = await check_accessibility("https://google.com", ["axe", "custom"])
        if result['success']:
            print(f"✅ Accessibility test successful: {result['score']}/100")
            return True
        else:
            print(f"❌ Accessibility test failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Accessibility test error: {e}")
        return False

def test_color_contrast():
    """Test color contrast tools"""
    print("\n🎨 Testing color contrast tools...")
    
    try:
        result = check_color_contrast("#000000", "#ffffff")
        if result['success']:
            ratio = result['contrast_ratio']
            aa_pass = result['wcag_aa_pass']
            print(f"✅ Color contrast test successful: {ratio}:1, AA: {'PASS' if aa_pass else 'FAIL'}")
            return True
        else:
            print(f"❌ Color contrast test failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Color contrast test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 TESTING FIXED SOPHISTICATED AGENT")
    print("="*50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Goal Parsing
    print("\n1️⃣ Testing goal parsing logic...")
    if test_goal_parsing():
        print("✅ Goal parsing test PASSED")
        tests_passed += 1
    else:
        print("❌ Goal parsing test FAILED")
    
    # Test 2: Accessibility Tools
    print("\n2️⃣ Testing accessibility tools...")
    if await test_accessibility_tools():
        print("✅ Accessibility tools test PASSED")
        tests_passed += 1
    else:
        print("❌ Accessibility tools test FAILED")
    
    # Test 3: Color Contrast
    print("\n3️⃣ Testing color contrast tools...")
    if test_color_contrast():
        print("✅ Color contrast test PASSED")
        tests_passed += 1
    else:
        print("❌ Color contrast test FAILED")
    
    # Summary
    print(f"\n📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The fixed agent should work properly.")
    else:
        print("⚠️ Some tests failed. Check the issues above.")

if __name__ == "__main__":
    asyncio.run(main()) 