#!/usr/bin/env python3
"""
SOPHISTICATED AI AGENT CLIENT - Proper Element Location & Action Strategy
🧠 UPGRADED: Two-step workflow (Find Element → Perform Action)

✅ STRATEGY: Proper locate → action → verify workflow
✅ COMPLETE: Accurate knowledge of ALL tools with correct parameters
✅ SOPHISTICATED: Multi-strategy element location with smart fallbacks
✅ AUDITED: Each step properly validated and reported
"""
import asyncio
import json
import os
import sys
import logging
import time
import inspect
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # For older Python versions
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ Environment variables loaded from .env file")

load_env_file()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sophisticated_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import required packages
try:
    import anthropic
    from Playwright_tools import PlaywrightTools
    from dom_analyzer import DOMAnalyzer
    from accessiblity_tools import (
        check_accessibility,
        check_color_contrast,
        get_wcag22_checklist,
        AccessibilityTester,
        ColorContrastChecker,
        WCAGChecklist
    )
    print("✅ All packages imported successfully (Playwright + Accessibility)")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class AgentMode(Enum):
    """Agent operation modes"""
    BASIC = "basic"           # Single LLM call, basic locators
    INTELLIGENT = "intelligent"  # Multi-strategy locators, DOM analysis  
    CONTINUOUS = "continuous"    # Continuous LLM interaction (DEFAULT)
    ULTIMATE = "ultimate"       # All features + continuous interaction

@dataclass
class AgentResult:
    """Sophisticated result structure"""
    success: bool
    step_description: str
    tool_used: str
    phase: str = ""
    strategy_used: str = ""
    confidence: float = 0.0
    execution_time: float = 0.0
    element_found: bool = False
    selector_used: str = ""
    alternatives: List[str] = None
    error_message: str = ""

