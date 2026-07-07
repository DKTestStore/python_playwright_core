from playwright.sync_api import sync_playwright
import logging
import os
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
import json


class RoleBasedLogger:
    """Role-Based Logger similar to Robot Framework"""
    
    def __init__(self, log_dir="./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"automation_{timestamp}.log"
        self.json_file = self.log_dir / f"automation_{timestamp}.json"
        
        # Initialize logger
        self.logger = logging.getLogger("PlaywrightAutomation")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        # Test execution tracking
        self.test_data = []
        self.current_test = None
        self.current_steps = []
    
    def start_test(self, test_name):
        """Start test execution logging"""
        self.current_test = {
            'name': test_name,
            'start_time': datetime.now().isoformat(),
            'status': 'RUNNING',
            'steps': [],
            'error': None
        }
        self.current_steps = []
        self.logger.info(f"{'='*70}")
        self.logger.info(f"TEST START: {test_name}")
        self.logger.info(f"{'='*70}")
    
    def end_test(self, status='PASS', error=None):
        """End test execution logging"""
        if self.current_test:
            self.current_test['end_time'] = datetime.now().isoformat()
            self.current_test['status'] = status
            self.current_test['error'] = error
            self.current_test['steps'] = self.current_steps
            
            duration = (datetime.fromisoformat(self.current_test['end_time']) - 
                       datetime.fromisoformat(self.current_test['start_time'])).total_seconds()
            
            status_icon = "PASS" if status == "PASS" else "FAIL"
            self.logger.info(f"[{status_icon}] TEST {status}: {self.current_test['name']} ({duration:.2f}s)")
            self.logger.info(f"{'='*70}\n")
            
            self.test_data.append(self.current_test)
            self.current_test = None
            self.current_steps = []
    
    def log_step(self, step_name, step_type='INFO'):
        """Log individual step"""
        step_info = {
            'name': step_name,
            'type': step_type,
            'timestamp': datetime.now().isoformat(),
            'status': 'EXECUTED'
        }
        
        prefix = ""
        if step_type == 'KEYWORD':
            prefix = "[KEYWORD] "
        elif step_type == 'VERIFICATION':
            prefix = "[VERIFY] "
        elif step_type == 'ACTION':
            prefix = "[ACTION] "
        elif step_type == 'INFO':
            prefix = "[INFO] "
        elif step_type == 'ERROR':
            prefix = "[ERROR] "
        
        self.logger.info(f"  {prefix}{step_name}")
        self.current_steps.append(step_info)
    
    def log_data(self, data_name, data_value):
        """Log data/variable"""
        self.logger.debug(f"  [DATA] {data_name} = {data_value}")
        if self.current_steps:
            self.current_steps[-1]['data'] = {data_name: str(data_value)}
    
    def log_error(self, error_message, error_type='ERROR'):
        """Log error"""
        self.logger.error(f"  [ERROR] {error_type}: {error_message}")
        if self.current_test:
            self.current_test['error'] = error_message
    
    def generate_html_report(self):
        """Generate HTML report with styling"""
        html_file = self.log_dir / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        total_tests = len(self.test_data)
        passed = sum(1 for t in self.test_data if t['status'] == 'PASS')
        failed = total_tests - passed
        success_rate = (passed/total_tests*100) if total_tests > 0 else 0
        
        # Calculate total duration
        total_duration = 0
        if self.test_data:
            for test in self.test_data:
                start = datetime.fromisoformat(test['start_time'])
                end = datetime.fromisoformat(test['end_time'])
                total_duration += (end - start).total_seconds()
        
        # Build test rows
        test_rows = ""
        for i, test in enumerate(self.test_data, 1):
            start = datetime.fromisoformat(test['start_time'])
            end = datetime.fromisoformat(test['end_time'])
            duration = (end - start).total_seconds()
            status_class = "pass" if test['status'] == 'PASS' else "fail"
            status_badge = f"<span class='badge {status_class}'>{test['status']}</span>"
            
            # Build steps details
            steps_html = ""
            for step in test['steps']:
                step_type = step['type']
                step_class = f"step-{step_type.lower()}"
                step_time = step['timestamp']
                step_data = step.get('data', {})
                
                data_html = ""
                for key, value in step_data.items():
                    data_html += f"<div class='step-data'><strong>{key}:</strong> {value}</div>"
                
                steps_html += f"""
                <div class='step {step_class}'>
                    <div class='step-header'>
                        <span class='step-type'>[{step['type']}]</span>
                        <span class='step-name'>{step['name']}</span>
                    </div>
                    {data_html}
                </div>
                """
            
            test_rows += f"""
            <tr class='{status_class}'>
                <td class='test-number'>{i}</td>
                <td class='test-name'>{test['name']}</td>
                <td class='test-status'>{status_badge}</td>
                <td class='test-duration'>{duration:.2f}s</td>
                <td class='test-actions'>
                    <button class='toggle-btn' onclick="toggleDetails('test-{i}')">Details</button>
                </td>
            </tr>
            <tr id='test-{i}' class='details-row' style='display:none;'>
                <td colspan='5'>
                    <div class='test-details'>
                        <h4>Test: {test['name']}</h4>
                        <div class='steps-container'>
                            {steps_html}
                        </div>
                    </div>
                </td>
            </tr>
            """
        
        # HTML Template
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Playwright Automation Test Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        .summary-card h3 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .summary-card.passed .number {{
            color: #28a745;
        }}
        
        .summary-card.failed .number {{
            color: #dc3545;
        }}
        
        .summary-card.duration .number {{
            color: #fd7e14;
        }}
        
        .summary-card.rate .number {{
            color: #17a2b8;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .content h2 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        
        table thead {{
            background: #667eea;
            color: white;
        }}
        
        table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        table tr:hover {{
            background: #f5f5f5;
        }}
        
        table tr.pass {{
            background-color: #f0f9ff;
        }}
        
        table tr.fail {{
            background-color: #fff5f5;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .badge.pass {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .badge.fail {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .toggle-btn {{
            background-color: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .toggle-btn:hover {{
            background-color: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        .details-row {{
            background: #f8f9fa;
        }}
        
        .test-details {{
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .test-details h4 {{
            margin-bottom: 15px;
            color: #333;
            font-size: 16px;
        }}
        
        .steps-container {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .step {{
            padding: 12px;
            border-left: 3px solid #ddd;
            background: #fafafa;
            border-radius: 4px;
            transition: all 0.3s ease;
        }}
        
        .step:hover {{
            background: #f0f0f0;
            border-left-color: #667eea;
        }}
        
        .step-header {{
            display: flex;
            gap: 10px;
            margin-bottom: 5px;
        }}
        
        .step-type {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .step-action .step-type {{
            background: #ff9800;
        }}
        
        .step-keyword .step-type {{
            background: #2196f3;
        }}
        
        .step-verify .step-type {{
            background: #4caf50;
        }}
        
        .step-info .step-type {{
            background: #9c27b0;
        }}
        
        .step-error .step-type {{
            background: #f44336;
        }}
        
        .step-name {{
            flex: 1;
            font-weight: 500;
            color: #333;
        }}
        
        .step-data {{
            margin-top: 8px;
            padding: 8px;
            background: white;
            border-radius: 3px;
            font-size: 12px;
            color: #555;
            border-left: 2px solid #667eea;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #dee2e6;
        }}
        
        .footer strong {{
            color: #333;
        }}
        
        .test-number {{
            text-align: center;
            font-weight: 600;
        }}
        
        .test-duration {{
            text-align: center;
            font-weight: 500;
        }}
        
        .test-actions {{
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            table {{
                font-size: 12px;
            }}
            
            .toggle-btn {{
                padding: 4px 8px;
                font-size: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Playwright Automation Test Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>Total Tests</h3>
                <div class="number">{total_tests}</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="number">{passed}</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="number">{failed}</div>
            </div>
            <div class="summary-card duration">
                <h3>Total Duration</h3>
                <div class="number">{total_duration:.2f}s</div>
            </div>
            <div class="summary-card rate">
                <h3>Success Rate</h3>
                <div class="number">{success_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="content">
            <h2>Test Execution Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {test_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p><strong>Report Location:</strong> {html_file}</p>
            <p>Automation Framework: Playwright | Python</p>
        </div>
    </div>
    
    <script>
        function toggleDetails(id) {{
            const element = document.getElementById(id);
            if (element.style.display === 'none') {{
                element.style.display = 'table-row';
            }} else {{
                element.style.display = 'none';
            }}
        }}
    </script>
</body>
</html>
        """
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML Report: {html_file}")
        return str(html_file)
    
    def generate_report(self):
        """Generate JSON report"""
        with open(self.json_file, 'w') as f:
            json.dump(self.test_data, f, indent=2)
        
        # Generate summary
        total_tests = len(self.test_data)
        passed = sum(1 for t in self.test_data if t['status'] == 'PASS')
        failed = total_tests - passed
        
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"EXECUTION SUMMARY")
        self.logger.info(f"{'='*70}")
        self.logger.info(f"Total Tests: {total_tests}")
        self.logger.info(f"Passed: {passed}")
        self.logger.info(f"Failed: {failed}")
        self.logger.info(f"Success Rate: {(passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        self.logger.info(f"Log File: {self.log_file}")
        self.logger.info(f"JSON Report: {self.json_file}")
        
        # Generate HTML report
        html_file = self.generate_html_report()
        self.logger.info(f"{'='*70}\n")
        
        return {
            'total': total_tests,
            'passed': passed,
            'failed': failed,
            'log_file': str(self.log_file),
            'json_file': str(self.json_file),
            'html_file': html_file
        }


# Global logger instance
logger = RoleBasedLogger()


def test_case(func):
    """Decorator to track test execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.start_test(func.__name__)
        try:
            result = func(*args, **kwargs)
            logger.end_test(status='PASS')
            return result
        except Exception as e:
            logger.end_test(status='FAIL', error=str(e))
            raise
    return wrapper


@test_case
def test_native_options():
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Initial Navigation
        logger.log_step("Navigate to Playwright website", "KEYWORD")
        page.goto("https://playwright.dev/")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(5000)

        # 2. Second Navigation
        logger.log_step("Navigate to GitHub", "KEYWORD")
        page.goto("https://github.com/")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(5000)

        # 3. NAVIGATE BACK (Mimics the 'Back' arrow)
        logger.log_step("Navigate back in history", "ACTION")
        page.go_back()
        logger.log_data("Current URL after go_back", page.url)
        logger.log_step(f"Verify back navigation worked - URL is {page.url}", "VERIFICATION")
        page.wait_for_timeout(5000)

        # 4. NAVIGATE FORWARD (Mimics the 'Forward' arrow)
        logger.log_step("Navigate forward in history", "ACTION")
        page.go_forward()
        logger.log_data("Current URL after go_forward", page.url)
        logger.log_step(f"Verify forward navigation worked - URL is {page.url}", "VERIFICATION")
        page.wait_for_timeout(5000)

        # 5. REFRESH (Mimics 'F5' or the Reload button)
        logger.log_step("Refresh page using page.reload()", "ACTION")
        page.reload()
        logger.log_data("URL after reload", page.url)

        # Alternative JavaScript using browser history
        logger.log_step("Refresh page using JavaScript (history.go(0))", "KEYWORD")
        page.evaluate("history.go(0)")
        page.wait_for_timeout(5000)

        logger.log_step("Close browser", "ACTION")
        browser.close()

@test_case
def test_renavigate_to_current_url():
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        logger.log_step("Navigate to Google", "KEYWORD")
        page.goto("https://www.google.com")
        logger.log_data("Initial URL", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Get current URL", "INFO")
        current_url = page.url
        logger.log_data("Current URL saved", current_url)
        
        logger.log_step("Re-navigate to current URL", "KEYWORD")
        page.goto(current_url)
        logger.log_data("URL after re-navigation", page.url)
        logger.log_step(f"Verify URL remains the same: {page.url}", "VERIFICATION")
        page.wait_for_timeout(5000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()

@test_case
def test_refresh_page_using_function_key():
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        logger.log_step("Navigate to Google", "KEYWORD")
        page.goto("https://www.google.com")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Refresh page using F5 key", "ACTION")
        page.keyboard.press("F5")
        logger.log_step("Wait for page to load", "KEYWORD")
        page.wait_for_load_state()
        logger.log_data("URL after refresh", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()

@test_case
def test_refresh_page_keyboard_commands():
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        logger.log_step("Navigate to Google", "KEYWORD")
        page.goto("https://www.google.com")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Refresh page using Ctrl+R", "ACTION")
        page.keyboard.press("Control+R")  # For Windows/Linux
        logger.log_step("Wait for page to load", "KEYWORD")
        page.wait_for_load_state()
        logger.log_data("URL after refresh", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()


@test_case
def test_refresh():
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        logger.log_step("Navigate to Google", "KEYWORD")
        page.goto("https://www.google.com")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Refresh page using location.reload() JavaScript", "ACTION")
        page.evaluate("location.reload()")
        logger.log_step("Wait for load state", "KEYWORD")
        page.wait_for_load_state()
        logger.log_data("URL after refresh", page.url)
        page.wait_for_timeout(5000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()


@test_case
def test_refresh_with_hard_reload():
    """Test page refresh with hard reload to bypass cache"""
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        logger.log_step("Navigate to Google", "KEYWORD")
        page.goto("https://www.google.com")
        logger.log_data("URL", page.url)
        page.wait_for_timeout(3000)
        
        # Hard refresh bypassing cache
        logger.log_step("Perform hard refresh using Ctrl+Shift+R", "ACTION")
        page.keyboard.press("Control+Shift+R")
        logger.log_step("Wait for page load state", "KEYWORD")
        page.wait_for_load_state()
        logger.log_data("URL after hard refresh", page.url)
        logger.log_step(f"Page refreshed with hard reload: {page.url}", "VERIFICATION")
        page.wait_for_timeout(5000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()


@test_case
def test_multiple_navigations_with_history():
    """Test multiple page navigations and using browser history"""
    with sync_playwright() as p:
        logger.log_step("Launching Chromium browser", "ACTION")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to multiple sites
        urls = [
            "https://www.google.com",
            "https://www.wikipedia.org",
            "https://www.stackoverflow.com"
        ]
        
        logger.log_step(f"Navigate to {len(urls)} websites", "KEYWORD")
        for url in urls:
            logger.log_step(f"Goto: {url}", "ACTION")
            page.goto(url)
            logger.log_data("Current URL", page.url)
            page.wait_for_timeout(2000)
        
        # Go back through history
        logger.log_step("Navigate back through browser history", "KEYWORD")
        logger.log_step("First go_back()", "ACTION")
        page.go_back()
        logger.log_data("URL after first go_back", page.url)
        logger.log_step(f"Verify navigation - URL is now: {page.url}", "VERIFICATION")
        page.wait_for_timeout(2000)
        
        logger.log_step("Second go_back()", "ACTION")
        page.go_back()
        logger.log_data("URL after second go_back", page.url)
        logger.log_step(f"Verify navigation - URL is now: {page.url}", "VERIFICATION")
        page.wait_for_timeout(2000)
        
        logger.log_step("Close browser", "ACTION")
        browser.close()


if __name__ == "__main__":
    logger.logger.info("\n" + "="*70)
    logger.logger.info("PLAYWRIGHT AUTOMATION TEST SUITE STARTED")
    logger.logger.info("="*70 + "\n")
    
    try:
        test_native_options()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_renavigate_to_current_url()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_refresh_page_using_function_key()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_refresh_page_keyboard_commands()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_refresh()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_refresh_with_hard_reload()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    try:
        test_multiple_navigations_with_history()
    except Exception as e:
        logger.log_error(f"Test failed: {str(e)}")
    
    # Generate final report
    report = logger.generate_report()
    logger.logger.info(f"\nReport Summary:")
    logger.logger.info(f"  Total Tests: {report['total']}")
    logger.logger.info(f"  Passed: {report['passed']}")
    logger.logger.info(f"  Failed: {report['failed']}")
    logger.logger.info(f"  Log File: {report['log_file']}")
    logger.logger.info(f"  JSON Report: {report['json_file']}")
    logger.logger.info(f"  HTML Report: {report['html_file']}")
