import ctypes
from datetime import datetime
import epic_eos
import renpy as r
from renpy.store import (renpy, config)
import os
import sys

try:
    from typing import List
except:
    pass

# https://dev.epicgames.com/docs/epic-account-services/auth-interface

def bytes_to_str(charp):
    # type: (bytes) -> str
    if charp is None:
        return None
    else:
        return str(charp, 'utf-8')

def str_to_bytes(string):
    # type: (str) -> bytes
    if string is None:
        return None
    else:
        return string.encode('utf-8')

# Public API functions

def epic_shutdown():
    # type: () -> None
    # TODO: Detect restart and fully shutdown if it is
    epic_eos.ren.log(300, epic_eos.renpy_category, "Shutdown EOS")
    if epic_eos.eos_platform is not None:
        epic_eos.eos_platform.Release()
        epic_eos.eos_platform = None

def epic_init():
    # type: () -> None
    # TODO: Keep session alive on restart
    # Search for the dll in preset locations
    dll_paths = epic_eos.ren.resolve_dlls(epic_eos.ren.get_dlls_for(
        # TODO: do only one function call, this is ridiculous
        renpy.windows and (sys.maxsize > (1 << 32)),
        renpy.windows and (sys.maxsize <= (1 << 32)),
        not renpy.windows and not renpy.macintosh,
        renpy.macintosh,
        ))

    if not dll_paths:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Could not find EOS library to load for current system")
        return

    # Load DLL
    try:
        dll = ctypes.cdll[os.path.abspath(dll_paths[0])]
    except Exception as e:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to load library from '{}'. This is usually caused by a missing vcredist DLL.".format(dll_paths[0]), e)

    epic_eos.cdefs.load(dll)

    # Initialize EOS context
    init_opts = epic_eos.cdefs.EOS_InitializeOptions(
        ProductName = str_to_bytes(renpy.store.__(config.name or "Ren'Py Game")),
        ProductVersion = str_to_bytes(config.version or "1.0.0"),)
    init_status = epic_eos.cdefs.EOS_Initialize(init_opts)
    if init_status.value not in (epic_eos.cdefs.EOS_Success.value, epic_eos.cdefs.EOS_AlreadyConfigured.value):
        # Init failed and was not already configured
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to initialize EOS ({})".format(init_status.value))
        return

    # Configure logging
    logging_status = epic_eos.cdefs.EOS_Logging_SetCallback(epic_eos.compat.epic_logger)
    if logging_status.value != epic_eos.cdefs.EOS_Success.value:
        epic_eos.ren.log(300, epic_eos.renpy_category, "Failed to setup logging for Epic EOS ({})".format(logging_status.value))

    # Configure ticks handling
    if epic_eos.ren.periodic not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(epic_eos.ren.periodic)

    # Configure Platform
    eos_args = epic_eos.ren.get_epic_args()
    eos_connexion_clientinfo = epic_eos.cdefs.EOS_Platform_ClientCredentials()
    if eos_args.client and eos_args.clientsecret:
        eos_connexion_clientinfo.ClientId = str_to_bytes(eos_args.client)
        eos_connexion_clientinfo.ClientSecret = str_to_bytes(eos_args.clientsecret)
    init_opts = epic_eos.cdefs.EOS_Platform_Options(
        ProductId = str_to_bytes(eos_args.product),
        SandboxId = str_to_bytes(eos_args.sandbox),
        DeploymentId = str_to_bytes(eos_args.deployment),
        ClientCredentials = eos_connexion_clientinfo,
        Flags = epic_eos.cdefs.EOS_PF_WINDOWS_ENABLE_OVERLAY_OPENGL if renpy.windows else epic_eos.cdefs.EOS_PF_DISABLE_OVERLAY,
    )
    epic_eos.eos_platform = epic_eos.cdefs.EOS_HPlatform.Create(ctypes.byref(init_opts))

    epic_eos.ren.log(300, epic_eos.renpy_category, "Started Epic Online Services v{} with status {}".format(bytes_to_str(epic_eos.cdefs.EOS_GetVersion()), epic_eos.eos_platform.GetApplicationStatus().value))

    # Try to use epic login if available
    if eos_args.authtype:
        eos_auth = epic_eos.eos_platform.GetAuthInterface()
        if eos_args.authtype == 'exchangecode':
            # https://dev.epicgames.com/docs/epic-account-services/auth-interface#epic-games-launcher
            eos_credentials = epic_eos.cdefs.EOS_Auth_Credentials(
                Token = str_to_bytes(eos_args.password),
                Type = epic_eos.cdefs.EOS_LCT_ExchangeCode,
            )
        elif eos_args.authtype == 'developer':
            # https://dev.epicgames.com/docs/epic-account-services/developer-authentication-tool
            eos_credentials = epic_eos.cdefs.EOS_Auth_Credentials(
                Id = str_to_bytes(eos_args.user),
                Token = str_to_bytes(eos_args.password),
                Type = epic_eos.cdefs.EOS_LCT_Developer,
            )
        else:
            raise Exception("Unsupported Epic authtype: {}".format(eos_args.authtype))
        login_info = epic_eos.cdefs.EOS_Auth_LoginOptions(
            Credentials = ctypes.pointer(eos_credentials),
            ScopeFlags = epic_eos.cdefs.EOS_EAuthScopeFlags(config.epic_scopes if config.epic_scopes is not None else epic_eos.cdefs.EOS_AS_NoFlags.value),
        )
        eos_auth.Login(login_info, None, auth_login_callback)

    if config.enable_epic_achievements:
        retrieve_stats()

    if epic_shutdown not in config.at_exit_callbacks:
        config.at_exit_callbacks.append(epic_shutdown)

