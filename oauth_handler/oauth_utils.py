import datetime as dt
import requests
import json
from pod_config import get_conf
from django.contrib import messages
# from django.shortcuts import redirect

from .models import OAuthKey

CONF = get_conf()


class OAuthError(Exception):
    pass


def get_oauth_request_url():
    return 'https://api.podbean.com/v1/dialog/oauth?'\
        'redirect_uri={}'\
        '&scope=podcast_read+podcast_update+episode_publish+episode_read'\
        '&response_type=code&client_id={}'.format(
            CONF['podbean']['redirect_uri'], CONF['podbean']['client_id']
        )


def get_token_from_code(code):
    oauth_request_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CONF['podbean']['redirect_uri'],
    }
    token_request = requests.post(
        'https://api.podbean.com/v1/oauth/token',
        data=oauth_request_data,
        auth=(CONF['podbean']['client_id'], CONF['podbean']['client_secret'])
    )
    token_dict = json.loads(token_request.content)
    return token_dict


def refresh_oauth_token(refresh_token):
    oauth_request_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    refresh_request = requests.post(
        'https://api.podbean.com/v1/oauth/token',
        data=oauth_request_data,
        auth=(CONF['podbean']['client_id'], CONF['podbean']['client_secret'])
    )
    refresh_dict = json.loads(refresh_request.content)
    refresh_dict['refresh_token'] = refresh_token
    return refresh_dict


def get_active_oauth_token(request=None):
    if len(OAuthKey.objects.all()) == 0:
        raise OAuthError('Need to add oauth_tokens')
    oauth_keys = OAuthKey.objects.filter(
        expires_at__gte=dt.datetime.utcnow()
    ).order_by('-created_at')
    if len(oauth_keys) == 0:
        if request is not None:
            messages.add_message(
                request, messages.INFO,
                'No non-expired oauth tokens. Refreshing tokens'
            )
        recent_oauth_key = OAuthKey.objects.order_by('-created_at')[0]
        new_key_dict = refresh_oauth_token(recent_oauth_key.refresh_token)
        if 'error' in new_key_dict:
            raise OAuthError(new_key_dict.get('error_description'))
        key = OAuthKey.create(**new_key_dict)
        key.save()
        return key.access_token
    return oauth_keys[0].access_token
