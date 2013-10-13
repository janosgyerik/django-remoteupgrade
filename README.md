Django Remote Upgrade
=====================
A simple Django App to make remote upgrading easy using web hooks.

TODO: how it works


Setup
-----
1. Copy the `remoteupgrade` directory to your project.
   TODO: It would be better to use Git submodules
   TODO: It would be good to distribute with `pip`

2. Add the following variables to your Django settings:

        REMOTEUPGRADE_IDS = [ 'DFA07FFB-B5B0-4115-A0C9-C948D381F43C', ]
        REMOTEUPGRADE_SCRIPT = '/path/to/upgrade/script.sh'
        REMOTEUPGRADE_SCRIPT_EXTRA_ARGS = []

    The IDs should be secret to your site, so that others
    cannot remote upgrade it so easily.
    It's a list, so you can have multiple valid ids.

    The script should be your custom script that can automatically
    upgrade your site, Django will call this script with two arguments:
    the HTTP_REFERER and HTTP_USER_AGENT of the caller.
    Keep in mind that your shell environment can be very different from
    that of Django's. It's safest to use an absolute path, for example.

    Refer to the sample script in `demo/local/upgrade.sh.sample`

3. Add `remoteupgrade` to your `INSTALLED_APPS` list

4. Add the following URL handler:

        url(r'^remoteupgrade/$', 'remoteupgrade.views.upgrade', name='remoteupgrade')


Running the demo
----------------
TODO


Running the unit tests
----------------------
TODO