# Steam-like API functions

def is_logged_in(): # type: () -> None
    if epic_eos.eos_platform is not None:
        return 0 < epic_eos.eos_platform.GetConnectInterface().GetLoggedInUsersCount()
    else:
        return False

def retrieve_stats(): # type: () -> None
    if epic_eos.eos_platform is not None:
        eos_achievements = epic_eos.eos_platform.GetAchievementsInterface()
        opts = epic_eos.cdefs.EOS_Achievements_QueryDefinitionsOptions()
        user = get_local_user_id()
        if user:
            opts.LocalUserId = user
        eos_achievements.QueryDefinitions(
            ctypes.byref(opts),
            None, epic_eos.compat.achievements_querydefinitions_callback,
            )
    else:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Can't load epic achievements as epic is not available")

def list_achievements(): # type: () -> List[str]
    achievement_list = []
    if epic_eos.eos_platform is not None:
        interface = epic_eos.eos_platform.GetAchievementsInterface()
        count = interface.GetAchievementDefinitionCount(epic_eos.cdefs.EOS_Achievements_GetAchievementDefinitionCountOptions())
        for i in range(count):
            opt = epic_eos.cdefs.EOS_Achievements_CopyAchievementDefinitionV2ByIndexOptions(AchievementIndex = i)
            achievement_ref = ctypes.POINTER(epic_eos.cdefs.EOS_Achievements_DefinitionV2)()
            interface.CopyAchievementDefinitionV2ByIndex(opt, ctypes.byref(achievement_ref))
            if achievement_ref:
                achievement = achievement_ref[0]
                achievement_list.append(bytes_to_str(achievement.AchievementId))
                achievement.Release()
    return achievement_list

def get_achievement(name): # type: (str) -> bool
    is_unlocked = None
    if epic_eos.eos_platform is not None:
        user = get_local_user_id()
        if user:
            opts = epic_eos.cdefs.EOS_Achievements_CopyPlayerAchievementByAchievementIdOptions(
                LocalUserId = user,
                AchievementId = str_to_bytes(name),
            )
            achievement_ref = ctypes.POINTER(epic_eos.cdefs.EOS_Achievements_PlayerAchievement)()
            epic_eos.eos_platform.GetAchievementsInterface().CopyPlayerAchievementByAchievementId(
                opts, ctypes.byref(achievement_ref)
            )
            if achievement_ref:
                achievement = achievement_ref[0]
                is_unlocked = achievement.UnlockTime != epic_eos.cdefs.EOS_ACHIEVEMENTS_ACHIEVEMENT_UNLOCKTIME_UNDEFINED
                achievement.Release()
    return is_unlocked

