from webargs.flaskparser import FlaskParser


class Parser(FlaskParser):
    DEFAULT_VALIDATION_STATUS = 400


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
