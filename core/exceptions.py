class WDQuizError(Exception):
    def __init__(self):
        msg = getattr(self.__class__, 'msg', 'Unknown Error')
        code = getattr(self.__class__, 'code', 500)
        super().__init__(code, msg)


class WikidataSparQLError(WDQuizError):
    msg = 'Unexpected error while request to Wikidata'


class WikidataResultError(WDQuizError):
    msg = 'Unexpected result from Wikidata'


class BackendDoesNotExist(WDQuizError):
    msg = 'Backend does not exist'


class FileTypeError(WDQuizError):
    msg = 'File type not allowed'


class NotFoundError(WDQuizError):
    msg = 'File type not allowed'
    code = 404
