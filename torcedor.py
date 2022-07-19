"""
Hand-roll some beacon data model instances
"""
import json
import logging
import os
from collections import defaultdict
from urllib.request import urlopen

from jsonschema import validate, RefResolver
from rdflib.term import URIRef

from graflipy import configure, to_iri, serialize_term
from graflipy.connect import do_query

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)
SCHEMA_BASEURI = ('https://raw.githubusercontent.com/ga4gh-beacon/'
                  'beacon-v2-Models/main/BEACON-V2-Model')
SCHEMA_NAMES = ['individuals', 'biosamples', 'runs', 'analyses',
                'genomicVariations', 'cohorts', 'datasets']
WARN_NO_MAPPING = '%s "%s" has no mapping'

# associate each schema document with its resolver
SCHEMA = {}
for name in SCHEMA_NAMES:
    location = f'{SCHEMA_BASEURI}/{name}/defaultSchema.json'
    with urlopen(location) as uh:
        schema = json.load(uh)
    SCHEMA[name] = (schema, RefResolver(location, schema))

# TODO combine custom property value_maps/ files into term_map:
# will involve keying on predicate as well as object in the
# catalogue and the map

with open('value_maps/donorRegionOfResidence.json') as fh:
    RESIDENCE_REGION = json.load(fh)

with open('value_maps/donorDiagnosisIcd10.json') as fh:
    DISEASE_DIAGNOSIS = json.load(fh)

with open('value_maps/tumourHistologicalType.json') as fh:
    HISTOLOGY = json.load(fh)


def individuals(termmap):
    """
    Map Donors in grafli to beacon individuals

    Returns:
        list of validated beacon individuals
    """
    with open('query/mela_5_donors.sparql', 'rt') as fh:
        query = fh.read()
    graph = do_query(query).graph
    indivs = []
    schema, resolver = SCHEMA['individuals']
    _toggle_https_proxy()

    for donor in set(graph.subjects()):
        indiv = {'$schema': 'individuals/defaultSchema.json'}
        p_o = defaultdict(list)
        for p, o in graph.predicate_objects(donor):
            p_o[p].append(o)

        indiv['id'] = _value(p_o, ':uuid')
        indiv['sex'] = _value(p_o, ':donorSex', mapping=termmap)
        indiv['geographicOrigin'] = _value(p_o, ':donorRegionOfResidence',
                                           mapping=RESIDENCE_REGION)
        diseaseCode = _value(p_o, ':donorDiagnosisIcd10',
                             mapping=DISEASE_DIAGNOSIS)
        ageOfOnset = {
            'age': {'iso8601duration':
                    f'P{int(_value(p_o, ":donorAgeAtDiagnosis"))}Y'}}
        disease = {'diseaseCode': diseaseCode, 'ageOfOnset': ageOfOnset}
        familyHistory = _value(p_o, ':cancerHistoryFirstDegreeRelative',
                               mapping=termmap)
        if familyHistory:
            disease['familyHistory'] = familyHistory
        indiv['diseases'] = [disease]

        LOGGER.info(f'validating individual {indiv["id"]}')
        validate(indiv, schema=schema, resolver=resolver)
        indivs.append(indiv)

    _toggle_https_proxy()
    return indivs


def biosamples(termmap):
    """
    Map CollectedSamples in grafli to beacon biosamples

    Returns:
        list of validated beacon biosamples
    """
    with open('query/mela_5_samples.sparql', 'rt') as fh:
        query = fh.read()
    graph = do_query(query).graph
    smpls = []
    schema, resolver = SCHEMA['biosamples']
    _toggle_https_proxy()

    for collectedsample in set(graph.subjects()):
        smpl = {'$schema': 'biosamples/defaultSchema.json'}
        p_o = defaultdict(list)
        for p, o in graph.predicate_objects(collectedsample):
            p_o[p].append(o)

        smpl['id'] = _value(p_o, ':uuid')
        smpl['individualId'] = _value(p_o, ':individualId', fragment=True)
        smpl['biosampleStatus'] = _value(p_o, ':specimenType',
                                         mapping=termmap)
        sampleOriginType = {'id': 'OBI:0001479',
                            'label': 'specimen from organism'}
        if 'xenograft' in smpl['biosampleStatus']['label'].lower():
            sampleOriginType = {'id': 'OBI:0100058',
                                'label': 'xenograft'}
        if 'cell line' in smpl['biosampleStatus']['label'].lower():
            sampleOriginType = {'id': 'OBI:0001876',
                                'label': 'cell culture'}
        smpl['sampleOriginType'] = sampleOriginType

        if smpl['biosampleStatus']['label'] != 'reference sample':
            smpl['histologicalDiagnosis'] = _value(
                    p_o, ':tumourHistologicalType', mapping=HISTOLOGY)
        extras = [':hasSampleTissue', ':hasSampleType', ':hasSampleMaterial']
        smpl['notes'] = '|'.join(_value(p_o, p, fragment=True)
                                 for p in extras)

        LOGGER.info(f'validating biosample {smpl["id"]}')
        validate(smpl, schema=schema, resolver=resolver)
        smpls.append(smpl)

    _toggle_https_proxy()
    return smpls


