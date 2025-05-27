#!/usr/bin/env python3
"""
DOMAnalyzer - Comprehensive DOM and Form Analysis Tool

This class provides advanced DOM analysis capabilities for production-ready
browser automation, including form structure analysis, element detection,
and iframe handling.
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class DOMAnalyzer:
    """
    Advanced DOM analysis tool for browser automation.
    
    Provides comprehensive form analysis, element detection, and
    iframe context management for production automation scenarios.
    """
    
    def __init__(self, tools):
        """Initialize DOM analyzer with Playwright tools."""
        self.tools = tools
    
    async def analyze_form(self, page_index: int = 0) -> Dict[str, Any]:
        """
        Analyzes complete form structure and returns all possible selectors.
        
        Returns:
            dict: Comprehensive form analysis including:
                - input_fields: All input field selectors and metadata
                - form_structure: Form hierarchy and relationships
                - iframe_context: Iframe detection and context
                - interactive_elements: All clickable elements
                - validation_info: Form validation attributes
        """
        logger.info(f"Starting comprehensive form analysis for page {page_index}")
        
        try:
            # Run all analysis methods
            input_fields = await self.get_all_input_selectors(page_index)
            form_structure = await self.get_form_hierarchy(page_index)
            iframe_context = await self.detect_iframes(page_index)
            interactive_elements = await self.get_interactive_elements(page_index)
            validation_info = await self.get_validation_attributes(page_index)
            
            analysis_result = {
                "input_fields": input_fields,
                "form_structure": form_structure,
                "iframe_context": iframe_context,
                "interactive_elements": interactive_elements,
                "validation_info": validation_info,
                "analysis_timestamp": await self.tools.playwright_evaluate(
                    script="new Date().toISOString()",
                    page_index=page_index
                )
            }
            
            logger.info(f"Form analysis complete: {len(input_fields)} inputs, {len(interactive_elements)} interactive elements")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error during form analysis: {e}")
            return {
                "error": str(e),
                "input_fields": [],
                "form_structure": {},
                "iframe_context": [],
                "interactive_elements": [],
                "validation_info": {}
            }
    
    async def get_all_input_selectors(self, page_index: int = 0) -> List[Dict[str, Any]]:
        """
        Gets all possible selectors for input fields with comprehensive metadata.
        
        Returns:
            list: Each input with multiple selector strategies and metadata
        """
        input_analysis_script = """
        () => {
            function getXPath(element) {
                if (element.id !== '') {
                    return `//[@id="${element.id}"]`;
                }
                if (element === document.body) {
                    return '/html/body';
                }
                
                let ix = 0;
                const siblings = element.parentNode?.childNodes || [];
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (sibling === element) {
                        return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                    }
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
                return '';
            }
            
            function getAttributes(element) {
                const attrs = {};
                for (let attr of element.attributes) {
                    attrs[attr.name] = attr.value;
                }
                return attrs;
            }
            
            function getCSSPath(element) {
                if (element.id) return `#${element.id}`;
                
                let path = [];
                while (element && element.nodeType === 1) {
                    let selector = element.tagName.toLowerCase();
                    
                    if (element.className) {
                        selector += '.' + element.className.trim().split(/\\s+/).join('.');
                    }
                    
                    // Add position if there are siblings
                    const siblings = element.parentNode?.children || [];
                    const sameTagSiblings = Array.from(siblings).filter(s => s.tagName === element.tagName);
                    if (sameTagSiblings.length > 1) {
                        const index = Array.from(sameTagSiblings).indexOf(element) + 1;
                        selector += `:nth-of-type(${index})`;
                    }
                    
                    path.unshift(selector);
                    element = element.parentNode;
                    
                    // Stop at body or if we have an ID
                    if (!element || element.tagName === 'BODY' || element.id) break;
                }
                
                return path.join(' > ');
            }
            
            function getLabels(element) {
                const labels = [];
                
                // Direct label association
                if (element.id) {
                    const directLabels = document.querySelectorAll(`label[for="${element.id}"]`);
                    labels.push(...Array.from(directLabels).map(l => l.textContent?.trim() || ''));
                }
                
                // Parent label
                let parent = element.parentNode;
                while (parent && parent.tagName !== 'BODY') {
                    if (parent.tagName === 'LABEL') {
                        labels.push(parent.textContent?.trim() || '');
                        break;
                    }
                    parent = parent.parentNode;
                }
                
                return labels.filter(l => l.length > 0);
            }
            
            const inputs = document.querySelectorAll('input, textarea, select');
            return Array.from(inputs).map((el, index) => {
                const rect = el.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0 && 
                                 window.getComputedStyle(el).visibility !== 'hidden' &&
                                 window.getComputedStyle(el).display !== 'none';
                
                return {
                    index: index,
                    tagName: el.tagName.toLowerCase(),
                    type: el.type || '',
                    id: el.id || '',
                    name: el.name || '',
                    className: el.className || '',
                    placeholder: el.placeholder || '',
                    value: el.value || '',
                    required: el.required || false,
                    disabled: el.disabled || false,
                    readonly: el.readOnly || false,
                    visible: isVisible,
                    labels: getLabels(el),
                    position: {
                        x: Math.round(rect.left),
                        y: Math.round(rect.top),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    },
                    selectors: {
                        id: el.id ? `#${el.id}` : '',
                        name: el.name ? `[name="${el.name}"]` : '',
                        xpath: getXPath(el),
                        cssPath: getCSSPath(el),
                        placeholder: el.placeholder ? `[placeholder="${el.placeholder}"]` : '',
                        type: el.type ? `${el.tagName.toLowerCase()}[type="${el.type}"]` : el.tagName.toLowerCase()
                    },
                    attributes: getAttributes(el),
                    formContext: {
                        formId: el.form?.id || '',
                        formName: el.form?.name || '',
                        formAction: el.form?.action || '',
                        formMethod: el.form?.method || ''
                    }
                };
            });
        }
        """
        
        try:
            result = await self.tools.playwright_evaluate(
                script=input_analysis_script,
                page_index=page_index
            )
            
            input_fields = result.get("data", [])
            logger.info(f"Found {len(input_fields)} input fields")
            return input_fields
            
        except Exception as e:
            logger.error(f"Error getting input selectors: {e}")
            return []
    
    async def get_form_hierarchy(self, page_index: int = 0) -> Dict[str, Any]:
        """
        Analyzes form structure and hierarchy relationships.
        
        Returns:
            dict: Form hierarchy including parent-child relationships
        """
        form_hierarchy_script = """
        () => {
            const forms = document.querySelectorAll('form');
            const hierarchy = {
                forms: [],
                fieldsets: [],
                totalFields: 0
            };
            
            forms.forEach((form, formIndex) => {
                const formData = {
                    index: formIndex,
                    id: form.id || '',
                    name: form.name || '',
                    action: form.action || '',
                    method: form.method || 'get',
                    enctype: form.enctype || '',
                    fields: [],
                    fieldsets: []
                };
                
                // Find all fields in this form
                const fields = form.querySelectorAll('input, textarea, select');
                formData.fields = Array.from(fields).map((field, fieldIndex) => ({
                    index: fieldIndex,
                    tagName: field.tagName.toLowerCase(),
                    type: field.type || '',
                    id: field.id || '',
                    name: field.name || '',
                    required: field.required || false
                }));
                
                // Find fieldsets
                const fieldsets = form.querySelectorAll('fieldset');
                formData.fieldsets = Array.from(fieldsets).map((fieldset, fsIndex) => ({
                    index: fsIndex,
                    id: fieldset.id || '',
                    legend: fieldset.querySelector('legend')?.textContent?.trim() || '',
                    fields: Array.from(fieldset.querySelectorAll('input, textarea, select')).length
                }));
                
                hierarchy.forms.push(formData);
                hierarchy.totalFields += formData.fields.length;
            });
            
            return hierarchy;
        }
        """
        
        try:
            result = await self.tools.playwright_evaluate(
                script=form_hierarchy_script,
                page_index=page_index
            )
            
            return result.get("data", {})
            
        except Exception as e:
            logger.error(f"Error getting form hierarchy: {e}")
            return {}
    
    async def detect_iframes(self, page_index: int = 0) -> List[Dict[str, Any]]:
        """
        Detects iframes and their contexts for cross-frame automation.
        
        Returns:
            list: Iframe information and accessibility
        """
        iframe_detection_script = """
        () => {
            const iframes = document.querySelectorAll('iframe, frame');
            return Array.from(iframes).map((iframe, index) => {
                const rect = iframe.getBoundingClientRect();
                return {
                    index: index,
                    id: iframe.id || '',
                    name: iframe.name || '',
                    src: iframe.src || '',
                    title: iframe.title || '',
                    visible: rect.width > 0 && rect.height > 0,
                    position: {
                        x: Math.round(rect.left),
                        y: Math.round(rect.top),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    },
                    sandbox: iframe.sandbox?.toString() || '',
                    seamless: iframe.seamless || false,
                    accessibleContent: true // Will need special handling for cross-origin
                };
            });
        }
        """
        
        try:
            result = await self.tools.playwright_evaluate(
                script=iframe_detection_script,
                page_index=page_index
            )
            
            return result.get("data", [])
            
        except Exception as e:
            logger.error(f"Error detecting iframes: {e}")
            return []
    
    async def get_interactive_elements(self, page_index: int = 0) -> List[Dict[str, Any]]:
        """
        Gets all interactive elements (buttons, links, clickable elements).
        
        Returns:
            list: All clickable elements with selectors
        """
        interactive_script = """
        () => {
            function getXPath(element) {
                if (element.id !== '') return `//[@id="${element.id}"]`;
                if (element === document.body) return '/html/body';
                
                let ix = 0;
                const siblings = element.parentNode?.childNodes || [];
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (sibling === element) {
                        return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                    }
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
                return '';
            }
            
            const selectors = [
                'button',
                'input[type="button"]',
                'input[type="submit"]',
                'input[type="reset"]',
                'a[href]',
                '[onclick]',
                '[role="button"]',
                '.btn, .button',
                '[data-action]'
            ];
            
            const elements = [];
            selectors.forEach(selector => {
                try {
                    const found = document.querySelectorAll(selector);
                    elements.push(...Array.from(found));
                } catch (e) {
                    // Skip invalid selectors
                }
            });
            
            // Remove duplicates
            const uniqueElements = [...new Set(elements)];
            
            return uniqueElements.map((el, index) => {
                const rect = el.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0 && 
                                 window.getComputedStyle(el).visibility !== 'hidden' &&
                                 window.getComputedStyle(el).display !== 'none';
                
                return {
                    index: index,
                    tagName: el.tagName.toLowerCase(),
                    type: el.type || '',
                    id: el.id || '',
                    className: el.className || '',
                    textContent: el.textContent?.trim() || '',
                    href: el.href || '',
                    disabled: el.disabled || false,
                    visible: isVisible,
                    position: {
                        x: Math.round(rect.left),
                        y: Math.round(rect.top),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    },
                    selectors: {
                        id: el.id ? `#${el.id}` : '',
                        xpath: getXPath(el),
                        text: el.textContent?.trim() ? `text="${el.textContent.trim()}"` : '',
                        tag: el.tagName.toLowerCase()
                    },
                    actions: {
                        onclick: !!el.onclick,
                        hasEventListeners: !!el._eventListeners || false,
                        role: el.getAttribute('role') || '',
                        dataAction: el.getAttribute('data-action') || ''
                    }
                };
            });
        }
        """
        
        try:
            result = await self.tools.playwright_evaluate(
                script=interactive_script,
                page_index=page_index
            )
            
            return result.get("data", [])
            
        except Exception as e:
            logger.error(f"Error getting interactive elements: {e}")
            return []
    
    async def get_validation_attributes(self, page_index: int = 0) -> Dict[str, Any]:
        """
        Extracts form validation information for better automation.
        
        Returns:
            dict: Validation rules and constraints
        """
        validation_script = """
        () => {
            const inputs = document.querySelectorAll('input, textarea, select');
            const validation = {
                required_fields: [],
                patterns: [],
                min_max_constraints: [],
                custom_validation: []
            };
            
            inputs.forEach((input, index) => {
                const inputData = {
                    index: index,
                    id: input.id || '',
                    name: input.name || '',
                    type: input.type || ''
                };
                
                if (input.required) {
                    validation.required_fields.push(inputData);
                }
                
                if (input.pattern) {
                    validation.patterns.push({
                        ...inputData,
                        pattern: input.pattern,
                        title: input.title || ''
                    });
                }
                
                if (input.min || input.max || input.minLength || input.maxLength) {
                    validation.min_max_constraints.push({
                        ...inputData,
                        min: input.min || '',
                        max: input.max || '',
                        minLength: input.minLength || '',
                        maxLength: input.maxLength || ''
                    });
                }
                
                // Check for custom validation attributes
                const customAttrs = ['data-validate', 'data-validation', 'data-rule'];
                customAttrs.forEach(attr => {
                    if (input.hasAttribute(attr)) {
                        validation.custom_validation.push({
                            ...inputData,
                            attribute: attr,
                            value: input.getAttribute(attr)
                        });
                    }
                });
            });
            
            return validation;
        }
        """
        
        try:
            result = await self.tools.playwright_evaluate(
                script=validation_script,
                page_index=page_index
            )
            
            return result.get("data", {})
            
        except Exception as e:
            logger.error(f"Error getting validation attributes: {e}")
            return {}
    
    async def find_element_by_description(self, description: str, page_index: int = 0) -> Optional[Dict[str, Any]]:
        """
        Intelligently finds an element based on natural language description.
        
        Args:
            description: Natural language description (e.g., "name field", "submit button")
            page_index: Page index to search
            
        Returns:
            dict: Best matching element with selectors, or None if not found
        """
        logger.info(f"Finding element by description: '{description}'")
        
        # Get all elements first
        analysis = await self.analyze_form(page_index)
        all_inputs = analysis.get("input_fields", [])
        all_interactive = analysis.get("interactive_elements", [])
        
        description_lower = description.lower()
        candidates = []
        
        # Score input fields
        for input_field in all_inputs:
            score = 0
            reasons = []
            
            # Check various attributes
            if input_field.get('id') and description_lower in input_field['id'].lower():
                score += 10
                reasons.append(f"ID matches '{description_lower}'")
            
            if input_field.get('name') and description_lower in input_field['name'].lower():
                score += 8
                reasons.append(f"Name matches '{description_lower}'")
            
            if input_field.get('placeholder') and description_lower in input_field['placeholder'].lower():
                score += 9
                reasons.append(f"Placeholder matches '{description_lower}'")
            
            # Check labels
            for label in input_field.get('labels', []):
                if description_lower in label.lower():
                    score += 10
                    reasons.append(f"Label matches '{description_lower}'")
            
            # Type-based matching
            type_mappings = {
                'name': ['text'], 'email': ['email'], 'password': ['password'],
                'phone': ['tel'], 'number': ['number'], 'date': ['date']
            }
            
            for desc_key, types in type_mappings.items():
                if desc_key in description_lower and input_field.get('type') in types:
                    score += 7
                    reasons.append(f"Type '{input_field.get('type')}' matches '{desc_key}'")
            
            if score > 0:
                candidates.append({
                    'element': input_field,
                    'score': score,
                    'reasons': reasons,
                    'type': 'input'
                })
        
        # Score interactive elements (buttons, links)
        for interactive in all_interactive:
            score = 0
            reasons = []
            
            text_content = interactive.get('textContent', '').lower()
            if description_lower in text_content:
                score += 8
                reasons.append(f"Text content matches '{description_lower}'")
            
            # Button-specific matching
            if 'button' in description_lower or 'submit' in description_lower or 'click' in description_lower:
                if interactive.get('tagName') in ['button', 'input'] or interactive.get('type') in ['submit', 'button']:
                    score += 6
                    reasons.append("Element is a button")
            
            if score > 0:
                candidates.append({
                    'element': interactive,
                    'score': score,
                    'reasons': reasons,
                    'type': 'interactive'
                })
        
        # Sort by score and return best match
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        if candidates:
            best = candidates[0]
            logger.info(f"Found element: {best['reasons']} (Score: {best['score']})")
            return best
        else:
            logger.warning(f"No element found matching '{description}'")
            return None
    
    def print_analysis_summary(self, analysis: Dict[str, Any]) -> None:
        """Print a human-readable summary of the DOM analysis."""
        print("\n" + "="*60)
        print("🔍 DOM ANALYSIS SUMMARY")
        print("="*60)
        
        # Input fields summary
        input_fields = analysis.get("input_fields", [])
        visible_inputs = [f for f in input_fields if f.get("visible", False)]
        print(f"📝 Input Fields: {len(visible_inputs)}/{len(input_fields)} visible")
        
        for i, field in enumerate(visible_inputs[:5]):  # Show first 5
            field_type = field.get('type', 'unknown')
            field_id = field.get('id', 'no-id')
            field_labels = ', '.join(field.get('labels', ['no-label']))
            print(f"   {i+1}. {field_type} field - ID: '{field_id}' - Labels: [{field_labels}]")
        
        if len(visible_inputs) > 5:
            print(f"   ... and {len(visible_inputs) - 5} more")
        
        # Interactive elements summary
        interactive = analysis.get("interactive_elements", [])
        visible_interactive = [e for e in interactive if e.get("visible", False)]
        print(f"🖱️  Interactive Elements: {len(visible_interactive)}/{len(interactive)} visible")
        
        for i, elem in enumerate(visible_interactive[:3]):  # Show first 3
            elem_text = elem.get('textContent', 'no-text')[:30]
            elem_tag = elem.get('tagName', 'unknown')
            print(f"   {i+1}. {elem_tag} - Text: '{elem_text}'")
        
        # Forms summary
        form_structure = analysis.get("form_structure", {})
        forms = form_structure.get("forms", [])
        print(f"📋 Forms: {len(forms)} found")
        
        for i, form in enumerate(forms):
            form_id = form.get('id', 'no-id')
            form_fields = len(form.get('fields', []))
            print(f"   {i+1}. Form ID: '{form_id}' - {form_fields} fields")
        
        # Iframes summary
        iframes = analysis.get("iframe_context", [])
        print(f"🖼️  Iframes: {len(iframes)} detected")
        
        print("="*60) 