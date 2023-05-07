import os
import subprocess


def create_project():
    project_name = input("Введите название проекта: ")
    project_dir = os.path.join(os.getcwd(), project_name)

    os.makedirs(project_dir)

    venv_dir = os.path.join(project_dir, 'venv')
    subprocess.run(['python', '-m', 'venv', venv_dir], check=True)

    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') \
        if os.name == 'nt' \
        else os.path.join(venv_dir, 'bin', 'activate')
    command = f'{activate_script} && pip install django'
    subprocess.run(command, shell=True, check=True)

    django_admin = os.path.join(venv_dir,
                                'Scripts',
                                'django-admin') \
        if os.name == 'nt' \
        else os.path.join(venv_dir, 'bin', 'django-admin')

    subprocess.run([django_admin, 'startproject', project_name, project_dir], check=True)
    print(f"Проект {project_name} успешно создан.")


if __name__ == '__main__':
    create_project()