def runs(termmap):
    """
    Map AlignedReadGroupSets in grafli to beacon runs

    Returns:
        list of validated beacon runs
    """
    with open('query/mela_5_runs.sparql', 'rt') as fh:
        query = fh.read()
    graph = do_query(query).graph
    runs = []
    schema, resolver = SCHEMA['runs']
    _toggle_https_proxy()

    for args in set(graph.subjects()):
        run = {'$schema': 'runs/defaultSchema.json'}
        p_o = defaultdict(list)
        for p, o in graph.predicate_objects(args):
            p_o[p].append(o)

        run['id'] = _value(p_o, ':uuid')
        run['individualId'] = _value(p_o, ':individualId', fragment=True)
        run['biosampleId'] = _value(p_o, ':biosampleId', fragment=True)
        run['runDate'] = _value(p_o, ':runDate')
        run['platformModel'] = _value(p_o, ':platformModel', mapping=termmap)
        run['libraryStrategy'] = _value(p_o, ':libraryStrategy')
        run['libraryLayout'] = 'PAIRED'
        run['librarySelection'] = 'RANDOM'
        # TODO properly infer rather than hard-code:
        # * platform (subset of platformModel)
        # * libraryLayout ('PAIRED' if DNA)
        # * librarySelection ('RANDOM' if WGS)

        LOGGER.info(f'validating run {run["id"]}')
        validate(run, schema=schema, resolver=resolver)
        runs.append(run)

    _toggle_https_proxy()
    return runs


def analyses(termmap):
    """
    Map Analyses in grafli to beacon analyses

    Returns:
        list of validated beacon analyses
    """
    with open('query/mela_5_analyses.sparql', 'rt') as fh:
        query = fh.read()
    graph = do_query(query).graph
    analyses = []
    schema, resolver = SCHEMA['analyses']
    _toggle_https_proxy()

    for args in set(graph.subjects()):
        analysis = {'$schema': 'analyses/defaultSchema.json'}
        p_o = defaultdict(list)
        for p, o in graph.predicate_objects(args):
            p_o[p].append(o)

        analysis['id'] = _value(p_o, ':uuid')
        analysis['individualId'] = _value(p_o, ':individualId', fragment=True)
        analysis['biosampleId'] = _value(p_o, ':biosampleId', fragment=True)
        analysis['runId'] = _value(p_o, ':runId', fragment=True)
        analysis['analysisDate'] = _value(p_o, ':analysisDate')
        analysis['aligner'] = _value(p_o, ':aligner')
        analysis['pipelineName'] = _value(p_o, ':pipelineName')

        LOGGER.info(f'validating analysis {analysis["id"]}')
        validate(analysis, schema=schema, resolver=resolver)
        analyses.append(analysis)

    _toggle_https_proxy()
    return analyses


def term_map(map_file):
    """
    Returns:
        Parse a catalogue mapping file and return a dict from grafli terms to
        beacon terms { iri: str }
    """
    map_ = {}
    raw = json.load(map_file)
    for _, terms in raw.items():
        for term in terms:
            key = URIRef(term['iri'])
            label = term['label']
            val = term['maps_to']
            if val is None:
                LOGGER.warning(WARN_NO_MAPPING, serialize_term(key), label)
                pass
            map_[key] = val
    return map_


def _toggle_https_proxy():
    """
    graflipy.connect.get_sparqlstore requires HTTPS environment vars to be
    unset for long queries to work but jsonschema requires them to be set for
    the validator resolver to work. This sets/unsets the vars as required. When
    setting vars the value from HTTP_PROXY or http_proxy is used.
    """
    for httpsproxyvar in ('https_proxy', 'HTTPS_PROXY'):
        if os.environ.get(httpsproxyvar):
            del os.environ[httpsproxyvar]
        else:
            httpproxyvar = httpsproxyvar.replace('s','').replace('S','')
            if os.environ.get(httpproxyvar):
                os.environ[httpsproxyvar] = os.environ[httpproxyvar]


def _value(p_o, p, mapping=None, fragment=False):
    """
    Returns the processed value of the predicate 'p' specified as a string.

    Args:
        p_o: a dict like {'predicate': [list of object values]}
        p: short-form string representation of the predicate e.g. 'rdfs:label'
        mapping: if supplied, use this to map the o value to the final value
        fragment: use the fragment part of the o value as the final value
    Returns:
        item: the updated item
    """
    k = to_iri(p)
    v = p_o.get(k, [])
    assert len(v) == 1, f'Multiple values of {k} in p_o: {v}'
    value = v[0]
    if mapping:
        try:
            value = mapping[value]
        except KeyError:
            value = mapping[str(value)]
    elif fragment:
        value = value.split('#')[1]
    return value


if __name__ == '__main__':

    configure('PRODUCTION', 'READONLY')

    with open('value_maps/catalogue.json') as fh:
        termmap = term_map(fh)

    instances_outfile = (
        (individuals(termmap), 'output/individuals.json'),
        (biosamples(termmap), 'output/biosamples.json'),
        (runs(termmap), 'output/runs.json'),
        (analyses(termmap), 'output/analyses.json'),
    )
    for instances, outfile in instances_outfile:
        with open(outfile, 'wt') as fh:
            for instance in sorted(instances, key=lambda x: x["id"]):
                schema = instance["$schema"].split("/")[0]
                LOGGER.info(f'writing {schema} instance {instance["id"]}')
                fh.write(json.dumps(instance, indent=2, sort_keys=True))
