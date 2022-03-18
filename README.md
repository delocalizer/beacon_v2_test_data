# Description

Put together some example beaconv2 instances by whatever means possible. We
chose 5 donors of cutaneous subtype from the MELA 183 Nature paper. The code
is not runnable anywhere but QIMR Berghofer as it has dependencies on our
internal Stardog database (`grafli`) and python libraries (`graflipy`) but the
generated outputs are completely generic, valid, beacon v2 data.

# Notes 

Most of the hard yakka is in crafting the mapping from our internal data model
to the beacon v2 data models. This is accomplished by a combination of db
CONSTRUCT queries and post-processing. The `catalogue.json` and other mapping
resources have been generated as templates and the details filled by hand.

# Validation

The `RefResolver` needs to be constructed with the URI of the schema doc as well
as the schema itself so that relative references will be resolved.

# genomicVariations

These were entirely handrolled and validated against https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/defaultSchema.json

We describe BRAF V600E (2 case instances) and BRAF V600K (2 case instances)

# other models:

To generate the validated instances in `outputs/`:

    python torcedor.py
