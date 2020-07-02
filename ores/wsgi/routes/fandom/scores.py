from flask import request

from . import util
from ... import preprocessors, responses
from ...fandomutil import build_fandom_score_request

def configure(config, bp, scoring_system):

    # /fandom/scores/
    @bp.route("/fandom/scores/", methods=["GET"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def scores_fandom():
        try:
            score_request = build_fandom_score_request(scoring_system, request)
        except Exception as e:
            return responses.bad_request(str(e))

        return util.build_fandom_context_model_map(score_request, scoring_system)

    # /fandom/scores/enwiki/?models=reverted&revids=456789|4567890
    @bp.route("/fandom/scores/<context>/", methods=["GET", "POST"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def score_model_revisions_fandom(context):
        try:
            score_request = build_fandom_score_request(
                scoring_system, request, context)
        except Exception as e:
            return responses.bad_request(str(e))

        return util.process_score_request(score_request, scoring_system)

    # /fandom/scores/enwiki/reverted/?revids=456789|4567890
    @bp.route("/fandom/scores/<context>/<int:revid>/", methods=["GET", "POST"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def score_revisions_fandom(context, revid):
        try:
            score_request = build_fandom_score_request(
                scoring_system, request, context, rev_id=revid)
        except Exception as e:
            return responses.bad_request(str(e))

        return util.process_score_request(score_request, scoring_system)

    # /fandom/scores/enwiki/reverted/4567890
    @bp.route("/fandom/scores/<context>/<int:rev_id>/<model>/", methods=["GET", "POST"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def score_revision_fandom(context, model, rev_id):
        try:
            score_request = build_fandom_score_request(
                scoring_system, request, context, rev_id=rev_id,
                model_name=model)
        except Exception as e:
            return responses.bad_request(str(e))

        return util.process_score_request(score_request, scoring_system)

    return bp
