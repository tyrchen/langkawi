from django.contrib.auth.models import User
from langkawi.contrib.facebook.auth import FacebookAuth
from langkawi.contrib.linkedin.auth import LinkedInAuth
from langkawi.contrib.openid.auth import OpenIDAuth
from langkawi.contrib.twitter.auth import TwitterAuth

import warnings

warnings.warn("`langkawi.auth.*` will be removed. "
    "Use `langkawi.contrib.*.auth.*` instead.")