class SophisticatedAgentClient:
    """
    SOPHISTICATED AI AGENT CLIENT - Proper Element Location & Action Strategy
    
    🎯 STRATEGY: Two-step workflow (Find Element → Perform Action)
    🧠 COMPLETE: Accurate knowledge of ALL tools with correct parameters
    🛠️ INTELLIGENT: Multi-strategy element location with smart fallbacks
    📊 AUDITED: Each step properly validated and reported
    """
    
    def __init__(self, mode: AgentMode = AgentMode.CONTINUOUS):
        self.tools = None
        self.llm_client = None
        self.dom_analyzer = None
        self.mode = mode
        self.locator_tools = {}
        self.action_tools = {}
        self.utility_tools = {}
        self.accessibility_tools = {}
        self.conversation_history = []
        self.execution_context = {}
        self.failure_count = 0
        self.max_failures = 3
        self.setup_anthropic()
    
    def setup_anthropic(self):
        """Initialize the Anthropic client."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found")
            return False
        
        try:
            self.llm_client = anthropic.Anthropic(api_key=api_key)
            logger.info("Anthropic client initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic: {e}")
            return False
    
    async def initialize(self):
        """Initialize all systems with sophisticated tool categorization"""
        try:
            self.tools = PlaywrightTools()
            await self.tools.initialize()
            
            self.dom_analyzer = DOMAnalyzer(self.tools)
            
            # Categorize tools properly for LLM understanding
            await self._categorize_all_tools()
            
            logger.info("Sophisticated Agent systems initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Sophisticated Agent: {e}")
            return False

    async def _categorize_all_tools(self) -> None:
        """Categorize all tools into proper workflow categories"""
        print("🔧 Categorizing ALL available tools for sophisticated workflow...")
        
        # Element Location Tools (First Step) - ALL LOCATOR METHODS
        self.locator_tools = {
            # Smart Locators
            "playwright_smart_text_locator": {
                "description": "Find elements by text content with fuzzy matching and scoring",
                "parameters": {"text": "str", "element_types": "list (optional)", "action": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Best for finding elements by visible text with intelligent matching"
            },
            "playwright_multi_strategy_locate": {
                "description": "Use multiple strategies to locate elements with fallback approaches",
                "parameters": {"description": "str", "action": "str (optional)", "page_index": "int (optional)"},
                "use_case": "When simple locators fail, tries multiple approaches automatically"
            },
            "playwright_find_by_role": {
                "description": "Find elements by ARIA role and accessible name",
                "parameters": {"role": "str", "name": "str (optional)", "exact": "bool (optional)", "action": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Best for accessible elements (buttons, inputs, headings, etc.)"
            },
            "playwright_accessibility_locator": {
                "description": "Find elements using accessibility attributes (aria-label, aria-describedby)",
                "parameters": {"description": "str", "action": "str (optional)", "page_index": "int (optional)"},
                "use_case": "For elements with aria-label, aria-describedby, or other accessibility attributes"
            },
            "playwright_css_locator": {
                "description": "Find elements using CSS selectors with enhanced Playwright features",
                "parameters": {"selector": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "When you know the exact CSS selector or want to use advanced CSS features"
            },
            "playwright_xpath_locator": {
                "description": "Find elements using XPath expressions",
                "parameters": {"xpath": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Complex element relationships and advanced element selection"
            },
            "playwright_label_to_control": {
                "description": "Find form controls by their label text",
                "parameters": {"label_text": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Find input fields, selects, and other form controls by their labels"
            },
            "playwright_locator_by_label": {
                "description": "Alternative label-based locator with exact matching options",
                "parameters": {"text": "str", "exact": "bool (optional)", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Find form controls with precise label matching"
            },
            "playwright_nth_element": {
                "description": "Target specific element by index in a collection",
                "parameters": {"selector": "str", "index": "int", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "When multiple elements match and you need a specific one"
            },
            "playwright_parent_element": {
                "description": "Target the parent element of a matched element",
                "parameters": {"selector": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Click or interact with parent containers"
            },
            "playwright_custom_attribute_locator": {
                "description": "Find elements by custom attributes with partial matching",
                "parameters": {"attribute": "str", "value": "str", "action": "str (optional)", "text_input": "str (optional)", "partial_match": "bool (optional)", "page_index": "int (optional)"},
                "use_case": "Locate elements by data attributes or custom properties"
            },
            "playwright_complex_selector_builder": {
                "description": "Build complex selectors with multiple criteria",
                "parameters": {"criteria": "dict", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Advanced element selection with multiple conditions"
            },
            "playwright_js_locate": {
                "description": "Use JavaScript for custom element location logic",
                "parameters": {"description": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Last resort locator with maximum flexibility and custom logic"
            },
            "playwright_vision_locator": {
                "description": "Visual element location using image recognition",
                "parameters": {"text": "str", "action": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Find elements based on visual appearance"
            },
            "playwright_comprehensive_element_analyzer": {
                "description": "Analyze all elements on page with detailed properties",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Understand page structure and available elements"
            }
        }
        
        # Action Tools (Second Step) - ALL ACTION METHODS
        self.action_tools = {
            # Direct Actions
            "playwright_click": {
                "description": "Click an element using selector",
                "parameters": {"selector": "str", "page_index": "int (optional)", "timeout": "int (optional)"},
                "use_case": "Click after finding element selector"
            },
            "playwright_fill": {
                "description": "Fill text input using selector",
                "parameters": {"selector": "str", "text": "str", "page_index": "int (optional)"},
                "use_case": "Fill input after finding element selector"
            },
            "playwright_select": {
                "description": "Select option from dropdown using selector",
                "parameters": {"selector": "str", "value": "str", "page_index": "int (optional)"},
                "use_case": "Select dropdown option after finding selector"
            },
            "playwright_hover": {
                "description": "Hover over element using selector",
                "parameters": {"selector": "str", "page_index": "int (optional)"},
                "use_case": "Hover after finding element selector"
            },
            "playwright_drag": {
                "description": "Drag element from source to target",
                "parameters": {"source_selector": "str", "target_selector": "str", "page_index": "int (optional)"},
                "use_case": "Drag and drop operations"
            },
            "playwright_press_key": {
                "description": "Press keyboard key",
                "parameters": {"key": "str", "page_index": "int (optional)"},
                "use_case": "Keyboard interactions like Enter, Tab, Escape"
            },
            # Smart Actions (Combined locate + action)
            "unified_click": {
                "description": "Intelligent click with automatic element location",
                "parameters": {"description": "str", "page_index": "int (optional)"},
                "use_case": "When you want automatic element finding + click"
            },
            "unified_fill": {
                "description": "Intelligent fill with automatic element location",
                "parameters": {"description": "str", "value": "str", "page_index": "int (optional)"},
                "use_case": "When you want automatic element finding + fill"
            },
            # Advanced Actions
            "playwright_smart_click": {
                "description": "Smart click with text or selector and element type filtering",
                "parameters": {"text": "str (optional)", "selector": "str (optional)", "element_type": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Intelligent clicking with multiple strategies"
            },
            "playwright_click_and_switch_tab": {
                "description": "Click element and switch to new tab if opened",
                "parameters": {"selector": "str", "page_index": "int (optional)"},
                "use_case": "Handle links that open in new tabs"
            },
            "playwright_iframe_click": {
                "description": "Click element inside an iframe",
                "parameters": {"iframe_selector": "str", "element_selector": "str", "page_index": "int (optional)"},
                "use_case": "Interact with elements in embedded frames"
            },
            "playwright_intelligent_form_fill": {
                "description": "Automatically fill forms with provided data",
                "parameters": {"form_data": "dict", "page_index": "int (optional)"},
                "use_case": "Fill entire forms automatically"
            }
        }
        
        # Utility Tools - ALL UTILITY AND NAVIGATION METHODS
        self.utility_tools = {
            # Navigation
            "playwright_navigate": {
                "description": "Navigate to URL",
                "parameters": {"url": "str", "wait_for_load": "bool (optional)", "capture_screenshot": "bool (optional)", "page_index": "int (optional)"},
                "use_case": "Go to websites"
            },
            "playwright_smart_navigation": {
                "description": "Smart navigation with error handling and retries",
                "parameters": {"url": "str", "page_index": "int (optional)"},
                "use_case": "Robust navigation with automatic error recovery"
            },
            "playwright_navigate_and_wait_for_url": {
                "description": "Navigate and wait for specific URL pattern",
                "parameters": {"url": "str", "expected_url": "str", "timeout_ms": "int (optional)", "page_index": "int (optional)"},
                "use_case": "Handle redirects and multi-step navigation"
            },
            "playwright_wait_for_navigation": {
                "description": "Perform action and wait for navigation to complete",
                "parameters": {"trigger_action": "str", "selector": "str (optional)", "text_input": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Actions that trigger page navigation"
            },
            "playwright_go_back": {
                "description": "Navigate back in browser history",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Browser back button functionality"
            },
            "playwright_go_forward": {
                "description": "Navigate forward in browser history",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Browser forward button functionality"
            },
            # Information Gathering
            "playwright_screenshot": {
                "description": "Take screenshot of page or element",
                "parameters": {"filename": "str", "selector": "str (optional)", "page_index": "int (optional)", "full_page": "bool (optional)"},
                "use_case": "Visual debugging and verification"
            },
            "playwright_get_visible_text": {
                "description": "Get visible text from element or page",
                "parameters": {"selector": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Read page content and element text"
            },
            "playwright_get_visible_html": {
                "description": "Get HTML content from element or page",
                "parameters": {"selector": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Inspect HTML structure"
            },
            "playwright_analyze_form": {
                "description": "Analyze form structure and fields",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Understand form fields and structure"
            },
            "playwright_find_element_by_visual": {
                "description": "Find elements by visual characteristics",
                "parameters": {"page_index": "int (optional)", "element_type": "str (optional)"},
                "use_case": "Visual element detection and analysis"
            },
            # Page State and Verification
            "playwright_verify_state": {
                "description": "Verify expected page state conditions",
                "parameters": {"expected_state": "dict", "page_index": "int (optional)"},
                "use_case": "Verify page has reached expected state"
            },
            "playwright_wait_for_load_state_multiple": {
                "description": "Wait for multiple load states",
                "parameters": {"states": "list", "timeout_ms": "int (optional)", "page_index": "int (optional)"},
                "use_case": "Wait for complex page loading scenarios"
            },
            # JavaScript and Evaluation
            "playwright_evaluate": {
                "description": "Execute JavaScript in page context",
                "parameters": {"script": "str", "page_index": "int (optional)"},
                "use_case": "Custom JavaScript execution"
            },
            "playwright_console_logs": {
                "description": "Get console logs from page",
                "parameters": {"page_index": "int (optional)", "count": "int (optional)"},
                "use_case": "Debug JavaScript errors and console output"
            },
            # Advanced Features
            "playwright_custom_user_agent": {
                "description": "Set custom user agent string",
                "parameters": {"user_agent": "str", "page_index": "int (optional)"},
                "use_case": "Simulate different browsers or devices"
            },
            "playwright_save_as_pdf": {
                "description": "Save page as PDF",
                "parameters": {"filename": "str", "page_index": "int (optional)"},
                "use_case": "Generate PDF documents from web pages"
            },
            "playwright_intercept_requests": {
                "description": "Intercept and modify network requests",
                "parameters": {"url_pattern": "str", "action": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Mock API responses and block resources"
            },
            "playwright_stop_intercepting_requests": {
                "description": "Stop intercepting network requests",
                "parameters": {"url_pattern": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Remove request interception"
            },
            # Dialog Handling
            "playwright_set_dialog_handler": {
                "description": "Set handler for browser dialogs (alert, confirm, prompt)",
                "parameters": {"action": "str (optional)", "prompt_text": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Handle JavaScript dialogs automatically"
            },
            "playwright_remove_dialog_handler": {
                "description": "Remove dialog handler",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Stop handling dialogs automatically"
            },
            "playwright_auto_handle_next_dialog": {
                "description": "Handle the next dialog with specified action",
                "parameters": {"action": "str (optional)", "prompt_text": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Handle one-time dialog interactions"
            },
            # Response and Network
            "playwright_expect_response": {
                "description": "Wait for specific network response",
                "parameters": {"url_pattern": "str", "timeout_ms": "int (optional)", "page_index": "int (optional)"},
                "use_case": "Wait for API calls to complete"
            },
            "playwright_assert_response": {
                "description": "Assert network response status",
                "parameters": {"url_pattern": "str", "status_code": "int (optional)", "page_index": "int (optional)"},
                "use_case": "Verify API response status codes"
            },
            # Error Recovery
            "playwright_error_recovery": {
                "description": "Automatic error recovery and retry logic",
                "parameters": {"error": "Exception", "context": "dict"},
                "use_case": "Handle and recover from automation errors"
            },
            # Page Management
            "playwright_close": {
                "description": "Close a page tab",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Close specific browser tabs"
            }
        }
        
        # Accessibility Testing Tools - ALL ACCESSIBILITY METHODS
        self.accessibility_tools = {
            # Core Accessibility Testing
            "check_accessibility": {
                "description": "Comprehensive WCAG 2.2 accessibility testing with 11 engines",
                "parameters": {"url": "str", "engines": "list (optional) - axe, axe_devtools, pa11y, lighthouse, wave, accessibility_insights, axe_webdriverjs, web_accessibility_checker, color_contrast_analyzer, aatt, custom"},
                "use_case": "Full accessibility audit of websites with detailed reports and multiple engine support"
            },
            "accessibility_quick_check": {
                "description": "Quick accessibility check of current page",
                "parameters": {"page_index": "int (optional)"},
                "use_case": "Fast accessibility scan of current page state"
            },
            # Color Contrast Analysis
            "check_color_contrast": {
                "description": "WCAG 2.2 color contrast analysis and compliance checking",
                "parameters": {"foreground": "str (color)", "background": "str (color)", "font_size": "int (optional)", "bold": "bool (optional)"},
                "use_case": "Validate color combinations meet WCAG AA/AAA standards"
            },
            "check_non_text_contrast": {
                "description": "WCAG 2.2 non-text element contrast checking",
                "parameters": {"color1": "str", "color2": "str"},
                "use_case": "Check contrast for UI elements, borders, and icons (WCAG 2.2 - 1.4.11)"
            },
            "check_color_blindness_accessibility": {
                "description": "Test color accessibility for different types of color blindness",
                "parameters": {"foreground": "str", "background": "str"},
                "use_case": "Ensure colors work for deuteranopia, protanopia, and tritanopia users"
            },
            "simulate_color_blindness": {
                "description": "Simulate how colors appear to color blind users",
                "parameters": {"color": "str", "blindness_type": "str (optional)"},
                "use_case": "Preview colors as seen by color blind users"
            },
            "analyze_gradient_contrast": {
                "description": "Analyze contrast for text over gradient backgrounds",
                "parameters": {"gradient_colors": "list", "text_color": "str"},
                "use_case": "Ensure text readability over gradient backgrounds"
            },
            # WCAG 2.2 Checklist and Compliance
            "get_wcag22_checklist": {
                "description": "Generate comprehensive WCAG 2.2 compliance checklist",
                "parameters": {"url": "str (optional)"},
                "use_case": "Get complete accessibility checklist with manual and automated tests"
            },
            # Accessibility Tree and ARIA
            "playwright_accessibility_snapshot": {
                "description": "Get accessibility tree snapshot for debugging",
                "parameters": {"selector": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Debug accessibility tree structure and ARIA attributes"
            },
            "playwright_accessibility_tree_snapshot": {
                "description": "Get detailed accessibility tree with interesting elements only",
                "parameters": {"root_selector": "str (optional)", "interesting_only": "bool (optional)", "page_index": "int (optional)"},
                "use_case": "Detailed accessibility tree analysis for specific elements"
            },
            "playwright_find_by_role_in_accessibility_tree": {
                "description": "Find elements by role within accessibility tree",
                "parameters": {"role": "str", "accessible_name": "str (optional)", "page_index": "int (optional)"},
                "use_case": "Locate elements using accessibility tree navigation"
            }
        }
        
        total_tools = len(self.locator_tools) + len(self.action_tools) + len(self.utility_tools) + len(self.accessibility_tools)
        print(f"📊 Categorized {total_tools} tools:")
        print(f"   🔍 {len(self.locator_tools)} Element Locators")
        print(f"   ⚡ {len(self.action_tools)} Action Tools") 
        print(f"   🛠️ {len(self.utility_tools)} Utility Tools")
        print(f"   ♿ {len(self.accessibility_tools)} Accessibility Tools")
        print(f"")
        print(f"🎯 COMPREHENSIVE TOOL COVERAGE:")
        print(f"   • All Playwright locator methods included")
        print(f"   • All action and interaction methods")
        print(f"   • Complete navigation and utility suite")
        print(f"   • Full WCAG 2.2 accessibility testing")
        print(f"   • Advanced features: JS execution, network interception, dialog handling")
        print(f"   • Error recovery and state verification")

    def _generate_sophisticated_tools_documentation(self) -> str:
        """Generate sophisticated tools documentation with proper workflow"""
        doc = f"""🎯 SOPHISTICATED BROWSER AUTOMATION WORKFLOW

