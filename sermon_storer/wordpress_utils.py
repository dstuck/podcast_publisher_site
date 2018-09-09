from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from pod_config import get_conf

CONF = get_conf()


def publish_to_wordpress(ep_id, sermon_title, sermon_description,
                         wp_client=None):
    if wp_client is None:
        wordpress_params = {
            'url': CONF['wordpress']['url'],
            'username': CONF['wordpress']['user'],
            'password': CONF['wordpress']['password'],
        }
        wp_client = Client(**wordpress_params)
    ep_id = ep_id.lower()
    ep_emb_id = '-'.join([ep_id[0:5], ep_id[5:]])
    pb_url = 'https://www.podbean.com/media/player/{}?from=yiiadmin'.format(
        ep_emb_id
    )
    full_content = '''<h2>{0}</h2>
    <iframe src="{1}" width="100%" height="100" frameborder="0" scrolling="no" data-link="{1}" data-name="pb-iframe-player"></iframe>
    {2}'''.format(
        sermon_title.encode('utf8'), pb_url, sermon_description
    )
    post = WordPressPost()
    # post and activate new post
    post = WordPressPost()
    post.title = sermon_title
    post.content = full_content
    post.post_status = CONF['wordpress']['publish_mode']
    post.terms_names = {
        'category': ['Podcast']
    }
    return wp_client.call(NewPost(post)), sermon_title
