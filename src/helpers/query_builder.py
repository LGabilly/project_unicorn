from elasticsearch_dsl.query import Bool, MatchAll


def all_rules_query() -> Bool:
    boolean_query = Bool(must=MatchAll())
    return boolean_query