def grant_achievement(name): # type: (str) -> None
    if epic_eos.eos_platform is not None:
        user = get_local_user_id()
        if user:
            interface = epic_eos.eos_platform.GetAchievementsInterface()
            name_bytes = ctypes.c_char_p(str_to_bytes(name))

            opts = epic_eos.cdefs.EOS_Achievements_UnlockAchievementsOptions(
                UserId = user,
                AchievementIds = ctypes.pointer(name_bytes),
                AchievementsCount = 1,
            )
            status = interface.UnlockAchievements(
                opts, None, achievements_unlocked_callback
            )
            if status.value != epic_eos.cdefs.EOS_Success.value:
                epic_eos.ren.log(
                    400, epic_eos.renpy_category,
                    "An error occured while granting the achievement '{}': {} - {}".format(
                        name, status.value, bytes_to_str(status.ToString()))
                )

# Internal API functions

def get_local_user_id(): # type: () -> str
    # Note that we assume that only one user is locally available and that it is the first connected user
    if epic_eos.eos_platform is not None:
        interface = epic_eos.eos_platform.GetConnectInterface() # FIXME: use connect interface
        account_count = interface.GetLoggedInUsersCount()
        if account_count > 0:
            account = interface.GetLoggedInUserByIndex(0)
            #account_buffer = ctypes.create_string_buffer(epic_eos.cdefs.EOS_PRODUCTUSERID_MAX_LENGTH+1)
            #account.ToString(account_buffer, ctypes.byref(ctypes.c_int32(ctypes.sizeof(account_buffer))))
            #return bytes_to_str(account_buffer.value)
            return account
    return None

# Generic native callback functions

@epic_eos.cdefs.EOS_Auth_OnLoginCallback
def auth_login_callback(login_info):
    # type: (ctypes.POINTER(epic_eos.cdefs.EOS_Auth_LoginCallbackInfo)) -> None
    if not login_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Auth login callback did not receive data")
        return
    info = login_info[0]
    if info.ResultCode.value != epic_eos.cdefs.EOS_Success.value:
        if info.AccountFeatureRestrictedInfo:
            target_uri = bytes_to_str(info.AccountFeatureRestrictedInfo[0].VerificationURI)
            epic_eos.ren.log(400, epic_eos.renpy_category, "Auth login callback failed because a manual action is required. Open {}".format(target_uri))
        else:
            epic_eos.ren.log(400, epic_eos.renpy_category, "Auth login callback failed with error: {} - {}".format(info.ResultCode.value, bytes_to_str(info.ResultCode.ToString())))
        return

    # EOS_Auth_CopyIdToken EOS_Auth_CopyUserAuthToken
    token_ref = ctypes.POINTER(epic_eos.cdefs.EOS_Auth_Token)()
    copy_result = epic_eos.eos_platform.GetAuthInterface().CopyUserAuthToken(
        epic_eos.cdefs.EOS_Auth_CopyUserAuthTokenOptions(),
        info.SelectedAccountId,
        ctypes.byref(token_ref),
    )
    if copy_result.value != epic_eos.cdefs.EOS_Success.value:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to get token in auth login callback")
        return
    token = token_ref[0]
    creds = epic_eos.cdefs.EOS_Connect_Credentials(
        Token = token.AccessToken,
        Type = epic_eos.cdefs.EOS_ECT_EPIC,
    )
    opts = epic_eos.cdefs.EOS_Connect_LoginOptions(
        Credentials = ctypes.pointer(creds),
        UserLoginInfo = None,
    )
    connect = epic_eos.eos_platform.GetConnectInterface()
    connect.Login(ctypes.byref(opts), None, connect_login_callback)
    token.Release()

