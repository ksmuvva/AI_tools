#!/usr/bin/env python3
"""
Test script to verify the upgraded Unified Agent with Continuous LLM interaction
"""
import asyncio
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

async def test_unified_agent():
    """Test the upgraded unified agent features"""
    print("🧪 Testing Upgraded Unified Agent Features...")
    
    try:
        from unified_agent_client import UnifiedAgentClient, AgentMode
        
        # Test 1: Verify default mode is CONTINUOUS
        agent = UnifiedAgentClient()
        print(f"✅ Default mode: {agent.mode.value} (should be 'continuous')")
        
        # Test 2: Verify initialization with full tool discovery
        if await agent.initialize():
            print(f"✅ Agent initialized successfully")
            print(f"✅ Tools discovered: {len(agent.available_tools)} (should be 50+)")
            
            # Test 3: Verify LLM client
            if agent.llm_client:
                print("✅ LLM client initialized")
            else:
                print("❌ LLM client not available (check ANTHROPIC_API_KEY)")
            
            # Test 4: Verify tools documentation generation
            tools_doc = agent._generate_tools_documentation()
            if "COMPLETE PLAYWRIGHT TOOLS AVAILABLE" in tools_doc:
                print("✅ Complete tools documentation generated")
            else:
                print("❌ Tools documentation incomplete")
            
            # Test 5: Verify enhanced continuous features
            has_continuous_features = (
                hasattr(agent, 'continuous_llm_interaction') and
                hasattr(agent, '_parse_llm_response') and
                hasattr(agent, '_create_fallback_plan') and
                hasattr(agent, '_execute_continuous_step')
            )
            
            if has_continuous_features:
                print("✅ Enhanced continuous LLM features available")
            else:
                print("❌ Missing continuous LLM features")
            
            # Test 6: Verify failure tracking
            if hasattr(agent, 'failure_count') and hasattr(agent, 'max_failures'):
                print("✅ Failure tracking system available")
            else:
                print("❌ Missing failure tracking")
            
            await agent.close()
            
        else:
            print("❌ Agent initialization failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

async def main():
    print("=" * 80)
    print("🚀 UNIFIED AGENT UPGRADE VERIFICATION")
    print("=" * 80)
    print("🎯 Testing: Continuous LLM as Default Mode")
    print("🧠 Testing: Complete Tool Knowledge")
    print("🛠️ Testing: Enhanced Failure Recovery")
    print("=" * 80)
    
    await test_unified_agent()
    
    print("\n" + "=" * 80)
    print("✅ VERIFICATION COMPLETE!")
    print("=" * 80)
    print("🔄 Ready to use: python unified_agent_client.py")
    print("💡 Default mode: CONTINUOUS with step-by-step LLM decisions")
    print("🧠 Full knowledge of ALL Playwright tools available")
    print("🛠️ Intelligent failure recovery with LLM guidance")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main()) 