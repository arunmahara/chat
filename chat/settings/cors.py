from .base import *

# cors headers
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS

CORS_ALLOW_HEADERS = [
    "x-total-count",
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "content-length",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-origin",
]

CORS_EXPOSE_HEADERS = [
    "x-total-count",
    "content-length",
]
