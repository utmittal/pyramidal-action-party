"""
Test functions to make sure things are working correctly
"""
import re

def validate_kwargs(**kwargs):
    """Run assert checks on option arguments for search_tweets()"""
    # If count specified, extract that, otherwise default to 15
    if 'count' in kwargs:
        assert 1 <= kwargs['count'] <= 100, 'Count must be in range [1, 100]'

    # If exact search specified, enclose in quotation marks (multi-word queries)
    if 'exact' in kwargs:
        assert isinstance(kwargs['exact'], bool), "exact argument must be a boolean"

    # result_type should be one of three options
    if 'result_type' in kwargs:
        assert kwargs['result_type'] in ['recent', 'popular', 'mixed'], "Invalid result_type"

    # Must be formatted as date YYYY-MM-DD
    if 'until' in kwargs:
        assert re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', kwargs['until'])
