"""
Настройки для тестов Candy Crush Saga
"""

# Настройки Appium
APPIUM_CONFIG = {
    'platform_name': 'Android',
    'automation_name': 'UiAutomator2',
    'app_package': 'com.king.candycrushsaga',
    'app_activity': '.CandyCrushSagaActivity',
    'new_command_timeout': 300,
    'no_reset': True,
    'full_reset': False,
    'server_url': 'http://localhost:4723'
}

# Настройки ожиданий
TIMEOUTS = {
    'implicit_wait': 10,
    'explicit_wait': 15,
    'app_launch_wait': 10,
    'element_wait': 5
}

# Настройки отчетов
REPORTS = {
    'screenshot_on_failure': True,
    'save_page_source': True,
    'html_report': True
}

# Настройки устройства (можно переопределить)
DEVICE_CONFIG = {
    'device_name': 'Android Emulator',
    'platform_version': '11.0',  # Можно изменить под свою версию
    'udid': None  # Автоопределение
}
