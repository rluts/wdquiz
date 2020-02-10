class GQuizError(Exception):
    def __init__(self):
        msg = getattr(self.__class__, 'msg', 'Unknown Error')
        code = getattr(self.__class__, 'code', '500_INTERNAL_ERROR')
        super().__init__(code, msg)


class WikidataSparQLError(GQuizError):
    msg = 'Unexpected error while request to Wikidata'


class WikidataResultError(GQuizError):
    msg = 'Unexpected result from Wikidata'
