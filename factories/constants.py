# Wikidata SPARQL query
SPARQL_BASE_URL = 'https://query.wikidata.org/sparql'


SPARQL_WIKIDATA_QUERY = """
SELECT ?item ?itemLabel
WHERE
{{
{filters}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language}" }}
}}
"""

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/50.0.2661.102 Safari/537.36"

