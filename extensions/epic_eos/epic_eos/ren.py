"""Ren'Py-facing functions"""
from __future__ import print_function
import os
import sys
import epic_eos
import renpy as r
from renpy.store import (renpy, config)

def log(level, category, message, *args):
    # type: (int, str, str, ...) -> None
    """Default high-level logging callback."""
    if renpy.store.config.epic_log_console:
        print("[{}] {} - {}".format(level, category, message), *args)
    else:
        renpy.write_log("[{}] {} - {}".format(level, category, message), *args)

def periodic():
    # type: () -> None
    """Function called by Ren'Py to allow periodic data processing."""
    if is_epic_available():
        epic_eos.eos_platform.Tick()

def get_epic_args():
    """Get arguments received via cmdline."""
    class AttrContainer(object):
        """Pseudo-class used to store parsed parameters"""
        client = renpy.config.epic_client
        clientsecret = renpy.config.epic_clientsecret
        product = renpy.config.epic_product
        sandbox = renpy.config.epic_sandbox
        deployment = renpy.config.epic_deployment
        user = renpy.config.epic_userlogin
        password = renpy.config.epic_userpassword
        authtype = renpy.config.epic_authtype
        userid = None
        username = ''
        env = 'Dev'
        appid = ''
        locale = None
        is_portal = False

    argset = AttrContainer()

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
    """Check whether the epic SDK is loaded."""
    return epic_eos.eos_platform is not None

def get_dlls_for(win_64 = False, win32 = False, linux = False, mac = False):
    # type: (bool, bool, bool, bool) -> list
    """Get DLL path for the current system."""
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

def resolve_dlls(dll_list):
    # type: (List[str]) -> list
    """From a list of dlls, return the valid dll paths that are found."""
    dll_paths = []
    for dll_name in dll_list:
        is_found = False
        for p in [config.basedir, os.path.dirname(sys.executable)] + config.searchpath:
            for subpath in ['libs', '.']:
                if os.path.exists(os.path.join(p, subpath, dll_name)):
                    dll_paths.append(os.path.join(p, subpath, dll_name))
                    is_found = True
                    break
            if is_found is True:
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

        epic_stat, stat_max, stat_modulo = self.stats[name]
        epic_eos.compat.add_int_stat(epic_stat, completed)

    def has(self, name):
        name = self.names.get(name, name)

        return renpy.store.config.epic_report_achievements_status and renpy.store.epicapi.get_achievement(name)
