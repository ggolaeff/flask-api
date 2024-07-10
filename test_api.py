import requests

# URL базового API
base_url = 'http://localhost:5000/api'


# Создание новой страны
def create_country(name):
    url = f'{base_url}/countries'
    data = {'name': name}
    response = requests.post(url, json=data)
    print(response.status_code, response.json())
    return response.json().get('country_id')


# Получение списка всех стран
def get_countries():
    url = f'{base_url}/countries'
    response = requests.get(url)
    print(response.status_code, response.json())


# Создание нового типа
def create_type(name):
    url = f'{base_url}/types'
    data = {'name': name}
    response = requests.post(url, json=data)
    print(response.status_code, response.json())
    return response.json().get('type_id')


# Получение списка всех типов
def get_types():
    url = f'{base_url}/types'
    response = requests.get(url)
    print(response.status_code, response.json())


# Создание нового проекта
def create_project(name, description, country_id, type_id, lat, long,  file_path=None, image_path=None):
    url = f'{base_url}/projects'
    files = {}
    if file_path:
        files['file'] = open(file_path, 'rb')
    if image_path:
        files['image'] = open(image_path, 'rb')
    data = {
        'name': name,
        'description': description,
        'country_id': str(country_id),
        'type_id': str(type_id),
        'latitude': str(lat),
        'longitude': str(long)
    }
    response = requests.post(url, files=files, data=data)
    print(response.status_code, response.json())


# Получение списка всех проектов
def get_projects():
    url = f'{base_url}/projects'
    response = requests.get(url)
    print(response.status_code, response.json())


# Получение определенного проекта
def get_project(project_id):
    url = f'{base_url}/projects/{project_id}'
    response = requests.get(url)
    print(response.status_code, response.json())


# Обновление проекта
def update_project(project_id, name, description, country_id, type_id, lat, long, file_path=None, image_path=None):
    url = f'{base_url}/projects/{project_id}'
    files = {}
    if file_path:
        files['file'] = open(file_path, 'rb')
    if image_path:
        files['image'] = open(image_path, 'rb')
    data = {
        'name': name,
        'description': description,
        'country_id': str(country_id),
        'type_id': str(type_id),
        'latitude': str(lat),
        'longitude': str(long)
    }
    response = requests.put(url, files=files, data=data)
    print(response.status_code, response.json())


# Получение файла проекта
def get_project_file(project_id):
    url = f'{base_url}/projects/{project_id}/file'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'project_{project_id}_file.zip', 'wb') as f:
            f.write(response.content)
        print(f'File for project {project_id} downloaded successfully')
    else:
        print(response.status_code, response.json())


# Получение изображения проекта
def get_project_image(project_id):
    url = f'{base_url}/projects/{project_id}/image'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'project_{project_id}_image.jpg', 'wb') as f:
            f.write(response.content)
        print(f'Image for project {project_id} downloaded successfully')
    else:
        print(response.status_code, response.json())


if __name__ == '__main__':
    # # Создание страны и типа
    # country_id = create_country('USA')
    # type_id = create_type('Map')
    #
    # Создание проекта с файлом и изображением
    # create_project('Project1', 'Description1', 1, 1, 'test.zip', 'test.jpg')

    # # Получение списка всех проектов
    # get_projects()
    #
    # # Получение определенного проекта
    # get_project(1)
    #
    # # Обновление проекта
    # update_project(2, 'UpdatedProject', 'UpdatedDescription', 1, 1, 30, 90)

    # # Получение файла проекта
    # get_project_file(1)
    #
    # # Получение изображения проекта
    # get_project_image(1)
    pass
