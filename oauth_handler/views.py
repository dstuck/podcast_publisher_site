from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

import oauth_utils
from .models import OAuthKey


def oauth_receiver(request):
    oauth_code = request.GET.get('code')
    token_dict = oauth_utils.get_token_from_code(oauth_code)
    if 'error' in token_dict:
        messages.add_message(
            request, messages.INFO,
            'OAuth Failed with error: {}'.format(
                token_dict.get('error_description')
            )
        )
        return HttpResponseRedirect('/sermons/')
    key = OAuthKey.create(**token_dict)
    key.save()
    messages.add_message(
        request, messages.INFO,
        'Added oauth_key'
    )
    return HttpResponseRedirect('/sermons/')


def oauth_db(request):
    if False:
        test = OAuthKey.create(
            access_token='testing',
            expires_in='60',
            refresh_token='dont know',
            scope='stuff',
            token_type='type',
        )
        test.save()
    oauthkeys = OAuthKey.objects.all()
    return render(request, 'oauth_db.html', {'oauthkeys': oauthkeys})
