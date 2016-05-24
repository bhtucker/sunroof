# -*- coding: utf-8 -*-
"""
    sunroof.ingest_bills
    ~~~~~~~~~~

    Ingest data from Sunlight Fdtn Congress API
"""

import argparse
import requests
import urlparse
import math
from sqlalchemy import MetaData, engine
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse as dateparse

from sunroof.models import bills, legislators
from sunroof.secrets import API_KEY


SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/congress'
HOST = 'https://congress.api.sunlightfoundation.com'
BILLS_URL = urlparse.urljoin(HOST, 'bills')
LEGISLATORS_URL = urlparse.urljoin(HOST, 'legislators')


def _initialize_model(metadata, model):
    model.metadata = metadata
    if not model.exists():
        model.create()
    return model


def _validate_args(args, help_string):
    assert isinstance(args.query, (str, unicode)), "Invalid query. See usage:\n" + help_string
    end_dt = dateparse(args.end)
    assert args.end in end_dt.isoformat(),  "Invalid end date. See usage:\n" + help_string


def _generate_sunlight_results(url, **kwargs):
    """
    Centralize pagination and request logic.
    Returns a generator of result documents
    """
    params = dict(apikey=API_KEY, per_page=100)
    params.update(kwargs)
    r = requests.get(url, params=params)
    initial_body = r.json()
    
    pages = math.ceil(initial_body['count'] / 100.)
    responses = [initial_body]
    if pages > 1:
        for page in range(1, int(pages)):
            params.update(page=page)
            r = requests.get(url, params=params)
            responses.append(r.json())
    for response in responses:
        for result in response['results']:
            yield result


def ingest_document(result, model, session):
    """
    Models have some fields pulled out redundantly for query ease,
    as well as a `document` field for the full result.
    """
    top_level_fields = [x.name for x in model.columns if x.name != 'document']
    record = {field: result[field] for field in top_level_fields}
    record['document'] = result
    session.execute(model.insert(values=record))


def main():
    parser = argparse.ArgumentParser(
        description='Download some U.S. Congress data')
    parser.add_argument('--query', dest='query',
                        help='Bill contents to query')
    parser.add_argument('--end-date', dest='end',
                        help='Lower bound filter on `last_action_at` field')
    args = parser.parse_args()
    _validate_args(args, parser.format_help())

    congress_engine = engine.create_engine(SQLALCHEMY_DATABASE_URI)
    metadata = MetaData(bind=congress_engine)
    congress_models = {bills, legislators}
    for model in congress_models:
        _initialize_model(metadata, model)
    session = sessionmaker(bind=congress_engine)()

    bill_results = _generate_sunlight_results(
        BILLS_URL, query=args.query, last_action_at__gte=args.end,
        order='last_action_at')

    for bill in bill_results:
        ingest_document(bill, bills, session)
    session.commit()

    # get distinct sponsor_ids to collect more info
    sponsor_ids = [
        x[0] for x in session.query(bills.c.sponsor_id.distinct()).all()
    ]

    for sponsor_id in sponsor_ids:
        for legislator_result in _generate_sunlight_results(
                LEGISLATORS_URL, bioguide_id=sponsor_id):
            ingest_document(legislator_result, legislators, session)
    session.commit()
    print 'Ingested relevant bill and sponsor information'

if __name__ == '__main__':
    main()