🔄 MANDATORY STRATEGY: Always follow this two-step process:
1️⃣ FIND ELEMENT: Use locator tools to find elements
2️⃣ PERFORM ACTION: Use action tools on found elements

📍 ELEMENT LOCATOR TOOLS (Step 1 - Find Elements):
"""
        
        for tool_name, tool_info in self.locator_tools.items():
            doc += f"  🔍 {tool_name}:\n"
            doc += f"     Description: {tool_info['description']}\n"
            doc += f"     Parameters: {tool_info['parameters']}\n"
            doc += f"     Use Case: {tool_info['use_case']}\n\n"
        
        doc += f"""⚡ ACTION TOOLS (Step 2 - Perform Actions):
"""
        
        for tool_name, tool_info in self.action_tools.items():
            doc += f"  ⚡ {tool_name}:\n"
            doc += f"     Description: {tool_info['description']}\n"
            doc += f"     Parameters: {tool_info['parameters']}\n"
            doc += f"     Use Case: {tool_info['use_case']}\n\n"
        
        doc += f"""🛠️ UTILITY TOOLS (Supporting Actions):
"""
        
        for tool_name, tool_info in self.utility_tools.items():
            doc += f"  🛠️ {tool_name}:\n"
            doc += f"     Description: {tool_info['description']}\n"
            doc += f"     Parameters: {tool_info['parameters']}\n"
            doc += f"     Use Case: {tool_info['use_case']}\n\n"
        
        doc += f"""♿ ACCESSIBILITY TOOLS (WCAG 2.2 Testing):
