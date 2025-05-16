import time
import webbrowser
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
            sequence, last_active_square = [], None
            while len(sequence) < num_squares:
                active = self.driver.find_elements(By.CSS_SELECTOR, "div.square.active")
                if active:
                    square = active[0]
                    if last_active_square is None or square != last_active_square:
                        sequence.append(square)
                    last_active_square = square
            time.sleep(1)
            for el in sequence:
                el.click()
    
    def aim_trainer(self):
        self.navigate_to_test("aim")

        for _ in range(31):
            target = self.driver.find_element(By.CSS_SELECTOR, '[data-aim-target="true"]')
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
            self.driver.execute_script("""
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
            input_field = WebDriverWait(self.driver, 100, poll_frequency=0.001).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
            )
            input_field.send_keys(number)

            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()

            if num != lvls - 1:
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'NEXT')]").click()
    
    def verbal_memory(self, lvls):
        self.navigate_to_test("verbal-memory")

        seen_words = set()

        self.driver.find_element(By.XPATH, "//button[contains(text(),'Start')]").click()

        for _ in range(lvls):
            word = self.driver.find_element(By.CLASS_NAME, 'word').text
            if word in seen_words:
                self.driver.find_element(By.XPATH, "//button[contains(text(),'SEEN')]").click()
            else:
                seen_words.add(word)
                self.driver.find_element(By.XPATH, "//button[contains(text(),'NEW')]").click()
    
    def chimp_test(self, lvls):
        self.navigate_to_test("chimp")

        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start Test')]").click()

        for num in range(lvls):
            numbers = 4 + num
            for i in range(1, numbers + 1):
                self.driver.find_element(By.XPATH, f'//div[@data-cellnumber="{i}"]').click()
            if num != lvls - 1:
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
    
    def visual_memory(self, lvls):
        self.navigate_to_test("memory")

        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]").click()

        num_squares = 3

        for _ in range(lvls):
            active_elements = []
            while len(active_elements) != num_squares:
                active_elements = self.driver.find_elements(By.CSS_SELECTOR,'div.active')
            time.sleep(1.25)
            for el in active_elements:
                el.click()
            num_squares += 1
    
    def typing(self):
        self.navigate_to_test("typing")

        text = ""
        raw_text = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div/span')
        for raw_character in raw_text:
            char = raw_character.text or " "
            text += char
        typing_form = self.driver.find_element(By.CSS_SELECTOR, ".letters.notranslate")
        typing_form.send_keys(text)

browsers = {
    'firefox': lambda: webdriver.Firefox(),
    'chrome': lambda: webdriver.Chrome(),
    'edge': lambda: webdriver.Edge()
}

mode_functions = {
    'reactiontime': 'reaction_time',
    'sequencememory': 'sequence_memory',
    'aimtrainer': 'aim_trainer',
    'numbermemory': 'number_memory',
    'verbalmemory': 'verbal_memory',
    'chimptest': 'chimp_test',
    'visualmemory': 'visual_memory',
    'typing': 'typing'
}

level_based_tests = ['sequencememory', 'numbermemory', 'verbalmemory', 'chimptest', 'visualmemory']


def run_test(browser_choice, driver=None):
    while True:
        mode = input("\nMode (Reaction Time, Sequence Memory, Aim Trainer, Number Memory, Verbal Memory, Chimp Test, Visual Memory, Typing): ").lower().replace(" ", "")
        if mode in mode_functions:
            break
        print("Invalid mode.")
    levels = None
    if mode in level_based_tests:
        while True:
            try:
                levels = int(input("How many levels: "))
                if levels > 0 and (mode != "chimptest" or levels <= 37):
                    break
            except ValueError:
                pass
            print("Enter a valid number" + (" ≤ 37" if mode=="chimptest" else " > 0"))
    if driver is None:
        driver = browsers[browser_choice]()
    bot = HumanBenchmarkBot(driver)
    method = getattr(bot, mode_functions[mode])
    if levels is not None:
        method(levels)
    else:
        method()
    return driver

def main():
    while True:
        browser_choice = input("Choose driver (Firefox, Chrome, Edge): ").lower().replace(" ", "")
        if browser_choice in browsers:
            break
        print("Invalid driver.")
    driver = None

    while True:
        driver = run_test(browser_choice, driver)
        again = input("\nRun another? (y/n): ").lower().strip()
        if 'n' in again:
            driver.quit()
        elif 'y' in again:
            continue

if __name__ == "__main__":
    main()
