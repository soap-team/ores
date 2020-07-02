import json
import logging

from flask_jsonpify import jsonify as flask_jsonify

from ..fandom_score_request import FandomScoreRequest
from .util import parse_model_names, parse_injection, parse_model_info, read_bar_split_param, parse_rev_ids

logger = logging.getLogger(__name__)

def build_fandom_score_request(scoring_system, request, context_name=None, rev_id=None,
                        model_name=None):
    """
    Build an :class:`ores.score_request.ScoreRequest` from information contained in a
    request.

    :Parameters:
        scoring_system : :class:`ores.scoring_systems.ScoringSystem`
            A scoring system to build request with
        request : :class:`flask.Request`
            A web request to extract information from
        context_name : `str`
            The name of the context to perform scoring. For Fandom, this is always 
            'fandom' and the context_name is the wiki URL instead, e.g. community.fandom.com.
        rev_id : `str`
            The revision ID to score.  Note that multiple IDs can be provided
            in `request.args`
        model_name = `str`
            The name of the model to score.  Note that multiple models can be
            provided in `request.args`
    """
    rev_ids = parse_rev_ids(request, rev_id)
    model_names = parse_model_names(request, model_name)
    precache = 'precache' in request.args
    include_features = 'features' in request.args
    injection_caches = parse_injection(request, rev_ids)
    model_info = parse_model_info(request)

    if context_name and not model_names:
        model_names = scoring_system['fandom'].keys()

    # WMF specific solution
    if request.headers.get('X-Client-IP') is None:
        ip = request.remote_addr.strip()
    else:
        ip = request.headers['X-Client-IP'].strip()

    return FandomScoreRequest('fandom', rev_ids, model_names,
                              precache=precache,
                              include_features=include_features,
                              injection_caches=injection_caches,
                              model_info=model_info,
                              ip=ip,
                              wiki=context_name)
