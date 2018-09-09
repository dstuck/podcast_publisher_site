import os
import requests

from pod_config import get_conf

CONF = get_conf()


class PodbeanError(Exception):
    pass


def authorize_upload_to_podbean(local_file, oauth_token):
    upload_url = 'https://api.podbean.com/public/v1/files/uploadAuthorize'
    filesize = os.stat(local_file).st_size
    upload_data = {
        'access_token': oauth_token,
        'filename': os.path.basename(local_file),
        'content_type': 'audio/mp3',
        'filesize': filesize
    }
    print upload_data
    r_podbean = requests.get(
        upload_url, params=upload_data
    )
    upload_response = r_podbean.json()
    print upload_response
    if 'error' in upload_response:
        raise PodbeanError(upload_response["error_description"])
    return upload_response


def upload_mp3_to_podbean(local_file, presigned_url):
    with open(local_file, 'rb') as f:
        r_import_pb = requests.put(
            url=presigned_url,
            headers={'Content-Type': 'audio/mp3'},
            files={os.path.basename(local_file).encode('utf8'): f},
        )
        if 'error' in r_import_pb.content:
            raise PodbeanError(r_import_pb.content)
    return r_import_pb


def publish_to_podbean(sermon, media_key, oauth_token):
    publish_api_url = 'https://api.podbean.com/public/v2/episodes'
    status = CONF['podbean']['publish_mode']
    podcast_data = {
        'access_token': oauth_token,
        'title': sermon.pretty_title(),
        'content': sermon.description,
        'status': status,
        'type': 'public',
        'media_key': media_key,
    }
    publish_response = requests.post(
        publish_api_url, data=podcast_data
    ).json()
    if 'error' in publish_response:
        raise PodbeanError(publish_response['error_description'])
    else:
        return publish_response
