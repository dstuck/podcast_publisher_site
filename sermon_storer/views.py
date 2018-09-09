import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import FTPPasswordForm
from .models import Sermon
import ftp_utils
from oauth_handler import oauth_utils
from podbean_utils import (
    authorize_upload_to_podbean, upload_mp3_to_podbean, publish_to_podbean,
    PodbeanError
)
from wordpress_utils import publish_to_wordpress


@login_required
def index(request):
    sermons = Sermon.objects.all().order_by('-date')[:20]
    if request.method == "POST":
        pswd_form = FTPPasswordForm()
        if pswd_form.is_valid():
            # return HttpResponse('Entered Password')
            return HttpResponseRedirect('/sermons/update/')
    else:
        pswd_form = FTPPasswordForm()
    return render(
        request, 'sermon_index.html',
        {
            'sermons': sermons,
            'pswd_form': pswd_form,
            'oauth_url': oauth_utils.get_oauth_request_url()
        }
    )


# def login(request):
#     login(request, template_name='login.html')
#     return None
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#     else:
#         return HttpResponse("Invalid login details supplied.")


def update_from_ftp(request):
    from ftplib import error_perm
    if request.method == "POST":
        if 'download_sermon' in request.POST:
            try:
                oauth_token = oauth_utils.get_active_oauth_token(request)
                for sid in request.POST.getlist('sermon_select'):
                    sermon = Sermon.objects.get(pk=int(sid))
                    try:
                        cp_filename = ftp_utils.download_sermon_audio(
                            sermon.date
                        )
                        sermon.tmp_filename = os.path.basename(cp_filename)
                        sermon.save()
                        messages.add_message(
                            request, messages.INFO,
                            'Downloaded sermon {}'.format(
                                sermon.date.strftime('%b %d, %Y')
                            )
                        )
                        upload_auth = authorize_upload_to_podbean(
                            cp_filename, oauth_token,
                        )
                        upload_mp3_to_podbean(
                            cp_filename,
                            upload_auth['presigned_url'].encode('utf8'),
                        )
                        publish_response = publish_to_podbean(
                            sermon, upload_auth['file_key'], oauth_token,
                        )
                        sermon.pb_ep_id = publish_response['episode']['id']
                        sermon.save()

                        publish_to_wordpress(
                            sermon.pb_ep_id,
                            sermon.pretty_title(),
                            sermon.description
                        )

                    except IOError:
                        messages.add_message(
                            request, messages.ERROR,
                            'No file found for sermon "{}"'.format(
                                sermon.date
                            )
                        )
                    except PodbeanError as e:
                        print(e)
                        messages.add_message(
                            request, messages.ERROR,
                            'Problem publishing sermon to podbean "{}"'.format(
                                sermon.date
                            )
                        )
                return redirect('sermons:index')
            except error_perm:
                messages.add_message(
                    request, messages.ERROR, 'Incorrect password on download'
                )
                return redirect(
                    'sermons:index',
                )
        try:
            sermon_info = ftp_utils.download_sermon_info()
        except error_perm:
            messages.add_message(
                request, messages.ERROR, 'Incorrect password'
            )
            return redirect('sermons:index')
        for sinfo in sermon_info:
            try:
                prev_sermon = Sermon.objects.get(date=sinfo['date'])
                prev_sermon.has_ftp_file = sinfo.get('has_ftp_file')
                prev_sermon.save()
            except Sermon.DoesNotExist:
                new_sermon = Sermon.create(**sinfo)
                new_sermon.save()
            except Sermon.MultipleObjectsReturned:
                pass
        messages.add_message(
            request, messages.INFO, 'Successfully updated sermons'
        )
    return redirect('sermons:index')
