import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://humanbenchmark.com/tests/"

class HumanBenchmarkBot:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
    
    def navigate_to_test(self, test_name):
        self.driver.get(f"{BASE_URL}{test_name}")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return True
    
    def reaction_time(self, lvls=5):
        self.navigate_to_test("reactiontime")
        self.driver.find_element(By.CLASS_NAME, 'view-splash').click()

        for num in range(lvls):
            WebDriverWait(self.driver, 10, poll_frequency=0.001).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'view-go'))
            ).click()
            if num != lvls - 1:
                self.driver.find_element(By.CLASS_NAME, 'view-result').click()
    
    def sequence_memory(self, lvls):
        self.navigate_to_test("sequence")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]").click()

        for num_squares in range(1, lvls + 1):
            sequence, last_active = [], None
            while len(sequence) < num_squares:
                active = self.driver.find_elements(By.CSS_SELECTOR, "div.square.active")
                if active:
                    square = active[0]
                    if last_active is None or square != last_active:
                        sequence.append(square)
                    last_active = square
            time.sleep(1)
            for el in sequence:
                el.click()
    
    def aim_trainer(self):
        self.navigate_to_test("aim")

        for _ in range(31):
            target = self.driver.find_element(By.CSS_SELECTOR, '[data-aim-target="true"]')
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
            self.driver.execute_script(
                """
                var elem = arguments[0];
                ['mousedown', 'mouseup', 'click'].forEach(function(evtType) {
                    var event = new MouseEvent(evtType, {view: window, bubbles: true, cancelable: true});
                    elem.dispatchEvent(event);
                });
                """, target)
    
    def number_memory(self, lvls):
        self.navigate_to_test("number-memory")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]").click()

        for num in range(lvls):
            number = self.driver.find_element(By.CLASS_NAME, 'big-number').text
            input_field = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
            )
            input_field.send_keys(number)
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
            if num != lvls - 1:
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'NEXT')]").click()
    
    def verbal_memory(self, lvls):
        self.navigate_to_test("verbal-memory")
        seen = set()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Start')]").click()

        for _ in range(lvls):
            word = self.driver.find_element(By.CLASS_NAME, 'word').text
            if word in seen:
                self.driver.find_element(By.XPATH, "//button[contains(text(),'SEEN')]").click()
            else:
                seen.add(word)
                self.driver.find_element(By.XPATH, "//button[contains(text(),'NEW')]").click()
    
    def chimp_test(self, lvls):
        self.navigate_to_test("chimp")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start Test')]").click()

        for num in range(lvls):
            for i in range(1, 5 + num):
                self.driver.find_element(By.XPATH, f'//div[@data-cellnumber="{i}"]').click()
            if num != lvls - 1:
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
    
    def visual_memory(self, lvls):
        self.navigate_to_test("memory")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]").click()
        count = 3

        for _ in range(lvls):
            active = []
            while len(active) != count:
                active = self.driver.find_elements(By.CSS_SELECTOR, 'div.active')
            time.sleep(1.25)
            for el in active:
                el.click()
            count += 1
    
    def typing(self):
        self.navigate_to_test("typing")
        raw = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div/span')
        text = ''.join([c.text or ' ' for c in raw])
        self.driver.find_element(By.CSS_SELECTOR, ".letters.notranslate").send_keys(text)

#Browser factories
browsers = {
    'firefox': lambda: webdriver.Firefox(),
    'chrome':  lambda: webdriver.Chrome(),
    'edge':    lambda: webdriver.Edge()
}

#Display name mappings
tests = {
    'reaction time':   'reactiontime',
    'sequence memory': 'sequence',
    'aim trainer':     'aim', 
    'number memory':   'number-memory',
    'verbal memory':   'verbal-memory',
    'chimp test':      'chimp',
    'visual memory':   'memory',
    'typing':          'typing'
}

#Tests that require level input
level_based_tests = {'sequence', 'number-memory', 'verbal-memory', 'chimp', 'memory'}

def get_test_method(bot, endpoint):
    """Get the bot method for a given test endpoint"""
    methods = {
        'reactiontime':   bot.reaction_time,
        'sequence':       bot.sequence_memory,
        'aim':            bot.aim_trainer,
        'number-memory':  bot.number_memory,
        'verbal-memory':  bot.verbal_memory,
        'chimp':          bot.chimp_test,
        'memory':         bot.visual_memory,
        'typing':         bot.typing
    }
    return methods.get(endpoint)

def get_browser_choice():
    """Get valid browser choice from user"""
    while True:
        choice = input("Choose browser (Firefox, Chrome, Edge): ").lower().strip()
        if choice in browsers:
            return choice
        print("Invalid browser. Choose Firefox, Chrome, or Edge.")

def get_test_choice():
    """Get valid test choice from user"""
    test_list = ", ".join([name.title() for name in tests.keys()])
    while True:
        choice = input(f"\nSelect test ({test_list}): ").lower().strip()
        if choice in tests:
            return choice
        print("Invalid test.")

def get_level_choice(endpoint):
    """Get valid level choice for level-based tests"""
    while True:
        try:
            levels = int(input("How many levels: "))
            if levels <= 0:
                print("Levels must be greater than 0")
                continue
            if endpoint == 'chimp' and levels > 37:
                print("Chimp Test maximum is 37 levels")
                continue
            return levels
        except ValueError:
            print("Enter a valid number")

def run_test(browser_choice, driver=None):
    """Run a single test session"""
    #Get test selection
    test_choice = get_test_choice()
    endpoint = tests[test_choice]
    
    #Get level if needed
    levels = None
    if endpoint in level_based_tests:
        levels = get_level_choice(endpoint)
    
    #Initialize driver if needed
    if driver is None:
        print("Starting browser...")
        driver = browsers[browser_choice]()
    
    #Run the test
    bot = HumanBenchmarkBot(driver)
    method = get_test_method(bot, endpoint)
    
    print(f"Running {test_choice.title()}...")
    if levels is not None:
        method(levels)
    else:
        method()
    
    print("Test completed!")
    return driver

def run_another():
    """Ask if user wants to run another test"""
    while True:
        choice = input("\nRun another test? (y/n): ").lower().strip()
        if "y" in choice:
            return True
        elif "n" in choice:
            return False
        print("Please enter a valid answer.")

def main():
    """Main program loop"""
    print("Human Benchmark Bot - Terminal Version")
    print("=" * 40)
    
    browser_choice = get_browser_choice()
    driver = None
    
    try:
        while True:
            driver = run_test(browser_choice, driver)
            
            if not run_another():
                break
                
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()
        print("Program ended")

if __name__ == "__main__":
    main()