## Description

Put together some example beaconv2 instances by whatever means possible. We
chose 5 donors of cutaneous subtype from the Hayward et al Nature paper
https://doi.org/10.1038/nature22071 . The code is not runnable anywhere but
QIMR Berghofer as it has dependencies on our internal Stardog database
(`grafli`) and python libraries (`graflipy`) but the generated outputs are
completely generic, valid, beacon v2 data.

## Notes 

Most of the hard yakka is in crafting the mapping from our internal data model
to the beacon v2 data models. This is accomplished by a combination of db
CONSTRUCT queries and post-processing. The `catalogue.json` and other mapping
resources have been generated as templates and the details filled by hand.

## Validation

The `RefResolver` needs to be constructed with the URI of the schema doc as well
as the schema itself so that relative references will be resolved.

## Generated data

To generate validated analyses, biosamples, individuals and runs in `outputs/`:

    python torcedor.py

## Hand-rolled data

### genomicVariations

These were manually created and validated against https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/defaultSchema.json

We describe BRAF V600E (2 case instances) and BRAF V600K (2 case instances)

### datasets

This was manually created and validated against https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/datasets/defaultSchema.json

### cohorts

This was manually created and validated against https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/cohorts/defaultSchema.json

