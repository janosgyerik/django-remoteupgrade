from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms


class RedeployForm(forms.Form):
    redeploy_id = forms.CharField()

    def clean_redeploy_id(self):
        data = self.cleaned_data['redeploy_id']
        if data not in settings.REDEPLOY_IDS:
            raise forms.ValidationError('Not a registered redeploy_id')

        return data


def response(message):
    return HttpResponse(message)


@csrf_exempt
def redeploy(request):
    form = RedeployForm(request.GET)
    if form.is_valid():
        return response('ok')
    else:
        return response(repr(form.errors))
