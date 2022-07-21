"""Beacon Configuration."""

#
# Beacon general info
#
beacon_id = 'qimrberghofer.edu.au-beacon-test'  # ID of the Beacon
beacon_name = 'QIMR Berghofer Beacon Test'  # Name of the Beacon service
api_version = 'v2.0.0'  # Version of the Beacon implementation
uri = 'https://beacon-giab-test.ega-archive.org'

#
# Beacon granularity
#
default_beacon_granularity = "record"
max_beacon_granularity = "record"

#
#  Organization info
#
org_id = 'QIMR_Berghofer'  # Id of the organization
org_name = 'QIMR Berghofer Medical Research Institute'  # Full name
org_description = ('From humble beginnings in 1945, the Queensland Institute '
                   'Medical Research, now known as QIMR Berghofer, is one of '
                   'Australia’s most successful medical research institutes, '
                   'translating discoveries from bench to bedside for a better '
                   'future of health. ')
org_adress = ('co/ Conrad Leonard, PhD, GradDipDataSci '
              'Senior Bioinformatician '
              'Genome Informatics Group '
              'QIMR Berghofer Medical Research Institute '
              '300 Herston Rd, Brisbane QLD 4006 Australia')
org_welcome_url = 'https://www.qimrberghofer.edu.au/about-us/'
org_contact_url = 'mailto:conrad.leonard@qimrberghofer.edu.au'
org_logo_url = 'https://www.qimrberghofer.edu.au/wp-content/themes/qimf-berghofer/images/logo-stacked.svg'
org_info = ('OUR PURPOSE '
            'Better health through impactful medical research. '
            'OUR VISION '
            'Lead the way to significant innovation in health – nationally '
            'and globally')

#
# Project info
#
description = ("Demonstrating data discovery via beacon")
version = 'v2.0'
welcome_url = 'https://qimrberghofer.edu.au/beacon-placeholder/api'
alternative_url = ''
create_datetime = '2021-11-29T12:00:00.000000'
update_datetime = ''
# update_datetime will be created when initializing the beacon, using the ISO 8601 format

#
# Service
#
service_type = 'org.ga4gh:beacon:1.0.0'  # service type
service_url = 'https://qimrberghofer.edu.au/beacon-placeholder/api'
entry_point = False
is_open = True
documentation_url = 'https://github.com/EGA-archive/beacon-2.x/'  # Documentation of the service
environment = 'test'  # Environment (production, development or testing/staging deployments)

# GA4GH
ga4gh_service_type_group = 'org.ga4gh'
ga4gh_service_type_artifact = 'beacon'
ga4gh_service_type_version = '1.0'

# Beacon handovers
beacon_handovers = [
    {
        'handoverType': {
            'id': 'CUSTOM',
            'label': 'Project description'
        },
        'note': 'Project description',
        'url': 'https://www.nist.gov/programs-projects/genome-bottle'
    }
]

#
# Database connection
#
database_host = '127.0.0.1'
database_port = 27017
database_user = 'root'
database_password = 'not-actually-the-password'
database_name = 'beacon'
database_auth_source = 'admin'
# database_schema = 'public' # comma-separated list of schemas
# database_app_name = 'beacon-appname' # Useful to track connections

#
# Web server configuration
# Note: a Unix Socket path is used when behind a server, not host:port
#
beacon_host = '0.0.0.0'
beacon_port = 5050
beacon_tls_enabled = False
beacon_tls_client = False
beacon_cert = '/etc/ega/server.cert'
beacon_key = '/etc/ega/server.key'
CA_cert = '/etc/ega/CA.cert'

#
# Permissions server configuration
#
permissions_url = 'http://beacon-permissions'

#
# IdP endpoints (OpenID Connect/Oauth2)
#
# or use Elixir AAI (see https://elixir-europe.org/services/compute/aai)
#
idp_client_id = 'beacon'
idp_client_secret = 'not-actually-the-secret'  # same as in the test IdP
idp_scope = 'profile openid'

idp_authorize = 'http://idp/auth/realms/Beacon/protocol/openid-connect/auth'
idp_access_token = 'http://idp/auth/realms/Beacon/protocol/openid-connect/token'
idp_introspection = 'http://idp/auth/realms/Beacon/protocol/openid-connect/token/introspect'
idp_user_info = 'http://idp/auth/realms/Beacon/protocol/openid-connect/userinfo'
idp_logout = 'http://idp/auth/realms/Beacon/protocol/openid-connect/logout'

idp_redirect_uri = 'http://beacon:5050/login'

#
# UI
#
autocomplete_limit = 16
autocomplete_ellipsis = '...'

#
# Ontologies
#
ontologies_folder = "ontologies"