@epic_eos.cdefs.EOS_Connect_OnLoginCallback
def connect_login_callback(login_info):
    # type: (ctypes.POINTER(ctypes.cdefs.EOS_Connect_LoginCallbackInfo)) -> None
    if not login_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Connect Login callback did not receive data")
        return

    info = login_info[0]
    if info.ResultCode.value == epic_eos.cdefs.EOS_Success.value:
        userid = ctypes.create_string_buffer(epic_eos.cdefs.EOS_PRODUCTUSERID_MAX_LENGTH + 1)
        info.LocalUserId.ToString(userid, ctypes.byref(ctypes.c_int32(ctypes.sizeof(userid))))
        epic_eos.ren.log(400, epic_eos.renpy_category, "Connected user {}".format(bytes_to_str(userid.value)))
        retrieve_stats()
    elif info.ResultCode.value == epic_eos.cdefs.EOS_InvalidUser.value:
        opts = epic_eos.cdefs.EOS_Connect_CreateUserOptions()
        if info.ContinuanceToken:
            opts.ContinuanceToken = info.ContinuanceToken
        connect = epic_eos.eos_platform.GetConnectInterface()
        connect.CreateUser(opts, None, connect_create_callback)
    else:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Connect login callback failed with error: {} - {}".format(info.ResultCode.value, bytes_to_str(info.ResultCode.ToString())))

@epic_eos.cdefs.EOS_Connect_OnCreateUserCallback
def connect_create_callback(create_info):
    if not create_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Connect OnCreateUser callback did not receive data")
        return

    info = create_info[0]
    if info.ResultCode.value == epic_eos.cdefs.EOS_Success.value:
        epic_eos.ren.log(100, epic_eos.renpy_category, "Created new EOS user")
        retrieve_stats()
    else:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to created new EOS user")

@epic_eos.cdefs.EOS_Achievements_OnUnlockAchievementsCompleteCallback
def achievements_unlocked_callback(data):
    # type: (epic_eos.cdefs.EOS_Achievements_OnUnlockAchievementsCompleteCallbackInfo) -> None
    if not data:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Achievements unlock callback did not receive data")
        return

    result = data[0]
    if result.ResultCode.value != epic_eos.cdefs.EOS_Success.value:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements unlock callback received error: {} - {}".format(data[0].ResultCode.value, bytes_to_str(data[0].ResultCode.ToString())))

@epic_eos.cdefs.EOS_Achievements_OnAchievementsUnlockedCallbackV2
def achievements_unlocknotify_callback(data):
    # type: (ctypes.POINTER(epic_eos.cdefs.EOS_Achievements_OnAchievementsUnlockedCallbackV2Info)) -> None
    if not data:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Achievements unlock notification callback did not receive data")
    else:
        achievement_info = data[0]
        productuser_buffer = ctypes.create_string_buffer(epic_eos.cdefs.EOS_PRODUCTUSERID_MAX_LENGTH + 1)
        achievement_info.UserId.ToString(productuser_buffer, ctypes.byref(ctypes.c_int32(ctypes.sizeof(productuser_buffer))))
        user_id = bytes_to_str(productuser_buffer)
        achievement_id = bytes_to_str(achievement_info.AchievementId)
        timestamp = achievement_info.UnlockTime.value
        epic_eos.ren.log(100, epic_eos.renpy_category, "User {} unlocked achievement {} at {}".format(user_id, achievement_id, datetime.fromtimestamp(timestamp)))
        # TODO: add renpy callbacks array

@epic_eos.cdefs.EOS_Achievements_OnQueryDefinitionsCompleteCallback
def achievements_querydefinitions_callback(data):
    # type: (ctypes.POINTER(epic_eos.cdefs.EOS_Achievements_OnQueryDefinitionsCompleteCallbackInfo)) -> None
    if not epic_eos.ren.is_epic_available():
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements callback called after main handle expiration")
        return
    if data[0].ResultCode.value == epic_eos.cdefs.EOS_Success.value:
        eos_achievements = epic_eos.eos_platform.GetAchievementsInterface()
        cached_achievements_count = eos_achievements.GetAchievementDefinitionCount(epic_eos.cdefs.EOS_Achievements_GetAchievementDefinitionCountOptions())
        epic_eos.ren.log(200, epic_eos.renpy_category, "Done loading {} achievements".format(cached_achievements_count))
    else:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements definitions query received error: {} - {}".format(data[0].ResultCode.value, bytes_to_str(data[0].ResultCode.ToString())))

@epic_eos.cdefs.EOS_LogMessageFunc
def epic_logger(message):
    # type: (ctypes.POINTER(epic_eos.cdefs.EOS_LogMessage)) -> None
    m = message[0]
    epic_eos.ren.log(m.Level.value, bytes_to_str(m.Category), bytes_to_str(m.Message))
