#!/usr/bin/env python3
"""
Test sophisticated agent with accessibility tools integration
"""

import asyncio
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sophisticated_agent_client import SophisticatedAgentClient

async def test_sophisticated_agent():
    """Test that sophisticated agent has accessibility tools"""
    print("🧠 Testing Sophisticated Agent with Accessibility Tools")
    print("=" * 60)
    
    try:
        # Initialize agent
        agent = SophisticatedAgentClient()
        await agent.initialize()
        
        print("✅ Sophisticated agent initialized successfully!")
        
        # Check tool categories
        print(f"\n📊 Tool Categories:")
        print(f"   🔍 Element Locators: {len(agent.locator_tools)}")
        print(f"   ⚡ Action Tools: {len(agent.action_tools)}")
        print(f"   🛠️ Utility Tools: {len(agent.utility_tools)}")
        print(f"   ♿ Accessibility Tools: {len(agent.accessibility_tools)}")
        
        # Show accessibility tools
        print(f"\n♿ Accessibility Tools Available:")
        for tool_name, tool_info in agent.accessibility_tools.items():
            print(f"   • {tool_name}: {tool_info['description']}")
        
        # Show sample Playwright tools
        print(f"\n🔍 Sample Element Locator Tools:")
        for i, (tool_name, tool_info) in enumerate(agent.locator_tools.items()):
            if i < 3:  # Show first 3
                print(f"   • {tool_name}: {tool_info['description']}")
        
        print(f"\n⚡ Sample Action Tools:")
        for i, (tool_name, tool_info) in enumerate(agent.action_tools.items()):
            if i < 3:  # Show first 3
                print(f"   • {tool_name}: {tool_info['description']}")
        
        # Test tool validation
        print(f"\n🧪 Testing Tool Validation:")
        
        # Valid accessibility tool
        test_tools = ["check_accessibility", "check_color_contrast", "playwright_navigate", "unknown_tool"]
        all_tools = {**agent.locator_tools, **agent.action_tools, **agent.utility_tools, **agent.accessibility_tools}
        
        for tool in test_tools:
            exists = tool in all_tools or hasattr(agent.tools, tool)
            status = "✅ Found" if exists else "❌ Not found"
            print(f"   {tool}: {status}")
        
        print(f"\n🎉 Test completed successfully!")
        print(f"📈 Total tools available: {len(all_tools)}")
        
        # Clean up
        await agent.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sophisticated_agent()) 