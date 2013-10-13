import subprocess

from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django import forms


class RedeployForm(forms.Form):
    redeploy_id = forms.CharField()

    def clean_redeploy_id(self):
        data = self.cleaned_data['redeploy_id']
        if data not in settings.REDEPLOY_IDS:
            raise forms.ValidationError('Not a registered redeploy_id')

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
def redeploy(request):
    form = RedeployForm(request.GET)
    if form.is_valid():
        proc = subprocess.Popen(settings.REDEPLOY_SCRIPT_WITH_ARGS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
