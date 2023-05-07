import os
import subprocess


def run_project():
    project_name = input("Введите название проекта: ")

    project_dir = os.path.join(os.getcwd(), project_name)
    if not os.path.exists(project_dir):
        print(f"Проект {project_name} не найден.")
        return

    venv_dir = os.path.join(project_dir, 'venv')
    if not os.path.exists(venv_dir):
        print(f"Виртуальное окружение для проекта {project_name} не найдено.")
        return

    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(venv_dir, 'bin', 'activate')
    command = f'cmd.exe /C "{activate_script} && python manage.py runserver"'
    subprocess.run(command, shell=True, encoding='utf-8', cwd=project_dir)


def freeze_dependencies():
    project_name = input("Введите название проекта: ")

    project_dir = os.path.join(os.getcwd(), project_name)
    if not os.path.exists(project_dir):
        print(f"Проект {project_name} не найден.")
        return

    venv_dir = os.path.join(project_dir, 'venv')
    if not os.path.exists(venv_dir):
        print(f"Виртуальное окружение для проекта {project_name} не найдено.")
        return

    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(venv_dir, 'bin', 'activate')
    command = f'cmd.exe /C "{activate_script} && pip freeze > requirements.txt"'
    subprocess.run(command, shell=True, encoding='utf-8', cwd=project_dir)
    print(f"Зависимости проекта {project_name} заморожены.")


if __name__ == '__main__':
    while True:
        print("Выберите действие:")
        print("1. Запустить проект Django")
        print("2. Заморозить зависимости")
        print("3. Выйти")
        choice = input("Введите номер действия (1-3): ")

        if choice == '1':
            run_project()
        elif choice == '2':
            freeze_dependencies()
        elif choice == '3':
            break
        else:
            print("Неверный ввод. Пожалуйста, введите номер действия (1-3).")
