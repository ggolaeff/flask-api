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


# Получение списка всех проектов (последние версии)
def get_projects():
    url = f'{base_url}/projects'
    response = requests.get(url)
    print(response.status_code, response.json())


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
    # country_id = create_country('USA')
    # type_id = create_type('Map')

    # # Создание проекта с файлом и изображением
    # print('create project')
    # project_id = create_project('Project7', 'Description7', 1, 1, '40.7128', '-74.0060', 'test.zip', 'test.jpg')

    # print('all projects before update')
    # # Получение списка всех проектов (последние версии)
    # get_projects()

    # print('get project by id')
    # # Получение определенного проекта (последняя версия)
    # get_project(5)

    # print('updating project')
    # Обновление проекта: изменение описания и замена файла
    # update_project(1, 'Project6', country_id=1, type_id=1, lat='40.7128', long='-74.0060', file_path='test2.zip')
    #
    # print('all projects after updating')
    # # Получение списка всех проектов (последние версии) после обновления
    # get_projects()
    #
    # print('get project by id after updating')
    # # Получение определенного проекта (последняя версия) после обновления
    # get_project(6)
    #
    # print('get all versions by project id')
    # # Получение всех версий проекта
    get_project_versions(1)

    # print('get certain project version')
    # # Получение определенной версии проекта (версия 1)
    # get_project_version(6, 1)

    # print('project file')
    # # Получение файла проекта
    # get_project_file(project_id)
    #
    # print('project image')
    # # Получение изображения проекта
    # get_project_image(project_id)
    pass