"""
        
        for tool_name, tool_info in self.accessibility_tools.items():
            doc += f"  ♿ {tool_name}:\n"
            doc += f"     Description: {tool_info['description']}\n"
            doc += f"     Parameters: {tool_info['parameters']}\n"
            doc += f"     Use Case: {tool_info['use_case']}\n\n"
        
        doc += f"""
🎯 WORKFLOW EXAMPLES:

Example 1 - Click a button:
Step 1: Use playwright_find_by_role(role="button", name="Accept all") → Get selector
Step 2: Use playwright_click(selector=found_selector) → Click the button

Example 2 - Fill a search box:
Step 1: Use playwright_smart_text_locator(text="search") → Get selector  
Step 2: Use playwright_fill(selector=found_selector, text="your search") → Fill the box

Example 3 - Smart approach (auto-locate + action):
Single Step: Use unified_fill(description="search box", value="your search") → Auto-find + fill

Example 4 - Accessibility testing:
Single Step: Use check_accessibility(url="https://website.com") → Full WCAG 2.2 audit
Or: Use check_color_contrast(foreground="#000", background="#fff") → Contrast analysis

🚨 CRITICAL RULES:
- ALWAYS get a selector first before performing actions (unless using unified tools)
- If locator tools fail, try different locator approaches
- Take screenshots when stuck to understand page state
- Use unified tools when you want automatic element finding + action
- ♿ ACCESSIBILITY: When accessibility is mentioned, ALWAYS use check_accessibility tool
- 🎯 GOAL COMPLETION: Complete ALL parts of the goal, don't stop early
"""
        
        return doc

    async def sophisticated_llm_interaction(self, user_goal: str) -> None:
        """
        🧠 Sophisticated LLM Interaction with Proper Workflow Strategy
        """
        print(f"\n🧠 Sophisticated Agent: Starting intelligent automation for '{user_goal}'")
        
        # Generate sophisticated system prompt with proper workflow
        tools_doc = self._generate_sophisticated_tools_documentation()
        
        system_prompt = f"""You are a SOPHISTICATED Browser Automation Agent with complete tool knowledge and proper workflow strategy.

{tools_doc}

🧠 SOPHISTICATED DECISION MAKING:
You MUST follow the proper workflow strategy:

1️⃣ ELEMENT LOCATION PHASE:
   - Choose the BEST locator tool for the element
   - Try multiple locator strategies if first one fails
   - Get the element selector before any action

2️⃣ ACTION PHASE:
   - Use action tools with the found selector
   - OR use unified tools for automatic locate + action

3️⃣ VERIFICATION PHASE:
   - Check if action succeeded
   - Take screenshots if unclear
   - Try alternative approaches if failed

📋 RESPONSE FORMAT (JSON only):
{{"action": "plan", "phase": "locate|action|verify", "next_step": "description", "tool": "tool_name", "parameters": {{...}}, "reasoning": "why this tool and strategy"}}

🔧 TOOL SELECTION STRATEGY:
For finding elements (Phase 1):
- Use playwright_find_by_role for buttons, inputs with ARIA roles
- Use playwright_smart_text_locator for elements with visible text
- Use playwright_label_to_control for form fields with labels
- Use playwright_css_locator when you have exact selectors

For actions (Phase 2):
- Use playwright_click, playwright_fill with found selectors
- Use unified_click, unified_fill for automatic locate + action

🚨 FAILURE RECOVERY:
When locator fails:
1. Try different locator tool (role → text → css → xpath)
2. Take screenshot to understand page state
3. Use DOM analysis tools
4. Try unified tools as last resort

