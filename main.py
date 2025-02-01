from flask import (
    Flask,
    request,
    abort
)
from src.service import AntiplagService
from marshmallow import ValidationError
from src.entities import (
    CheckInput,
    CheckResult
)
from src.schema import (
    BadRequestSchema,
    CheckSchema
)


def create_app():


    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_request_handler(ex: ValidationError):
        return BadRequestSchema().dump(ex), 400

    @app.route('/check/', methods=['get', 'post'])
    def check() -> CheckResult: 

        schema = CheckSchema()
        service = AntiplagService()


        try:    
            request_data: CheckInput = request.json
            
            data = service.check(
                    data=schema.load(request_data)
                )
        except ValidationError as ex:
            abort(400, ex)
    
        else:
            return schema.dump(data)
    return app

app = create_app()