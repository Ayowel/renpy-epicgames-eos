from __future__ import print_function
import epic_eos
import os
import renpy as r
from renpy.store import (renpy, config)
import sys

def log(level, category, message, *args):
    # type: (int, str, str, ...) -> None
    if renpy.store.config.epic_log_console:
        print("[{}] {} - {}".format(level, category, message), *args)
    else:
        renpy.write_log("[{}] {} - {}".format(level, category, message), *args)

def periodic():
    # type: () -> None
    if is_epic_available():
        epic_eos.eos_platform.Tick()

def get_epic_args():
    class attr_container(object):
        pass
    argset = attr_container
    argset.client = renpy.config.epic_client
    argset.clientsecret = renpy.config.epic_clientsecret
    argset.product = renpy.config.epic_product
    argset.sandbox = renpy.config.epic_sandbox
    argset.deployment = renpy.config.epic_deployment
    argset.user = renpy.config.epic_userlogin
    argset.password = renpy.config.epic_userpassword
    argset.authtype = renpy.config.epic_authtype
    argset.userid = None
    argset.username = ''
    argset.env = 'Dev'
    argset.appid = ''
    argset.locale = None
    argset.is_portal = False

    epic_args = getattr(r.arguments, 'epic_arguments', None)
    if epic_args:
        for arg in epic_args:
            if arg.startswith('-AUTH_LOGIN='):
                argset.user = arg.split('=')[1]
            elif arg.startswith('-AUTH_PASSWORD='):
                argset.password = arg.split('=')[1]
            elif arg.startswith('-AUTH_TYPE='):
                argset.authtype = arg.split('=')[1]
            elif arg.startswith('-epicapp='):
                argset.appid = arg.split('=')[1]
            elif arg.startswith('-epicenv='):
                argset.env = arg.split('=')[1]
            elif arg == '-EpicPortal':
                argset.is_portal = True
            elif arg.startswith('-epicusername='):
                argset.username = arg.split('=')[1]
            elif arg.startswith('-epicuserid='):
                argset.userid = arg.split('=')[1]
            elif arg.startswith('-epiclocale='):
                argset.locale = arg.split('=')[1]
            elif arg.startswith('-epicsandboxid='):
                argset.sandbox = arg.split('=')[1]
            elif arg.startswith('-epicdeployment='): # Not an officially-supported arg
                argset.deployment = arg.split('=')[1]
    return argset

def is_epic_available():
    # type: () -> bool
    return epic_eos.eos_platform is not None

def get_dlls_for(win_64 = False, win32 = False, linux = False, mac = False):
    # type: (bool, bool, bool, bool) -> list
    target_dlls = []
    if win_64:
        target_dlls.append("EOSSDK-Win64-Shipping.dll")
    if win32:
        target_dlls.append("EOSSDK-Win32-Shipping.dll")
    if linux:
        target_dlls.append("libEOSSDK-Linux-Shipping.so")
    if mac:
        target_dlls.append("libEOSSDK-Mac-Shipping.dylib")
    return target_dlls

def resolve_dlls(list):
    # type: (list) -> list
    dll_paths = []
    for dll_name in list:
        is_found = False
        for p in [config.basedir, os.path.dirname(sys.executable)] + config.searchpath:
            for subpath in ['libs', '.']:
                if os.path.exists(os.path.join(p, subpath, dll_name)):
                    dll_paths.append(os.path.join(p, subpath, dll_name))
                    is_found = True
                    break
            if is_found == True:
                break
    return dll_paths

try:
    obj = renpy.revertable.RevertableObject
except:# 7.4.X or older
    obj = renpy.python.RevertableObject

class EpicBackend(obj): # TODO: migrate to rpy file to inherit Backend
    """
    A backend that sends achievements to Epic. This is only used if Epic
    has loaded and initialized successfully.
    """

    def __init__(self):
        # A map from achievement name to steam name.
        self.names = { }
        self.stats = { }

        renpy.store.epicapi.retrieve_stats()
        # renpy.maximum_framerate(steam_maximum_framerate)

    def register(self, name, epic=None, epic_stat=None, stat_max=None, stat_modulo=1, **kwargs):
        if epic is not None:
            self.names[name] = epic
        if epic_stat is None:
            epic_stat = epic or name

        self.stats[name] = (epic_stat, stat_max, stat_modulo)

    def grant(self, name):
        name = self.names.get(name, name)

        renpy.store.epicapi.grant_achievement(name)

    def clear(self, name):
        pass # Clearing achievements is not supported by Epic at the moment

    def clear_all(self):
        pass # Clearing achievements is not supported by Epic at the moment

    def progress(self, name, completed):
        # Epic games only support integer stat variations
        completed = int(completed)

        if name not in self.stats:
            if config.developer:
                raise Exception("To report progress, you must register the stat {} first.".format(name))
            else:
                return

        # current = persistent._achievement_progress.get(name, 0)

        epic_stat, stat_max, stat_modulo = self.stats[name]

        epic_eos.compat.set_int_stat(epic_stat, completed)
        # name = self.names.get(name, name)

        # if (current is not None) and (current >= completed):
        #     return

        # renpy.maximum_framerate(steam_maximum_framerate)

        # if completed >= stat_max:
        #     steam.grant_achievement(name)
        # else:
        #     if (stat_modulo is None) or (completed % stat_modulo) == 0:
        #         steam.indicate_achievement_progress(name, completed, stat_max)

        # steam.store_stats()

    def has(self, name):
        name = self.names.get(name, name)

        return renpy.store.config.epic_report_achievements_status and renpy.store.epicapi.get_achievement(name)
