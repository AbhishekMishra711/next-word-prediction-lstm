from playwright.sync_api import sync_playwright
import time
import os

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1600, 'height': 900})
        page = context.new_page()
        
        print("Navigating to http://localhost:8501...")
        page.goto('http://localhost:8501', wait_until='networkidle')
        page.wait_for_timeout(4000)
        
        # 1. Capture Predictor Page (default index=1)
        print("Capturing Predictor Page...")
        # ensure prompt is filled and button or chart is visible
        page.wait_for_selector("input[type='text']")
        page.wait_for_timeout(2000)
        page.screenshot(path="screenshot_2_predictor.png", full_page=False)
        print("Saved screenshot_2_predictor.png")
        
        # 2. Navigate to Overview & Architecture
        print("Navigating to Overview & Architecture...")
        page.click("text=Overview & Architecture")
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot_1_overview.png", full_page=False)
        print("Saved screenshot_1_overview.png")
        
        # 3. Navigate to Model Evaluation
        print("Navigating to Model Evaluation...")
        page.click("text=Model Evaluation")
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot_3_evaluation.png", full_page=False)
        print("Saved screenshot_3_evaluation.png")
        
        # 4. Navigate back to Next Word Predictor with multi-word generation
        print("Navigating to Predictor for test case 2...")
        page.click("text=Next Word Predictor")
        page.wait_for_timeout(2000)
        # click on quick prompt button
        sample_btn = page.query_selector("button:has-text('natural language processing')")
        if sample_btn:
            sample_btn.click()
            page.wait_for_timeout(2500)
            page.screenshot(path="screenshot_4_nlp_prompt.png", full_page=False)
            print("Saved screenshot_4_nlp_prompt.png")
            
        browser.close()
        print("All screenshots successfully captured!")

if __name__ == '__main__':
    capture_screenshots()
