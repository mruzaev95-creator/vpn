import subprocess
import sys
import os
import ctypes

# Проверка на права администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Перезапускаем с правами администратора
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{__file__}"', None, 1
    )
    sys.exit()

# Основной код
server_file = os.path.join(os.path.dirname(__file__), "server.txt")

if not os.path.exists(server_file):
    print(f"Файл server.txt не найден!")
    print(f"Положите server.txt в папку с vpn.py")
    input("Нажмите Enter...")
    sys.exit(1)

with open(server_file, "r") as f:
    server = f.read().strip()

if not server or "ЗАМЕНИТЕ" in server:
    print("Впишите адрес сервера в server.txt")
    input("Нажмите Enter...")
    sys.exit(1)

print(f"Сервер: {server}")

result = subprocess.run(
    ["netsh", "winhttp", "set", "proxy", server],
    capture_output=True,
    text=True,
    shell=True
)

if "успешно" in result.stdout.lower():
    print("Прокси включен!")
else:
    print(f"Результат: {result.stdout}")
    print(f"Ошибка: {result.stderr}")

input("Нажмите Enter...")