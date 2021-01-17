import json

from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())


# Keep secret keys in secrets.json
def get_secret(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)