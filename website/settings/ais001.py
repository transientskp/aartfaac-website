from website.settings import *

# Setup support for proxy headers, required since we are behind lofar proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PREFIX = '/aartfaac'

FORCE_SCRIPT_NAME = PREFIX
STATIC_URL = PREFIX + '/static/'
MEDIA_URL = PREFIX + '/media/'
LOGIN_URL = PREFIX + '/accounts/login/'
LOGIN_REDIRECT_URL = PREFIX + '/'

ALLOWED_HOSTS = ['proxy.lofar.eu', 'aartfaac.org', 'www.aartfaac.org']
