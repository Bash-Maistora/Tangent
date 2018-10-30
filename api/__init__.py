from flask import Flask, jsonify, abort, request
import requests
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


def create_app(config_name):
    from api.models import db
    from api.models import Comment

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.create_all(app=app)

    def watson_tone(comment):
        r = requests.get('https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone', params={'text': comment, 'version': '2017-09-21', 'sentences': 'true'}, auth=('96930825-4ef8-4bb5-b8c2-6d75816a58bf', 'qeU7UpHp8TNb'))
        response = r.json()
        if response.get('document_tone').get('tones'):
            tone = response.get('document_tone').get('tones')[0].get('tone_name')
        else:
            tone = ''
        return tone


    @app.route('/comments', methods=['GET', 'POST'])
    def comments():
        if request.method == 'POST':
            comment = str(request.form.get('comment'))
            if comment == 'None':
                abort(400)
            tone = watson_tone(comment)
            comment = Comment(comment=comment,tone=tone)
            comment.save()
            response = jsonify(comment.serialize())
            response.status_code = 201
        else:
            comments = Comment.query.all()
            results = [comment.serialize() for comment in comments]
            response = jsonify(results)
            response.status_code = 200
        return response


    @app.route('/comments/<int:sku>', methods=['GET', 'PUT', 'DELETE'])
    def comment(sku):
        comment = Comment.query.get(sku)
        if not comment:
            abort(404)

        if request.method == 'GET':
            response = jsonify(comment.serialize())
            response.status_code = 200

        elif request.method == 'PUT':
            new_comment = str(request.form.get('comment'))
            if not new_comment:
                response.status_code = 400
                return response
            tone = watson_tone(new_comment)
            comment.comment = new_comment
            comment.tone = tone
            comment.save()
            response = jsonify(comment.serialize())
            response.status_code = 200

        elif request.method == 'DELETE':
            comment.delete()
            response = jsonify({'message': f'Comment {sku} has been deleted'})
            response.status_code = 200
        return response

    return app

