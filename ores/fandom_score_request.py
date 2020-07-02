import json
from .score_request import ScoreRequest

class FandomScoreRequest(ScoreRequest):
    def __init__(self, *args, wiki=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.wiki = wiki

    def __str__(self):
        return self.format()

    def format(self, rev_id=None, model_name=None):
        """
        Fomat a request or a sub-part of a request based on a rev_id and/or
        model_name.  This is useful for logging.
        """
        rev_ids = rev_id if rev_id is not None else set(self.rev_ids)
        model_names = model_name if model_name is not None else set(self.model_names)
        common = [self.context_name, rev_ids, model_names]

        optional = []
        if self.precache:
            optional.append("precache")
        if self.include_features:
            optional.append("features")
        if self.injection_caches:
            optional.append("injection_caches={0}".format(self.injection_caches))
        if self.model_info:
            optional.append("model_info=" + json.dumps(self.model_info))
        if self.ip:
            optional.append("ip={0}".format(self.ip))
        if self.wiki:
            optional.append("wiki={0}".format(self.wiki))

        return "{0}({1})".format(":".join(repr(v) for v in common),
                                 ", ".join(optional))

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(v) for v in [
                self.context_name,
                self.rev_ids,
                self.model_names,
                "precache={0!r}".format(self.precache),
                "include_features={0!r}".format(self.include_features),
                "injection_caches={0!r}".format(self.injection_caches),
                "ip={0!r}".format(self.ip),
                "model_info={0!r}".format(self.model_info),
                "wiki={0!r}".format(self.wiki)]))

    def to_json(self):
        return {
            'context': self.context_name,
            'rev_ids': list(self.rev_ids),
            'model_names': list(self.model_names),
            'precache': self.precache,
            'include_features': self.include_features,
            'injection_caches': self.injection_caches,
            'ip': self.ip,
            'model_info': self.model_info,
            'wiki': self.wiki
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data['context'],
            set(data['rev_ids']),
            set(data['model_names']),
            precache=data['precache'],
            include_features=data['include_features'],
            injection_caches=data['injection_caches'],
            model_info=data['model_info'],
            ip=data['ip'],
            wiki=data['wiki'])