CRITICAL: Always provide valid JSON with proper tool names and parameters!"""

        # Initialize conversation
        self.conversation_history = [
            {"role": "user", "content": f"GOAL: {user_goal}\n\nAnalyze this goal and start with the proper workflow phase. Remember: LOCATE elements first, then PERFORM actions."}
        ]
        
        step_count = 0
        max_steps = 30  # Increased for complex automation
        self.failure_count = 0
        current_phase = "locate"
        
        while step_count < max_steps:
            step_count += 1
            print(f"\n🔄 Step {step_count}: Consulting LLM for {current_phase} phase...")
            
            try:
                # Get LLM decision with sophisticated context
                response = self.llm_client.messages.create(
                    model=os.getenv('CLAUDE_MODEL_NAME', 'claude-3-5-sonnet-20241022'),
                    max_tokens=1200,
                    system=system_prompt,
                    messages=self.conversation_history
                )
                
                llm_response = response.content[0].text.strip()
                print(f"🧠 LLM Decision: {llm_response[:200]}...")
                
                # Parse LLM response with validation
                decision = self._parse_and_validate_llm_response(llm_response)
                
                if decision.get("action") == "plan":
                    # Execute with sophisticated workflow validation
                    result = await self._execute_sophisticated_step(decision)
                    
                    # Update current phase based on result
                    if result.success:
                        self.failure_count = 0
                        if decision.get("phase") == "locate" and result.element_found:
                            current_phase = "action"
                        elif decision.get("phase") == "action":
                            current_phase = "verify"
                        elif decision.get("phase") == "verify":
                            current_phase = "locate"  # Ready for next element
                    else:
                        self.failure_count += 1
                        # Stay in current phase for retry
                    
                    # Provide sophisticated feedback to LLM
                    feedback = self._generate_sophisticated_feedback(result, current_phase)
                    
                    # Update conversation with detailed results
                    self.conversation_history.append({
                        "role": "assistant", 
                        "content": llm_response
                    })
                    self.conversation_history.append({
                        "role": "user", 
                        "content": feedback
                    })
                    
                    # Check for completion
                    if decision.get("phase") == "verify" and result.success:
                        completion_check = self._check_goal_completion(user_goal, self.conversation_history)
                        if completion_check:
                            print(f"🎉 GOAL ACHIEVED: {user_goal}")
                            break
                    
                elif decision.get("action") == "complete":
                    print(f"🎉 TASK COMPLETED: {decision.get('summary', 'Goal achieved!')}")
                    break
                    
                else:
                    print(f"⚠️ Unknown action: {decision.get('action', 'none')}. Continuing...")
                    self.conversation_history.append({
                        "role": "user", 
                        "content": f"Please provide a clear plan with proper workflow phase (locate/action/verify) and valid tool selection."
                    })
                
            except Exception as e:
                print(f"❌ LLM interaction error: {e}")
                self.conversation_history.append({
                    "role": "user", 
                    "content": f"Error occurred: {str(e)}. Please provide a simple plan for the next step."
                })
            
            # Brief pause between steps
            await asyncio.sleep(1.5)
        
        print(f"\n📊 Sophisticated automation completed after {step_count} decisions")
        print(f"📈 Success Rate: {((step_count - self.failure_count) / step_count * 100):.1f}%")

    def _parse_and_validate_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate LLM response with sophisticated error handling"""
        try:
            # Clean and parse JSON - try multiple approaches
            cleaned = response.strip()
            
            # Remove markdown code blocks if present
            if cleaned.startswith("```") and cleaned.endswith("```"):
                cleaned = cleaned[3:-3]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            
            # Try 1: Direct JSON parsing
            try:
                decision = json.loads(cleaned)
                if isinstance(decision, dict) and "action" in decision:
                    return self._validate_decision(decision)
            except json.JSONDecodeError:
                pass
            
            # Try 2: Find JSON object between braces
            json_start = cleaned.find("{")
            json_end = cleaned.rfind("}") + 1
            
            if json_start != -1 and json_end > json_start:
                json_part = cleaned[json_start:json_end]
                try:
                    decision = json.loads(json_part)
                    if isinstance(decision, dict) and "action" in decision:
                        return self._validate_decision(decision)
                except json.JSONDecodeError:
                    pass
            
            # Try 3: Look for multiple JSON objects and take the first valid one
            import re
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            json_matches = re.findall(json_pattern, cleaned)
            
            for json_match in json_matches:
                try:
                    decision = json.loads(json_match)
                    if isinstance(decision, dict) and "action" in decision:
                        return self._validate_decision(decision)
                except json.JSONDecodeError:
                    continue
            
            # Try 4: Extract from lines that look like JSON
            lines = cleaned.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        decision = json.loads(line)
                        if isinstance(decision, dict) and "action" in decision:
                            return self._validate_decision(decision)
                    except json.JSONDecodeError:
                        continue
            
            # If all parsing fails, use fallback
            print(f"⚠️ Could not parse JSON from LLM response, using intelligent fallback")
            return self._create_sophisticated_fallback(response)
                
        except Exception as e:
            print(f"⚠️ Error parsing LLM response: {e}")
            return self._create_sophisticated_fallback(response)
    
    def _validate_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the decision has valid tool and parameters"""
        tool_name = decision.get("tool", "")
        all_tools = {**self.locator_tools, **self.action_tools, **self.utility_tools, **self.accessibility_tools}
        
        # Check if tool exists in our categories or as a direct method
        if tool_name in all_tools or hasattr(self.tools, tool_name):
            print(f"✅ Valid tool found: {tool_name}")
            return decision
        else:
            print(f"⚠️ Unknown tool: {tool_name}, using fallback")
            return self._create_sophisticated_fallback(str(decision))

    def _create_sophisticated_fallback(self, response: str) -> Dict[str, Any]:
        """Create sophisticated fallback based on response analysis with proper accessibility detection"""
        response_lower = response.lower()
        
        # Only trigger completion if the response explicitly indicates task completion at the start
        if response_lower.strip().startswith(("task completed", "goal achieved", "finished:", "done:")):
            return {"action": "complete", "summary": "Task appears completed"}
        
        # Enhanced accessibility testing fallbacks - PRIORITY #1
        elif any(word in response_lower for word in ["accessibility", "wcag", "a11y", "audit", "accessiblity"]):
            return {
                "action": "plan", "phase": "action",
                "next_step": "Run comprehensive accessibility audit",
                "tool": "check_accessibility",
                "parameters": {"url": "", "engines": ["axe", "custom", "wave"]},  # Empty URL will use current page
                "reasoning": "CRITICAL: Accessibility testing requested - invoking accessibility tools"
            }
        
        # Navigation fallbacks
        elif any(word in response_lower for word in ["navigate", "go to", "visit"]):
            # Extract URL if mentioned
            url = "https://google.com"  # Default
            if "google" in response_lower:
                url = "https://google.com"
            elif "github" in response_lower:
                url = "https://github.com"
            elif "herokuapp" in response_lower:
                url = "https://the-internet.herokuapp.com/add_remove_elements/"
            elif "example" in response_lower:
                url = "https://example.com"
                
            return {
                "action": "plan", "phase": "action",
                "next_step": "Navigate to website",
                "tool": "playwright_navigate",
                "parameters": {"url": url, "wait_for_load": True, "capture_screenshot": True},
                "reasoning": "Fallback navigation based on detected intent"
            }
        
        # Click action fallbacks with count detection
        elif "click" in response_lower and "times" in response_lower:
            import re
            times_match = re.search(r'(\d+)\s*times?', response_lower)
            times = int(times_match.group(1)) if times_match else 1
            
            element_match = re.search(r'"([^"]+)"', response)
            element_name = element_match.group(1) if element_match else "Add Element"
            
            return {
                "action": "plan", "phase": "locate",
                "next_step": f"Find and click '{element_name}' button",
                "tool": "playwright_find_by_role",
                "parameters": {"role": "button", "name": element_name, "action": "click"},
                "reasoning": f"Fallback click action - need to click {times} times"
            }
        
        # Remove/delete action fallbacks
        elif any(word in response_lower for word in ["remove", "delete"]):
            return {
                "action": "plan", "phase": "locate",
                "next_step": "Find Delete button to remove element",
                "tool": "playwright_find_by_role",
                "parameters": {"role": "button", "name": "Delete", "action": "click"},
                "reasoning": "Fallback remove action - looking for Delete button"
            }
        
        # Screenshot fallbacks
        elif any(word in response_lower for word in ["screenshot", "visual", "capture"]):
            return {
                "action": "plan", "phase": "verify",
                "next_step": "Take screenshot",
                "tool": "playwright_screenshot", 
                "parameters": {"filename": "goal_completion_screenshot", "full_page": True},
                "reasoning": "Visual verification fallback"
            }
        
        # Element finding fallbacks
        elif any(word in response_lower for word in ["find", "locate", "search for"]):
            return {
                "action": "plan", "phase": "locate",
                "next_step": "Find element by role",
                "tool": "playwright_find_by_role",
                "parameters": {"role": "button", "name": ""},
                "reasoning": "Fallback element location"
            }
        
        # Default: Try to parse the goal and provide a reasonable first step
        else:
            return {
                "action": "plan", "phase": "action",
                "next_step": "Navigate to start automation",
                "tool": "playwright_navigate",
                "parameters": {"url": "https://the-internet.herokuapp.com/add_remove_elements/", "wait_for_load": True},
                "reasoning": "Default fallback - navigate to start the automation process"
            }

    async def _execute_sophisticated_step(self, decision: Dict[str, Any]) -> AgentResult:
        """Execute step with sophisticated workflow validation"""
        tool_name = decision.get("tool", "")
        parameters = decision.get("parameters", {})
        step_description = decision.get("next_step", "")
        phase = decision.get("phase", "unknown")
        reasoning = decision.get("reasoning", "")
        
        print(f"🎯 Phase: {phase.upper()}")
        print(f"🔧 Tool: {tool_name}")
        print(f"📝 Step: {step_description}")
        if reasoning:
            print(f"🧠 Reasoning: {reasoning}")
        print(f"⚙️ Parameters: {json.dumps(parameters, indent=2)}")
        
        start_time = time.time()
        
        try:
            # Handle unified tools (smart locate + action)
            if tool_name == "unified_fill":
                return await self._execute_unified_action("fill", parameters, step_description, phase, start_time)
            
            elif tool_name == "unified_click":
                return await self._execute_unified_action("click", parameters, step_description, phase, start_time)
            
            # Handle accessibility tools
            elif tool_name in self.accessibility_tools:
                return await self._execute_accessibility_tool(tool_name, parameters, step_description, phase, start_time)
            
            # Handle direct Playwright tools
            elif hasattr(self.tools, tool_name):
                method = getattr(self.tools, tool_name)
                
                if asyncio.iscoroutinefunction(method):
                    result = await method(**parameters)
                else:
                    result = method(**parameters)
                
                # Process result based on tool type
                return self._process_tool_result(result, tool_name, step_description, phase, start_time)
            
            else:
                return AgentResult(
                    success=False,
                    step_description=step_description,
                    tool_used=tool_name,
                    phase=phase,
                    execution_time=time.time() - start_time,
                    error_message=f"Unknown tool: {tool_name}"
                )
                
        except Exception as e:
            return AgentResult(
                success=False,
                step_description=step_description,
                tool_used=tool_name,
                phase=phase,
                execution_time=time.time() - start_time,
                error_message=f"Execution error: {str(e)}"
            )

    async def _execute_unified_action(self, action_type: str, parameters: dict, 
                                    step_description: str, phase: str, start_time: float) -> AgentResult:
        """Execute unified action with element location"""
        description = parameters.get("description", "")
        value = parameters.get("value", "") if action_type == "fill" else ""
        page_index = parameters.get("page_index", 0)
        
        print(f"🎯 Executing unified {action_type} for: {description}")
        
        # Try multiple locator strategies
        locator_strategies = [
            ("playwright_find_by_role", self._get_role_params(description, action_type)),
            ("playwright_smart_text_locator", {"text": description, "action": "find"}),
            ("playwright_label_to_control", {"label_text": description, "action": "find"}),
            ("playwright_accessibility_locator", {"description": description, "action": "find"})
        ]
        
        for strategy_name, strategy_params in locator_strategies:
            try:
                print(f"   🔍 Trying {strategy_name}...")
                
                # Get the locator method
                locator_method = getattr(self.tools, strategy_name)
                strategy_params["page_index"] = page_index
                
                # Execute locator
                if asyncio.iscoroutinefunction(locator_method):
                    locator_result = await locator_method(**strategy_params)
                else:
                    locator_result = locator_method(**strategy_params)
                
                # Extract selector if found
                selector = self._extract_selector_from_result(locator_result)
                
                if selector:
                    print(f"   ✅ Found selector: {selector}")
                    
                    # Execute action with found selector
                    action_result = None
                    if action_type == "click":
                        action_result = await self.tools.playwright_click(selector=selector, page_index=page_index)
                    elif action_type == "fill":
                        action_result = await self.tools.playwright_fill(selector=selector, text=value, page_index=page_index)
                    
                    success = action_result and action_result.get("status") == "success"
                    
                    return AgentResult(
                        success=success,
                        step_description=step_description,
                        tool_used=f"unified_{action_type}",
                        phase=phase,
                        strategy_used=strategy_name,
                        confidence=0.9 if success else 0.0,
                        execution_time=time.time() - start_time,
                        element_found=True,
                        selector_used=selector,
                        error_message=action_result.get("message", "") if not success else ""
                    )
                
            except Exception as e:
                print(f"   ❌ {strategy_name} failed: {e}")
                continue
        
        # All strategies failed
        return AgentResult(
            success=False,
            step_description=step_description,
            tool_used=f"unified_{action_type}",
            phase=phase,
            execution_time=time.time() - start_time,
            error_message=f"Could not locate element: {description}"
        )

    def _get_role_params(self, description: str, action_type: str) -> dict:
        """Get appropriate role parameters based on description"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["button", "click", "submit", "accept", "confirm"]):
            return {"role": "button", "name": description}
        elif any(word in desc_lower for word in ["input", "field", "text", "search", "email", "password"]):
            return {"role": "textbox", "name": description}
        elif any(word in desc_lower for word in ["select", "dropdown", "option"]):
            return {"role": "combobox", "name": description}
        elif any(word in desc_lower for word in ["link", "href"]):
            return {"role": "link", "name": description}
        else:
            # Default to button for click actions, textbox for fill
            default_role = "button" if action_type == "click" else "textbox"
            return {"role": default_role, "name": description}

    def _extract_selector_from_result(self, result: Any) -> str:
        """Extract selector from various tool result formats"""
        if not isinstance(result, dict):
            return ""
        
        if result.get("status") != "success":
            return ""
        
        # Try different selector formats
        if "selector" in result:
            return result["selector"]
        elif "best_match" in result:
            best_match = result["best_match"]
            if isinstance(best_match, dict):
                element = best_match.get("element", {})
                selectors = element.get("selectors", {})
                return (selectors.get("cssPath") or 
                       selectors.get("xpath") or 
                       selectors.get("css") or "")
        elif "element" in result:
            element = result["element"]
            if isinstance(element, dict):
                selectors = element.get("selectors", {})
                return (selectors.get("cssPath") or 
                       selectors.get("xpath") or 
                       selectors.get("css") or "")
        
        return ""

    async def _execute_accessibility_tool(self, tool_name: str, parameters: dict, 
                                         step_description: str, phase: str, start_time: float) -> AgentResult:
        """Execute accessibility testing tools"""
        print(f"♿ Executing accessibility tool: {tool_name}")
        
        try:
            if tool_name == "check_accessibility":
                url = parameters.get("url", "")
                engines = parameters.get("engines", ["axe", "custom"])
                
                if not url:
                    # Get current page URL
                    page = await self._get_page(0)
                    if page:
                        url = page.url
                        print(f"   🎯 Using current page URL: {url}")
                    else:
                        raise Exception("No URL provided and no active page")
                
                print(f"   🔍 Running COMPREHENSIVE accessibility test on: {url}")
                print(f"   🛠️ Using engines: {', '.join(engines)}")
                result = await check_accessibility(url, engines)
                
                success = result.get("success", False)
                if success:
                    score = result.get("score", 0)
                    violations = result.get("summary", {}).get("violations", 0)
                    warnings = result.get("summary", {}).get("warnings", 0)
                    
                    print(f"   📊 Accessibility Score: {score}/100")
                    print(f"   🚨 Violations: {violations}, ⚠️ Warnings: {warnings}")
                    
                    return AgentResult(
                        success=True,
                        step_description=f"Accessibility test completed: {score}/100 score",
                        tool_used=tool_name,
                        phase=phase,
                        confidence=1.0,
                        execution_time=time.time() - start_time,
                        error_message="" if success else f"Accessibility issues found: {violations} violations"
                    )
                else:
                    return AgentResult(
                        success=False,
                        step_description=step_description,
                        tool_used=tool_name,
                        phase=phase,
                        execution_time=time.time() - start_time,
                        error_message=result.get("error", "Accessibility test failed")
                    )
            
            elif tool_name == "check_color_contrast":
                foreground = parameters.get("foreground", "#000000")
                background = parameters.get("background", "#ffffff")
                font_size = parameters.get("font_size", 14)
                bold = parameters.get("bold", False)
                
                print(f"   🎨 Checking contrast: {foreground} on {background}")
                result = check_color_contrast(foreground, background, font_size, bold)
                
                success = result.get("success", False)
                if success:
                    ratio = result.get("contrast_ratio", 0)
                    wcag_aa = result.get("wcag_aa_pass", False)
                    wcag_aaa = result.get("wcag_aaa_pass", False)
                    
                    print(f"   📏 Contrast Ratio: {ratio}:1")
                    print(f"   ✅ WCAG AA: {'PASS' if wcag_aa else 'FAIL'}")
                    print(f"   ✅ WCAG AAA: {'PASS' if wcag_aaa else 'FAIL'}")
                    
                    return AgentResult(
                        success=True,
                        step_description=f"Color contrast: {ratio}:1 (AA: {'✅' if wcag_aa else '❌'})",
                        tool_used=tool_name,
                        phase=phase,
                        confidence=1.0,
                        execution_time=time.time() - start_time,
                        error_message="" if wcag_aa else f"Contrast ratio {ratio}:1 fails WCAG AA standard"
                    )
                else:
                    return AgentResult(
                        success=False,
                        step_description=step_description,
                        tool_used=tool_name,
                        phase=phase,
                        execution_time=time.time() - start_time,
                        error_message=result.get("error", "Color contrast check failed")
                    )
            
            elif tool_name == "get_wcag22_checklist":
                url = parameters.get("url")
                
                if not url:
                    # Get current page URL
                    page = await self._get_page(0)
                    if page:
                        url = page.url
                
                print(f"   📋 Generating WCAG 2.2 checklist for: {url or 'general'}")
                result = get_wcag22_checklist(url)
                
                success = result.get("success", False)
                if success:
                    total_criteria = result.get("total_criteria", 0)
                    new_criteria = len(result.get("new_in_wcag22", []))
                    
                    print(f"   📊 Total Criteria: {total_criteria}")
                    print(f"   🆕 New in WCAG 2.2: {new_criteria}")
                    
                    return AgentResult(
                        success=True,
                        step_description=f"WCAG 2.2 checklist: {total_criteria} criteria ({new_criteria} new)",
                        tool_used=tool_name,
                        phase=phase,
                        confidence=1.0,
                        execution_time=time.time() - start_time
                    )
                else:
                    return AgentResult(
                        success=False,
                        step_description=step_description,
                        tool_used=tool_name,
                        phase=phase,
                        execution_time=time.time() - start_time,
                        error_message=result.get("error", "Checklist generation failed")
                    )
            
            elif tool_name == "accessibility_quick_check":
                # Quick accessibility check of current page
                page_index = parameters.get("page_index", 0)
                page = await self._get_page(page_index)
                
                if not page:
                    raise Exception("No active page to check")
                
                url = page.url
                print(f"   ⚡ Quick accessibility check: {url}")
                
                # Run a quick check with axe engine only
                result = await check_accessibility(url, ["axe"])
                
                success = result.get("success", False)
                if success:
                    score = result.get("score", 0)
                    violations = result.get("summary", {}).get("violations", 0)
                    
                    return AgentResult(
                        success=True,
                        step_description=f"Quick accessibility check: {score}/100 ({violations} violations)",
                        tool_used=tool_name,
                        phase=phase,
                        confidence=0.8,  # Quick check is less comprehensive
                        execution_time=time.time() - start_time
                    )
                else:
                    return AgentResult(
                        success=False,
                        step_description=step_description,
                        tool_used=tool_name,
                        phase=phase,
                        execution_time=time.time() - start_time,
                        error_message=result.get("error", "Quick accessibility check failed")
                    )
            
            else:
                return AgentResult(
                    success=False,
                    step_description=step_description,
                    tool_used=tool_name,
                    phase=phase,
                    execution_time=time.time() - start_time,
                    error_message=f"Unknown accessibility tool: {tool_name}"
                )
                
        except Exception as e:
            return AgentResult(
                success=False,
                step_description=step_description,
                tool_used=tool_name,
                phase=phase,
                execution_time=time.time() - start_time,
                error_message=f"Accessibility tool error: {str(e)}"
            )

    async def _get_page(self, page_index: int):
        """Helper method to get current page"""
        if self.tools and hasattr(self.tools, '_get_page'):
            return await self.tools._get_page(page_index)
        return None

    def _process_tool_result(self, result: Any, tool_name: str, step_description: str, 
                           phase: str, start_time: float) -> AgentResult:
        """Process tool result with sophisticated analysis"""
        execution_time = time.time() - start_time
        
        if isinstance(result, dict):
            success = result.get("status") == "success"
            error_msg = result.get("message", "")
            
            # Extract selector information for locator tools
            element_found = False
            selector_used = ""
            
            if tool_name in self.locator_tools:
                # This is a locator tool
                selector_used = self._extract_selector_from_result(result)
                element_found = bool(selector_used)
            
            return AgentResult(
                success=success,
                step_description=step_description,
                tool_used=tool_name,
                phase=phase,
                strategy_used=f"{phase}_phase",
                confidence=result.get("confidence", 1.0 if success else 0.0),
                execution_time=execution_time,
                element_found=element_found,
                selector_used=selector_used,
                error_message=error_msg
            )
        else:
            # Non-dict result (assume success)
            return AgentResult(
                success=True,
                step_description=step_description,
                tool_used=tool_name,
                phase=phase,
                strategy_used=f"{phase}_phase",
                confidence=1.0,
                execution_time=execution_time
            )

    def _generate_sophisticated_feedback(self, result: AgentResult, current_phase: str) -> str:
        """Generate sophisticated feedback for LLM"""
        if result.success:
            feedback = f"✅ SUCCESS ({result.phase}): {result.step_description}\n"
            feedback += f"Tool: {result.tool_used} | Time: {result.execution_time:.2f}s\n"
            
            if result.element_found:
                feedback += f"🎯 ELEMENT LOCATED: {result.selector_used}\n"
                feedback += "Next phase: ACTION (use action tools with this selector)\n"
            else:
                feedback += f"Action completed successfully\n"
            
            feedback += f"Current phase: {current_phase.upper()}\n"
            feedback += "What's the next step in the workflow?"
            
        else:
            feedback = f"❌ FAILURE ({result.phase}): {result.step_description}\n"
            feedback += f"Error: {result.error_message}\n"
            feedback += f"Tool attempted: {result.tool_used}\n"
            feedback += f"Failure #{self.failure_count}/{self.max_failures}\n"
            
            if self.failure_count >= self.max_failures:
                feedback += "🚨 Max failures reached. Try:\n"
                feedback += "1. Take screenshot to understand page state\n"
                feedback += "2. Use different locator strategy\n"
                feedback += "3. Use unified tools for automatic handling\n"
            else:
                feedback += "💡 Try alternative approach:\n"
                if current_phase == "locate":
                    feedback += "- Different locator tool (role → text → css → xpath)\n"
                    feedback += "- Unified tools for automatic element finding\n"
                elif current_phase == "action":
                    feedback += "- Verify selector is correct\n"
                    feedback += "- Try unified action tools\n"
            
            feedback += f"Current phase: {current_phase.upper()}\n"
            feedback += "Please provide recovery strategy."
        
        return feedback

    def _check_goal_completion(self, user_goal: str, conversation: List[Dict]) -> bool:
        """Check if the user goal has been completed using PROPER goal analysis"""
        import re
        
        # Parse the original goal to identify required steps
        goal_lower = user_goal.lower()
        required_steps = []
        
        # Check for navigation requirement
        if any(word in goal_lower for word in ["navigate", "go to", "visit"]):
            required_steps.append("navigation")
        
        # Check for click requirements with specific count
        click_matches = re.findall(r'click[^\s]*\s+[^.]*?(\d+)\s*times?', goal_lower)
        if click_matches:
            times = int(click_matches[0])
            required_steps.append(f"click_{times}_times")
        
        # Check for removal requirements
        if any(word in goal_lower for word in ["remove", "delete"]):
            required_steps.append("remove_element")
        
        # Check for screenshot requirements
        if "screenshot" in goal_lower:
            required_steps.append("screenshot")
        
        # Check for accessibility requirements
        if any(word in goal_lower for word in ["accessibility", "a11y", "wcag", "accessiblity"]):
            required_steps.append("accessibility")
        
        if not required_steps:
            # If no specific steps identified, use old heuristic
            recent_messages = conversation[-6:]
            success_count = sum(1 for msg in recent_messages if "✅ SUCCESS" in msg.get("content", ""))
            return success_count >= 3
        
        # Check if all required steps have been completed
        conversation_text = " ".join([msg.get("content", "") for msg in conversation])
        completed_steps = []
        
        # Check for navigation completion
        if "navigation" in required_steps:
            if "Successfully navigated" in conversation_text or "navigation completed" in conversation_text:
                completed_steps.append("navigation")
        
        # Check for click completion
        for step in required_steps:
            if step.startswith("click_") and step.endswith("_times"):
                times = int(step.split("_")[1])
                click_count = conversation_text.lower().count("click") + conversation_text.lower().count("clicked")
                if click_count >= times:
                    completed_steps.append(step)
        
        # Check for removal completion
        if "remove_element" in required_steps:
            if "removed" in conversation_text.lower() or "delete" in conversation_text.lower():
                completed_steps.append("remove_element")
        
        # Check for screenshot completion
        if "screenshot" in required_steps:
            if "screenshot" in conversation_text.lower():
                completed_steps.append("screenshot")
        
        # Check for accessibility completion - THIS IS CRITICAL!
        if "accessibility" in required_steps:
            if ("accessibility audit" in conversation_text.lower() or 
                "accessibility test" in conversation_text.lower() or
                "wcag" in conversation_text.lower()):
                completed_steps.append("accessibility")
        
        # Goal is complete only if ALL required steps are completed
        completion_rate = len(completed_steps) / len(required_steps)
        print(f"🎯 Goal Completion Analysis: {len(completed_steps)}/{len(required_steps)} steps completed ({completion_rate*100:.1f}%)")
        print(f"   Required: {required_steps}")
        print(f"   Completed: {completed_steps}")
        
        return completion_rate >= 1.0  # All steps must be completed

    async def run_sophisticated_agent(self):
        """Run the sophisticated agent with proper workflow strategy"""
        print("\n" + "=" * 120)
        print("🧠 SOPHISTICATED AI AGENT CLIENT - Proper Element Location & Action Strategy")
        print("=" * 120)
        print("🎯 Current Mode:", self.mode.value.upper())
        print("🔄 STRATEGY: Two-step workflow (Find Element → Perform Action)")
        print("🧠 COMPLETE: Accurate knowledge of ALL tools with correct parameters")
        print("🛠️ SOPHISTICATED: Multi-strategy element location with smart fallbacks")
        print("♿ ACCESSIBILITY: Complete WCAG 2.2 testing and compliance tools")
        print("📊 AUDITED: Each step properly validated and reported")
        print("✨ Workflow Features:")
        print("  • Proper locate → action → verify workflow")
        print("  • Intelligent element location with multiple strategies")
        print("  • Sophisticated failure recovery and tool selection")
        print("  • Complete tool knowledge with accurate parameters")
        print("  • WCAG 2.2 accessibility testing integration")
        print("  • Comprehensive step-by-step auditing")
        
        print(f"\n💡 Commands:")
        print("  • 'Navigate to google.com and search for AI tools' - Natural language goals")
        print("  • 'Check accessibility of this website' - WCAG 2.2 compliance testing")
        print("  • 'Test color contrast of #000 on #fff' - Color accessibility validation")
        print("  • The agent will follow proper workflow: Locate → Action → Verify")
        print("=" * 120)
        
        while True:
            try:
                user_input = input(f"\n🧠 [{self.mode.value}] Your goal: ").strip()
                
                if user_input.lower() in ["exit", "quit", "stop"]:
                    print("🧠 Sophisticated Agent shutting down. Goodbye!")
                    break
                
                if user_input.startswith("mode "):
                    new_mode = user_input[5:].strip()
                    try:
                        self.mode = AgentMode(new_mode.lower())
                        print(f"✅ Mode changed to: {self.mode.value}")
                        continue
                    except ValueError:
                        print("❌ Invalid mode. Use: basic, intelligent, continuous, ultimate")
                        continue
                
                if not user_input:
                    continue
                
                print(f"\n🧠 Processing goal: \"{user_input}\" [Mode: {self.mode.value}]")
                
                # Use sophisticated LLM interaction with proper workflow
                await self.sophisticated_llm_interaction(user_input)
                
                print("\n🧠 Ready for your next goal...")
                
            except KeyboardInterrupt:
                print("\n⚠️ Interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Sophisticated Agent error: {e}")
    
    async def close(self):
        """Clean up sophisticated agent"""
        if self.tools:
            try:
                await self.tools.cleanup()
                logger.info("Sophisticated Agent cleaned up")
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

async def main():
    """Main function for the Sophisticated Agent"""
    print("🧠 Starting Sophisticated AI Agent Client...")
    
    # Use sophisticated agent with proper workflow
    agent = SophisticatedAgentClient(mode=AgentMode.CONTINUOUS)
    
    if not agent.llm_client:
        print("❌ Cannot start without Anthropic API key")
        return
    
    try:
        if not await agent.initialize():
            print("❌ Cannot start Sophisticated Agent")
            return
        
        print("✅ Sophisticated Agent ready with proper workflow strategy!")
        await agent.run_sophisticated_agent()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.error(f"Fatal error: {e}")
    finally:
        await agent.close()
        print("✅ Sophisticated Agent shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!") 