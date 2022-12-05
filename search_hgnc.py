from http_get import (
    http_get,
)  # uses https://gist.github.com/dmyersturnbull/fade1a5901beeb1003680f8267454640
from typing import Mapping, Union, Iterable
import json

searchable_fields = {
    "alias_name",
    "alias_symbol",
    "ccds_id",
    "ena",
    "ensemble_gene_id",
    "entrez_id",
    "hgnc_id",
    "locus_group",
    "locus_type",
    "mgd_id",
    "name",
    "prev_name",
    "prev_symbol",
    "refseq_accession",
    "rgd_id",
    "status",
    "symbol",
    "ucsc_id",
    "uniprot_ids",
    "vega_id",
}


def search_hgnc(fields: Union[Mapping[str, str], str]) -> Iterable[str]:
    """Searches HGNC and returns a list of HGNC symbol IDs.
    fields is either:
        A) A map of field names (contained in searchable_fields) to their values
        B) A string for the name field; i.e. search_hgnc('abc') === search_hgnc({'name': 'abc'})
    """
    if isinstance(fields, str):
        fields = {"name": fields}
    for key in fields.keys():
        if key not in searchable_fields:
            raise ValueError("'{}' is not a searchable field".format(key))
    query = "http://rest.genenames.org/search/" + "+AND+".join(
        [key + ":" + value for key, value in fields.items()]
    )
    text = http_get(query, {"Accept": "application/json"})
    results = json.loads(text)
    return [x["symbol"] for x in results["response"]["docs"]]
