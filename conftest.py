import pytest
import time
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.settings import APPIUM_CONFIG, TIMEOUTS

@pytest.fixture
def driver():
    """Создание драйвера для тестов"""
    
    # Настройки для Android из конфига
    options = UiAutomator2Options()
    options.platform_name = APPIUM_CONFIG['platform_name']
    options.app_package = APPIUM_CONFIG['app_package']
    options.app_activity = APPIUM_CONFIG['app_activity']
    options.automation_name = APPIUM_CONFIG['automation_name']
    options.new_command_timeout = APPIUM_CONFIG['new_command_timeout']
    options.no_reset = APPIUM_CONFIG['no_reset']
    options.full_reset = APPIUM_CONFIG['full_reset']
    
    # Подключение к Appium серверу
    driver = webdriver.Remote(
        command_executor=APPIUM_CONFIG['server_url'],
        options=options
    )
    
    # Настройка implicit wait
    driver.implicitly_wait(TIMEOUTS['implicit_wait'])
    
    # Ждем загрузки приложения
    time.sleep(TIMEOUTS['app_launch_wait'])
    
    yield driver
    
    # Закрываем драйвер после тестов
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def setup_test_run():
    """Настройка перед запуском всех тестов"""
    print("\n🎮 Начинаем тестирование Candy Crush Saga!")
    
    # Создаем папку для скриншотов если её нет
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    yield
    print("\n✅ Тестирование завершено!")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Получаем драйвер из фикстуры
        driver = item.funcargs.get('driver')
        if driver:
            # Делаем скриншот при падении теста
            screenshot_name = f"FAILED_{item.name}_{int(time.time())}"
            screenshot_path = f"reports/{screenshot_name}.png"
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Скриншот ошибки сохранен: {screenshot_path}")
            except Exception as e:
                print(f"\n❌ Не удалось сделать скриншот: {e}")
