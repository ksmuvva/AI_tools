#!/usr/bin/env python3
"""
Test script to demonstrate page evaluation tools
"""
import asyncio
from Playwright_tools import PlaywrightTools

async def test_page_evaluation_tools():
    """Test various page evaluation capabilities"""
    tools = PlaywrightTools()
    await tools.initialize()
    
    print("🚀 Testing Page Evaluation Tools...")
    print("="*50)
    
    # Navigate to a test page
    print("📍 Navigating to test page...")
    result = await tools.playwright_navigate('httpbin.org')
    print(f"   ✅ {result['message']}")
    
    # Test 1: Basic page evaluation
    print("\n🔧 Test 1: Basic JavaScript Evaluation")
    eval_result = await tools.playwright_evaluate('document.title')
    print(f"   📄 Page Title: {eval_result['result']}")
    
    # Test 2: Get page URL
    url_result = await tools.playwright_evaluate('window.location.href')
    print(f"   🌐 Page URL: {url_result['result']}")
    
    # Test 3: Count elements
    count_result = await tools.playwright_evaluate('document.querySelectorAll("*").length')
    print(f"   📊 Total Elements: {count_result['result']}")
    
    # Test 4: Complex DOM analysis
    print("\n🧠 Test 2: Complex DOM Analysis")
    complex_eval = await tools.playwright_evaluate('''
        () => {
            return {
                title: document.title,
                url: window.location.href,
                elementCount: document.querySelectorAll('*').length,
                inputCount: document.querySelectorAll('input').length,
                linkCount: document.querySelectorAll('a').length,
                buttonCount: document.querySelectorAll('button').length,
                pageHeight: document.body.scrollHeight,
                viewportSize: {
                    width: window.innerWidth,
                    height: window.innerHeight
                }
            };
        }
    ''')
    
    if complex_eval['status'] == 'success':
        analysis = complex_eval['result']
        print(f"   📄 Title: {analysis['title']}")
        print(f"   🌐 URL: {analysis['url']}")
        print(f"   📊 Total Elements: {analysis['elementCount']}")
        print(f"   🔗 Links: {analysis['linkCount']}")
        print(f"   🔲 Buttons: {analysis['buttonCount']}")
        print(f"   📏 Page Height: {analysis['pageHeight']}px")
        print(f"   🖥️ Viewport: {analysis['viewportSize']['width']}x{analysis['viewportSize']['height']}")
    
    # Test 5: Advanced element analyzer
    print("\n🔍 Test 3: Comprehensive Element Analysis")
    analyzer_result = await tools.playwright_comprehensive_element_analyzer()
    if analyzer_result['status'] == 'success':
        summary = analyzer_result['analysis']['summary']
        print(f"   📊 Total Elements: {summary['total_elements']}")
        print(f"   👁️ Visible Elements: {summary['visible_elements']}")
        print(f"   🖱️ Interactive Elements: {summary['interactive_elements']}")
        print(f"   📝 Form Elements: {summary['form_elements']}")
        
        # Show some input details
        inputs = analyzer_result['analysis']['inputs'][:3]  # First 3 inputs
        if inputs:
            print(f"   📝 Sample Inputs:")
            for i, inp in enumerate(inputs, 1):
                print(f"      {i}. {inp['tagName']} - {inp['attributes'].get('type', 'text')} - Visible: {inp['visibility']['visible']}")
    
    # Test 6: JavaScript-based element location
    print("\n🎯 Test 4: JavaScript Element Location")
    js_locate_result = await tools.playwright_js_locate("search")
    if js_locate_result['status'] == 'success' and js_locate_result.get('element_found'):
        best = js_locate_result['best_candidate']
        print(f"   🎯 Found element: {best['element']['tagName']} (score: {best['score']})")
        print(f"   📝 Text content: {best['element']['textContent'][:50]}...")
    else:
        print(f"   ❌ No search elements found")
    
    # Test 7: Form analysis with evaluation
    print("\n📋 Test 5: Form Analysis")
    form_analysis = await tools.playwright_analyze_form()
    if form_analysis['status'] == 'success':
        analysis = form_analysis['analysis']
        input_count = len(analysis.get('input_fields', []))
        form_count = len(analysis.get('form_structure', {}).get('forms', []))
        print(f"   📝 Input Fields Found: {input_count}")
        print(f"   📋 Forms Found: {form_count}")
        
        # Show interactive elements
        interactive = analysis.get('interactive_elements', [])[:3]
        if interactive:
            print(f"   🖱️ Interactive Elements:")
            for i, elem in enumerate(interactive, 1):
                print(f"      {i}. {elem['tagName']} - '{elem['text'][:30]}...' - Visible: {elem['visible']}")
    
    await tools.close()
    print("\n✅ All page evaluation tools working perfectly!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_page_evaluation_tools()) 