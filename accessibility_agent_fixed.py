#!/usr/bin/env python3
"""
FIXED SOPHISTICATED AGENT - WITH PROPER ACCESSIBILITY TOOL INVOCATION
=====================================================================

This agent properly invokes accessibility tools when requested.
"""

import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from accessiblity_tools import check_accessibility, check_color_contrast, get_wcag22_checklist

class FixedAccessibilityAgent:
    """Agent that properly handles accessibility testing requests"""
    
    def __init__(self):
        self.tools = {
            "check_accessibility": check_accessibility,
            "check_color_contrast": check_color_contrast, 
            "get_wcag22_checklist": get_wcag22_checklist
        }
    
    async def process_goal(self, goal: str):
        """Process user goal and invoke appropriate accessibility tools"""
        goal_lower = goal.lower()
        
        print(f"🎯 Processing Goal: {goal}")
        print("="*70)
        
        # Check if it's an accessibility request
        if any(word in goal_lower for word in ["accessibility", "a11y", "wcag", "audit", "test"]):
            print("♿ ACCESSIBILITY REQUEST DETECTED!")
            
            # Check for color contrast requests
            if "color" in goal_lower and "contrast" in goal_lower:
                await self._handle_color_contrast_request(goal)
            
            # Check for full accessibility audit requests  
            elif any(word in goal_lower for word in ["audit", "test", "check", "analyze", "analyse"]):
                await self._handle_accessibility_audit_request(goal)
            
            # Check for checklist requests
            elif "checklist" in goal_lower or "compliance" in goal_lower:
                await self._handle_checklist_request(goal)
                
            else:
                # Default to full accessibility audit
                await self._handle_accessibility_audit_request(goal)
        
        # Check for navigation + accessibility combo
        elif "navigate" in goal_lower or "google" in goal_lower:
            if any(word in goal_lower for word in ["accessibility", "a11y", "wcag", "audit", "test", "analyze", "analyse", "accesiiblity", "check"]):
                print("🌐 NAVIGATION + ACCESSIBILITY REQUEST DETECTED!")
                await self._handle_navigation_with_accessibility(goal)
            else:
                print("🌐 Navigation only request - would handle navigation")
        
        else:
            print("ℹ️ No accessibility request detected in goal")
    
    async def _handle_color_contrast_request(self, goal: str):
        """Handle color contrast testing requests"""
        print("\n🎨 HANDLING COLOR CONTRAST REQUEST:")
        
        # Extract colors from goal if present
        if "#" in goal:
            # Try to extract hex colors
            import re
            colors = re.findall(r'#[0-9a-fA-F]{3,6}', goal)
            if len(colors) >= 2:
                fg, bg = colors[0], colors[1]
                print(f"   🎯 Testing colors from goal: {fg} on {bg}")
                result = check_color_contrast(fg, bg)
                self._display_color_result(result, fg, bg)
                return
        
        # Default test cases
        print("   🎯 Running default color contrast tests:")
        test_cases = [
            ("#000000", "#ffffff", "Black on White"),
            ("#0066cc", "#ffffff", "Blue on White"),
            ("#ff0000", "#ffffff", "Red on White")
        ]
        
        for fg, bg, desc in test_cases:
            result = check_color_contrast(fg, bg)
            self._display_color_result(result, fg, bg, desc)
    
    def _display_color_result(self, result, fg, bg, desc=""):
        """Display color contrast test result"""
        if result['success']:
            ratio = result['contrast_ratio']
            aa_pass = "✅ PASS" if result['wcag_aa_pass'] else "❌ FAIL"
            aaa_pass = "✅ PASS" if result['wcag_aaa_pass'] else "❌ FAIL"
            print(f"   {desc or f'{fg} on {bg}'}: {ratio}:1")
            print(f"      WCAG AA: {aa_pass} | WCAG AAA: {aaa_pass}")
        else:
            print(f"   ❌ Error testing {fg} on {bg}: {result['error']}")
    
    async def _handle_accessibility_audit_request(self, goal: str):
        """Handle full accessibility audit requests"""
        print("\n♿ HANDLING ACCESSIBILITY AUDIT REQUEST:")
        
        # Extract URL from goal if present
        url = self._extract_url_from_goal(goal)
        
        print(f"   🔍 Testing URL: {url}")
        print("   🛠️ Using engines: axe, custom, wave")
        
        try:
            result = await check_accessibility(url, ["axe", "custom", "wave"])
            
            if result['success']:
                print(f"\n   📊 ACCESSIBILITY AUDIT RESULTS:")
                print(f"   🎯 Overall Score: {result['score']}/100")
                print(f"   🚨 Violations: {result['summary']['violations']}")
                print(f"   ⚠️  Warnings: {result['summary']['warnings']}")
                print(f"   📝 Manual Checks: {result['summary']['manual_checks']}")
                
                if result.get('recommendations'):
                    print(f"\n   💡 TOP RECOMMENDATIONS:")
                    for i, rec in enumerate(result['recommendations'][:3], 1):
                        print(f"   {i}. {rec}")
                
                # Provide grade based on score
                score = result['score']
                if score >= 90:
                    grade = "A+ (Excellent)"
                elif score >= 80:
                    grade = "A (Good)"
                elif score >= 70:
                    grade = "B (Fair)"
                elif score >= 60:
                    grade = "C (Needs Improvement)"
                else:
                    grade = "D (Poor - Requires Attention)"
                
                print(f"\n   🎓 ACCESSIBILITY GRADE: {grade}")
            else:
                print(f"   ❌ Audit failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Error during audit: {str(e)}")
    
    async def _handle_checklist_request(self, goal: str):
        """Handle WCAG checklist requests"""
        print("\n📋 HANDLING WCAG 2.2 CHECKLIST REQUEST:")
        
        url = self._extract_url_from_goal(goal)
        
        try:
            result = get_wcag22_checklist(url)
            
            if result['success']:
                print(f"   ✅ Checklist generated successfully!")
                print(f"   📊 Total Criteria: {result['total_criteria']}")
                print(f"   🆕 New in WCAG 2.2: {len(result['new_in_wcag22'])}")
                
                print(f"\n   📋 NEW WCAG 2.2 CRITERIA:")
                for criterion in result['new_in_wcag22']:
                    print(f"   • {criterion}")
                
                print(f"\n   🎯 COMPLIANCE SUMMARY:")
                level_counts = result.get('level_counts', {})
                for level, count in level_counts.items():
                    print(f"   Level {level}: {count} criteria")
                    
            else:
                print(f"   ❌ Checklist generation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Error generating checklist: {str(e)}")
    
    async def _handle_navigation_with_accessibility(self, goal: str):
        """Handle navigation followed by accessibility testing"""
        print("\n🌐 HANDLING NAVIGATION + ACCESSIBILITY REQUEST:")
        
        url = self._extract_url_from_goal(goal)
        
        print(f"   1️⃣ Would navigate to: {url}")
        print(f"   2️⃣ Would accept cookies if present")
        print(f"   3️⃣ Running accessibility audit...")
        
        # Skip navigation simulation, go directly to accessibility testing
        await self._handle_accessibility_audit_request(goal)
    
    def _extract_url_from_goal(self, goal: str) -> str:
        """Extract URL from goal text"""
        goal_lower = goal.lower()
        
        if "google" in goal_lower:
            return "https://google.com"
        elif "github" in goal_lower:
            return "https://github.com"
        elif "webaim" in goal_lower:
            return "https://webaim.org"
        elif "http" in goal:
            # Extract actual URL
            import re
            urls = re.findall(r'https?://[^\s]+', goal)
            if urls:
                return urls[0]
        
        # Default
        return "https://google.com"

async def main():
    """Main function for fixed accessibility agent"""
    print("🧠 FIXED ACCESSIBILITY AGENT")
    print("="*50)
    print("✅ This agent PROPERLY invokes accessibility tools!")
    print("💡 Try these commands:")
    print("   • 'Check accessibility of google.com'")
    print("   • 'Test color contrast of #000 on #fff'") 
    print("   • 'Generate WCAG 2.2 checklist'")
    print("   • 'Navigate to google.com and analyze accessibility'")
    print("="*50)
    
    agent = FixedAccessibilityAgent()
    
    while True:
        try:
            goal = input("\n🎯 Your goal: ").strip()
            
            if goal.lower() in ["exit", "quit", "stop"]:
                print("👋 Goodbye!")
                break
                
            if not goal:
                continue
                
            await agent.process_goal(goal)
            print("\n✅ Goal processing completed!")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 