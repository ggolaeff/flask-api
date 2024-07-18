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
def create_project(name, description, country_id, type_id, lat, long, file_path=None, image_path=None):
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
    return response.json().get('project_id')


# Функция для получения списка проектов с возможностью фильтрации
def get_projects(country_id=None, type_id=None, search_text=None):
    url = f'{base_url}/projects'
    params = {}
    if country_id:
        params['country_id'] = country_id
    if type_id:
        params['type_id'] = type_id
    if search_text:
        params['search_text'] = search_text

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Запрос успешен")
        projects = response.json()
        for project in projects:
            print(project)
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.json())


# Получение определенного проекта (последняя версия)
def get_project(project_id):
    url = f'{base_url}/projects/{project_id}'
    response = requests.get(url)
    print(response.status_code, response.json())


# Получение всех версий проекта
def get_project_versions(project_id):
    url = f'{base_url}/projects/{project_id}/versions'
    response = requests.get(url)
    print(response.status_code, response.json())


# Получение определенной версии проекта
def get_project_version(project_id, version_id):
    url = f'{base_url}/projects/{project_id}/versions/{version_id}'
    response = requests.get(url)
    print(response.status_code, response.json())


# Обновление проекта
def update_project(project_id, name=None, description=None, country_id=None, type_id=None, lat=None, long=None, file_path=None, image_path=None):
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
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid response"}
    print(response.status_code, response_data)


# Удаление проекта
def delete_project(project_id):
    url = f'{base_url}/projects/{project_id}'
    response = requests.delete(url)
    print(response.status_code, response.json())


# Удаление страны
def delete_country(country_id):
    url = f'{base_url}/countries/{country_id}'
    response = requests.delete(url)
    print(response.status_code, response.json())


# Удаление типа
def delete_type(type_id):
    url = f'{base_url}/types/{type_id}'
    response = requests.delete(url)
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
    # Создание страны и типа
    # country_id = create_country('Russia')
    # # type_id = create_type('Map')
    #
    # # Создание проекта с файлом и изображением
    # project_id = create_project('New_project', 'proj', country_id, 1, '40.7128', '-74.0060', 'test.zip', 'test.jpg')
    #
    # # Получение списка всех проектов (последние версии)
    get_projects(search_text='7', country_id=2, type_id=1)
    #
    # # # Удаление проекта
    # delete_project(9)
    # #
    # # # Получение списка всех проектов (последние версии) после удаления
    # get_projects()
    #
    # # Удаление страны и типа
    # delete_country(2)
    #
    # get_project_versions(6)
    # # Получение списка всех стран и типов после удаления
    # get_countries()
    # get_types()
    pass
