import os
from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import or_

from connect_db import engine
from models import Base, Project, Country, Type

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "supports_credentials": True,
                                 "allow_headers": ["Content-Type", "Authorization"]}})

app.config['UPLOAD_FOLDER'] = 'project_storage'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def get_new_version(id):
    versions = db_session.query(Project).filter(Project.id == id).all()
    return max([v.version for v in versions], default=0) + 1


@app.route('/api/countries', methods=['POST'])
def create_country():
    name = request.json['name']
    new_country = Country(name=name)
    db_session.add(new_country)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Integrity error"}), 400
    return jsonify({"message": "Country created successfully", "country_id": new_country.country_id}), 201


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = db_session.query(Country).all()
    return jsonify([country.as_dict() for country in countries])


@app.route('/api/types', methods=['POST'])
def create_type():
    name = request.json['name']
    new_type = Type(name=name)
    db_session.add(new_type)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Integrity error"}), 400
    return jsonify({"message": "Type created successfully", "type_id": new_type.type_id}), 201


@app.route('/api/types', methods=['GET'])
def get_types():
    types = db_session.query(Type).all()
    return jsonify([type_.as_dict() for type_ in types])


@app.route('/api/projects', methods=['POST'])
def create_project():
    name = request.form['name']
    description = request.form['description']
    country_id = request.form['country_id']
    type_id = request.form['type_id']

    country = db_session.query(Country).filter(Country.country_id == country_id).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    type_ = db_session.query(Type).filter(Type.type_id == type_id).first()
    if not type_:
        return jsonify({"error": "Type not found"}), 404

    new_project = Project(name=name, description=description, country_id=country_id, type_id=type_id)

    version = get_new_version(new_project.project_id)

    db_session.add(new_project)
    db_session.commit()
    project_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(new_project.project_id), f"v{version}")
    os.makedirs(project_folder, exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(project_folder, filename)
        file.save(filepath)
        new_project.file_path = filepath

    if 'image' in request.files:
        image = request.files['image']
        imagename = secure_filename(image.filename)
        imagepath = os.path.join(project_folder, imagename)
        image.save(imagepath)
        new_project.image_path = imagepath

    new_project.latitude = request.form.get('latitude')
    new_project.longitude = request.form.get('longitude')
    new_project.version = version
    new_project.id = new_project.project_id

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Integrity error"}), 400

    return jsonify({"message": "Project created successfully", "project_id": new_project.project_id, "version": version}), 201


@app.route('/api/projects', methods=['GET'])
def get_projects():
    country_id = request.args.get('country_id')
    type_id = request.args.get('type_id')
    search_text = request.args.get('search_text')

    query = db_session.query(Project).filter(Project.deleted_at.is_(None))

    if country_id:
        query = query.filter(Project.country_id == country_id)

    if type_id:
        query = query.filter(Project.type_id == type_id)

    if search_text:
        search_text = f"%{search_text}%"
        query = query.filter(or_(Project.name.ilike(search_text), Project.description.ilike(search_text)))

    projects = query.order_by(Project.id, Project.version.desc()).all()

    latest_projects = {}
    for project in projects:
        if project.id not in latest_projects:
            latest_projects[project.id] = project

    return jsonify([project.as_dict() for project in latest_projects.values()])


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = db_session.query(Project).filter(Project.id == project_id, Project.deleted_at.is_(None)).order_by(Project.version.desc()).first()
    if project:
        return jsonify(project.as_dict())
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/api/projects/<int:project_id>/versions', methods=['GET'])
def get_project_versions(project_id):
    projects = db_session.query(Project).filter(Project.id == project_id, Project.deleted_at.is_(None)).order_by(Project.version.desc()).all()
    if projects:
        return jsonify([project.as_dict() for project in projects])
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/api/projects/<int:project_id>/versions/<int:version>', methods=['GET'])
def get_project_version(project_id, version):
    project = db_session.query(Project).filter(Project.id == project_id, Project.version == version, Project.deleted_at.is_(None)).first()
    if project:
        return jsonify(project.as_dict())
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = db_session.query(Project).filter(Project.id == project_id).order_by(Project.version.desc()).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    version = get_new_version(project_id)

    new_project = Project(
        id=project.id,
        name=request.form.get('name', project.name),
        description=request.form.get('description', project.description),
        country_id=request.form.get('country_id', project.country_id),
        type_id=request.form.get('type_id', project.type_id),
        version=version,
        latitude=request.form.get('latitude', project.latitude),
        longitude=request.form.get('longitude', project.longitude),
        file_path=project.file_path,
        image_path=project.image_path
    )
    db_session.add(new_project)
    db_session.commit()

    project_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(new_project.id), f"v{version}")
    os.makedirs(project_folder, exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(project_folder, filename)
        file.save(filepath)
        new_project.file_path = filepath

    if 'image' in request.files:
        image = request.files['image']
        imagename = secure_filename(image.filename)
        imagepath = os.path.join(project_folder, imagename)
        image.save(imagepath)
        new_project.image_path = imagepath

    db_session.commit()
    return jsonify({"message": "Project updated successfully", "version": version}), 200


@app.route('/api/projects/<int:project_id>/file', methods=['GET'])
def get_project_file(project_id):
    project = db_session.query(Project).filter(Project.id == project_id).order_by(Project.version.desc()).first()
    if project and project.file_path:
        return send_from_directory(os.path.dirname(project.file_path), os.path.basename(project.file_path))
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/api/projects/<int:project_id>/file/<int:version>', methods=['GET'])
def get_project_version_file(project_id, version):
    project = db_session.query(Project).filter(Project.id == project_id, Project.version == version).first()
    if project and project.file_path:
        return send_from_directory(os.path.dirname(project.file_path), os.path.basename(project.file_path))
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/api/projects/<int:project_id>/image', methods=['GET'])
def get_project_image(project_id):
    project = db_session.query(Project).filter(Project.id == project_id).order_by(Project.version.desc()).first()
    if project and project.image_path:
        return send_from_directory(os.path.dirname(project.image_path), os.path.basename(project.image_path))
    else:
        return jsonify({"error": "Image not found"}), 404


@app.route('/api/projects/<int:project_id>/image/<int:version>', methods=['GET'])
def get_project_version_image(project_id, version):
    project = db_session.query(Project).filter(Project.id == project_id, Project.version == version).first()
    if project and project.image_path:
        return send_from_directory(os.path.dirname(project.image_path), os.path.basename(project.image_path))
    else:
        return jsonify({"error": "Image not found"}), 404


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = db_session.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    project.deleted_at = datetime.utcnow()
    db_session.commit()
    return jsonify({"message": "Project marked as deleted"}), 200


@app.route('/api/countries/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    country = db_session.query(Country).filter(Country.country_id == country_id).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    db_session.delete(country)
    db_session.commit()
    return jsonify({"message": "Country deleted successfully"}), 200


@app.route('/api/types/<int:type_id>', methods=['DELETE'])
def delete_type(type_id):
    type_ = db_session.query(Type).filter(Type.type_id == type_id).first()
    if not type_:
        return jsonify({"error": "Type not found"}), 404

    db_session.delete(type_)
    db_session.commit()
    return jsonify({"message": "Type deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
