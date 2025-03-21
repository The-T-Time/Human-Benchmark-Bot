#Reaction Time: Done
#Sequence Memory: Done
#Aim Trainer: Done
#Number Memory: Done
#Verbal Memory: Done
#Chimp Test: Done
#Visual Memory: Done
#Typing: Done

import time #for .sleep()
import webbrowser #opens a new tab
from selenium import webdriver #opens a new window
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #used for number memory. Trying to think of a different way. Now used with aim trainer also
from selenium.webdriver.support import expected_conditions as EC #used for number memory. Trying to think of a different way. Now used with aim trainer also

def Reaction_Time(driver):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/reactiontime")
    time.sleep(3)

    lvls = 5

    start = driver.find_element(By.CLASS_NAME, 'view-splash')
    start.click()
    
    for num in range(lvls):
            green = WebDriverWait(driver, 10, poll_frequency=0.001).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'view-go'))
            ).click()
            if num != 4:
                blue = driver.find_element(By.CLASS_NAME, 'view-result')
                blue.click()
    
    time.sleep(40000)

def Sequence_Memory(driver, lvls):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/sequence")
    time.sleep(3)

    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
    start_button.click()

    for num_squares in range(1, lvls + 1):

        sequence = []
        last_active_square = None

        while len(sequence) < num_squares:
            current_active = driver.find_elements(By.CSS_SELECTOR, "div.square.active")
            if current_active:
                square = current_active[0]
                if last_active_square is None or square != last_active_square:
                    sequence.append(square)
                last_active_square = square

        time.sleep(1)

        for element in sequence:
                element.click()

    time.sleep(40000)

def Aim_Trainer(driver):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/aim")
    time.sleep(3)

    for i in range(31):
        target = driver.find_element(By.CSS_SELECTOR, '[data-aim-target="true"]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", target)
        driver.execute_script("""
            var elem = arguments[0];
            ['mousedown', 'mouseup', 'click'].forEach(function(evtType) {
                var event = new MouseEvent(evtType, {view: window, bubbles: true, cancelable: true});
                elem.dispatchEvent(event);
            });
        """, target)

    time.sleep(40000)

def Number_Memory(driver, lvls):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/number-memory")
    time.sleep(3)

    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
    start_button.click()

    for num in range(lvls):
        number = driver.find_element(By.CLASS_NAME, 'big-number').text
        input_field = WebDriverWait(driver, 100, poll_frequency=0.001).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
        )
        input_field.send_keys(number)

        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()

        if num != lvls - 1:
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'NEXT')]")
            next_button.click()
        
    time.sleep(40000)

def Verbal_Memory(driver, lvls):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/verbal-memory")

    seen_words = set()

    
    start_button = driver.find_element(By.XPATH, "//button[contains(text(),'Start')]")
    start_button.click()

    for num in range(lvls):
        word = driver.find_element(By.CLASS_NAME, 'word').text
        if word in seen_words:
            seen_button = driver.find_element(By.XPATH, "//button[contains(text(),'SEEN')]")
            seen_button.click()
            num += 1
        else:
            seen_words.add(word)
            new_button = driver.find_element(By.XPATH, "//button[contains(text(),'NEW')]")
            new_button.click()
            num += 1

    time.sleep(40000)

def Chimp_Test(driver, lvls):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/chimp")
    time.sleep(3)

    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start Test')]")
    start_button.click()

    for num in range(lvls):
        numbers = 4 + num
        for i in range(1, numbers + 1):
            cell = driver.find_element(By.XPATH, f'//div[@data-cellnumber="{i}"]')
            cell.click()

        if num != lvls - 1:
            Continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            Continue_button.click()

    time.sleep(40000)

def Visual_Memory(driver, lvls):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/memory")
    time.sleep(3)

    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
    start_button.click()

    num_squares = 3

    for num in range(lvls):
        active_elements = []
        while len(active_elements) != num_squares:
            active_elements = driver.find_elements(By.CSS_SELECTOR,'div.active')
        
        time.sleep(1.25)
        
        for element in active_elements:
            element.click()
      
        num_squares += 1
    time.sleep(40000)

def Typing(driver):
    driver.maximize_window()

    driver.get("https://humanbenchmark.com/tests/typing")
    time.sleep(3)

    text = ""
    position = 0
    raw_text = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div/span')
    for raw_character in raw_text:
        character = raw_character.text
        if character == "":
            character = " "
        text += character
        
        position += 1

    typing_form = driver.find_element(By.CSS_SELECTOR, ".letters.notranslate")
    typing_form.send_keys(text)

    time.sleep(40000)

mode_functions = {
    'reactiontime': Reaction_Time,
    'sequencememory': Sequence_Memory,
    'aimtrainer': Aim_Trainer,
    'numbermemory': Number_Memory,
    'verbalmemory': Verbal_Memory,
    'chimptest': Chimp_Test,
    'visualmemory': Visual_Memory,
    'typing': Typing
}

browsers = {
    'firefox': lambda: webdriver.Firefox(),
    'chrome': lambda: webdriver.Chrome(),
    'edge': lambda: webdriver.Edge()
}

while True:
    browser_choice = input("Choose driver (Firefox, Chrome, Edge): ")
    browser_choice = browser_choice.lower().replace(" ","")
    if browser_choice in browsers:
        break
    else:
        print("Invalid driver selected. Please choose from Firefox, Chrome, or Edge.")

while True:
    mode = input("What mode (Reaction Time, Sequence Memory, Aim Trainer, Number Memory, Verbal Memory, Chimp Test, Visual Memory, Typing): ")
    mode = mode.lower().replace(" ","")
    if mode in mode_functions:
        if mode in ["sequencememory", "numbermemory", "verbalmemory", "chimptest", "visualmemory"]:
            while True:
                try:
                    lvls = int(input("How many levels: "))    
                except ValueError:
                    print("Please enter a valid number.")
                if lvls > 0: 
                    if mode == "Chimp Test" and lvls > 37:
                        print("Please enter a number 37 or less.")
                    else:
                        break
                else:
                    print("Please enter a number greater than 0.")
                    continue
            driver = browsers[browser_choice]()
            mode_functions[mode](driver, lvls)
        else:
            driver = browsers[browser_choice]()
            mode_functions[mode](driver)
        break
    else:
        print("Invalid mode selected.")

