import subprocess

from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django import forms


class RemoteUpgradeForm(forms.Form):
    id = forms.CharField()

    def clean_id(self):
        data = self.cleaned_data['id']
        if data not in settings.REMOTEUPGRADE_IDS:
            raise forms.ValidationError('Not a registered id')

        return data


def response(args):
    return HttpResponse(json.dumps(args))


def success(args):
    args['success'] = True
    return response(args)


def error(args):
    args['success'] = False
    return response(args)


@csrf_exempt
def upgrade(request):
    form = RemoteUpgradeForm(request.GET)
    if form.is_valid():
        args = [
                settings.REMOTEUPGRADE_SCRIPT,
                request.META.get('HTTP_REFERER', 'no-referer'),
                request.META.get('HTTP_USER_AGENT', 'no-agent'),
                ]
        args.extend(settings.REMOTEUPGRADE_SCRIPT_EXTRA_ARGS)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        args = {
                'returncode': proc.returncode,
                'stdout': stdout,
                'stderr': stderr,
                }
        return success(args)
    else:
        args = {
                'errors': form.errors,
                }
        return error(args)
