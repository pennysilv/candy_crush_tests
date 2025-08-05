"""
Вспомогательные функции для тестов
"""

import time
import json
import os
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy

def wait_and_screenshot(driver, name="screenshot", delay=2):
    """Подождать и сделать скриншот"""
    time.sleep(delay)
    timestamp = int(time.time())
    filename = f"reports/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"📸 Скриншот: {filename}")
    return filename

def find_element_with_text(driver, text, timeout=10):
    """Найти элемент содержащий текст"""
    xpath = f"//*[contains(@text, '{text}') or contains(@content-desc, '{text}')]"
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
        print(f"✅ Найден элемент с текстом: {text}")
        return element
    except:
        print(f"❌ Элемент с текстом '{text}' не найден")
        return None

def click_if_present(driver, xpath, timeout=5):
    """Кликнуть на элемент если он есть"""
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
        element.click()
        print(f"✅ Кликнули на элемент: {xpath}")
        return True
    except:
        print(f"❌ Не удалось кликнуть: {xpath}")
        return False

def get_all_clickable_info(driver):
    """Получить информацию о всех кликабельных элементах"""
    elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
    info = []
    
    for i, element in enumerate(elements):
        try:
            element_info = {
                'index': i,
                'text': element.get_attribute('text') or '',
                'content_desc': element.get_attribute('content-desc') or '',
                'resource_id': element.get_attribute('resource-id') or '',
                'class': element.get_attribute('class') or '',
                'bounds': element.get_attribute('bounds') or ''
            }
            info.append(element_info)
        except Exception as e:
            print(f"Ошибка получения информации об элементе {i}: {e}")
    
    return info

def wait_for_screen_change(driver, initial_source, timeout=10):
    """Ждать изменения экрана"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        current_source = driver.page_source
        if current_source != initial_source:
            print("✅ Экран изменился")
            return True
        time.sleep(1)
    
    print("❌ Экран не изменился за отведенное время")
    return False

def save_page_source(driver, name="page_source"):
    """Сохранить исходный код страницы"""
    timestamp = int(time.time())
    filename = f"reports/{name}_{timestamp}.xml"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 Исходный код сохранен: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Ошибка сохранения исходного кода: {e}")
        return None

def swipe_screen(driver, direction="down"):
    """Свайп по экрану в указанном направлении"""
    size = driver.get_window_size()
    
    if direction == "down":
        start_x = size['width'] // 2
        start_y = size['height'] * 0.8
        end_x = size['width'] // 2
        end_y = size['height'] * 0.2
    elif direction == "up":
        start_x = size['width'] // 2
        start_y = size['height'] * 0.2
        end_x = size['width'] // 2
        end_y = size['height'] * 0.8
    elif direction == "left":
        start_x = size['width'] * 0.8
        start_y = size['height'] // 2
        end_x = size['width'] * 0.2
        end_y = size['height'] // 2
    elif direction == "right":
        start_x = size['width'] * 0.2
        start_y = size['height'] // 2
        end_x = size['width'] * 0.8
        end_y = size['height'] // 2
    else:
        print(f"❌ Неизвестное направление: {direction}")
        return False
    
    try:
        driver.swipe(start_x, start_y, end_x, end_y, 1000)
        print(f"✅ Свайп {direction} выполнен")
        return True
    except Exception as e:
        print(f"❌ Ошибка свайпа: {e}")
        return False

def tap_center(driver):
    """Тап по центру экрана"""
    size = driver.get_window_size()
    center_x = size['width'] // 2
    center_y = size['height'] // 2
    
    try:
        driver.tap([(center_x, center_y)])
        print("✅ Тап по центру экрана")
        return True
    except Exception as e:
        print(f"❌ Ошибка тапа по центру: {e}")
        return False

def wait_for_element_disappear(driver, xpath, timeout=10):
    """Ждать исчезновения элемента"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            driver.find_element(AppiumBy.XPATH, xpath)
            time.sleep(1)  # Элемент еще есть, ждем
        except:
            print(f"✅ Элемент исчез: {xpath}")
            return True
    
    print(f"❌ Элемент не исчез за {timeout}с: {xpath}")
    return False

def create_test_report(test_name, results):
    """Создать отчет о тесте"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/test_report_{test_name}_{timestamp}.json"
    
    report = {
        'test_name': test_name,
        'timestamp': timestamp,
        'results': results
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📊 Отчет сохранен: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        return None
