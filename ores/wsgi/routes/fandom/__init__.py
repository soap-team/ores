from flask import request
from flask_swaggerui import render_swaggerui

from . import precache, scores, spec


def configure(config, bp, score_processor):

    @bp.route("/fandom/", methods=["GET"])
    def fandom_index():
        if "spec" in request.args:
            return spec.generate_spec(config)
        else:
            return render_swaggerui(swagger_spec_path="/fandom/spec/")

    bp = precache.configure(config, bp, score_processor)
    bp = scores.configure(config, bp, score_processor)
    bp = spec.configure(config, bp, score_processor)

    return bp
