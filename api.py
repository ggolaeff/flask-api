import os
from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

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

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    new_project = Project(name=name, description=description, country_id=country_id, type_id=type_id, file_path=filepath)

    db_session.add(new_project)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Integrity error"}), 400

    return jsonify({"message": "Project created successfully"}), 201


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = db_session.query(Project).all()
    return jsonify([project.as_dict() for project in projects])


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = db_session.query(Project).filter(Project.project_id == project_id).first()
    if project:
        return jsonify(project.as_dict())
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = db_session.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    name = request.form.get('name', project.name)
    description = request.form.get('description', project.description)
    country_id = request.form.get('country_id', project.country_id)
    type_id = request.form.get('type_id', project.type_id)

    country = db_session.query(Country).filter(Country.country_id == country_id).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    type_ = db_session.query(Type).filter(Type.type_id == type_id).first()
    if not type_:
        return jsonify({"error": "Type not found"}), 404

    project.name = name
    project.description = description
    project.country_id = country_id
    project.type_id = type_id

    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        project.file_path = filepath

    db_session.commit()
    return jsonify({"message": "Project updated successfully"}), 200


@app.route('/api/projects/<int:project_id>/file', methods=['GET'])
def get_project_file(project_id):
    project = db_session.query(Project).filter(Project.project_id == project_id).first()
    if project and project.file_path:
        return send_from_directory(app.config['UPLOAD_FOLDER'], project.file_path.split('/')[-1])
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
