from builtins import str
import ctypes
from datetime import datetime
import epic_eos
from . import cdefs
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
    """Turn a bytes array into a string."""
    if charp is None:
        return None
    else:
        return str(charp, 'utf-8')

def str_to_bytes(string):
    # type: (str) -> bytes
    """Turn a string into a bytes array."""
    if string is None:
        return None
    else:
        return string.encode('utf-8')

# Used to store allocated data that needs to be persisted through calls (UserData parameters)
# FIXME: values are never deallocated
ctypes_allocated_data = []

def id_to_c_char_p(eos_id, length):
    # type: (cdefs.EOS_EpicAccountId|cdefs.EOS_ProductUserId, int) -> ctypes.c_char_p
    """Build the string for an ID type."""
    eos_id_size = ctypes.c_int32(length+1)
    eos_id_buffer = ctypes.create_string_buffer(eos_id_size.value)
    retval = eos_id.ToString(eos_id_buffer, ctypes.byref(eos_id_size))
    if retval.value != cdefs.EOS_Success.value:
        return None
    return ctypes.c_char_p(eos_id_buffer.value)

# Public API functions

def epic_shutdown():
    # type: () -> None
    """Stop the SDK."""
    # TODO: Detect restart and fully shutdown if it is
    epic_eos.ren.log(300, epic_eos.renpy_category, "Shutdown EOS")
    if epic_eos.eos_platform is not None:
        epic_eos.eos_platform.Release()
        epic_eos.eos_platform = None

def load(force = False):
    """Load the SDK's DLL."""
    # Search for the dll in preset locations
    # Only try to load if the dll is not already loaded
    if cdefs.EOS_Initialize is cdefs.not_ready or force:
        dll_paths = epic_eos.ren.resolve_dlls(epic_eos.ren.get_dlls_for(
            # TODO: do only one function call, this is ridiculous
            renpy.windows and (sys.maxsize > (1 << 32)),
            renpy.windows and (sys.maxsize <= (1 << 32)),
            not renpy.windows and not renpy.macintosh,
            renpy.macintosh,
            ))

        if not dll_paths:
            epic_eos.ren.log(500, epic_eos.renpy_category, "Could not find EOS library to load for current system")
            return False

        # Load DLL
        try:
            dll = ctypes.cdll[os.path.abspath(dll_paths[0])]
        except Exception as e:
            epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to load library from '{}'. This is usually caused by a missing vcredist DLL.".format(dll_paths[0]), e)
            return False

        cdefs.load(dll)
    return True

def epic_init():
    # type: () -> None
    """Initialize the SDK."""
    if not load():
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to load the epic DLL - aborting initialisation")
        return False

    # Initialize EOS context
    init_opts = cdefs.EOS_InitializeOptions(
        ProductName = str_to_bytes(renpy.store.__(config.name or "Ren'Py Game")),
        ProductVersion = str_to_bytes(config.version or "1.0.0"),)
    init_status = cdefs.EOS_Initialize(init_opts)
    if init_status.value not in (cdefs.EOS_Success.value, cdefs.EOS_AlreadyConfigured.value):
        # Init failed and was not already configured
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to initialize EOS ({})".format(init_status.value))
        return False

    # Configure logging
    logging_status = cdefs.EOS_Logging_SetCallback(epic_eos.compat.epic_logger)
    if logging_status.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(300, epic_eos.renpy_category, "Failed to setup logging for Epic EOS ({})".format(logging_status.value))

    # Configure ticks handling
    if epic_eos.ren.periodic not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(epic_eos.ren.periodic)

    # Configure Platform
    # Do not recreate on reload if a platform already exists because the token provided
    # by the Epic Games Store would probably have expired
    if epic_eos.eos_platform is None:
        eos_args = epic_eos.ren.get_epic_args()
        eos_connexion_clientinfo = cdefs.EOS_Platform_ClientCredentials()
        if eos_args.client and eos_args.clientsecret:
            eos_connexion_clientinfo.ClientId = str_to_bytes(eos_args.client)
            eos_connexion_clientinfo.ClientSecret = str_to_bytes(eos_args.clientsecret)
        init_opts = cdefs.EOS_Platform_Options(
            ProductId = str_to_bytes(eos_args.product),
            SandboxId = str_to_bytes(eos_args.sandbox),
            DeploymentId = str_to_bytes(eos_args.deployment),
            ClientCredentials = eos_connexion_clientinfo,
            Flags = cdefs.EOS_PF_WINDOWS_ENABLE_OVERLAY_OPENGL if renpy.windows else cdefs.EOS_PF_DISABLE_OVERLAY,
        )
        epic_eos.eos_platform = cdefs.EOS_HPlatform.Create(ctypes.byref(init_opts))

        epic_eos.ren.log(300, epic_eos.renpy_category, "Started Epic Online Services v{} with status {}".format(bytes_to_str(cdefs.EOS_GetVersion()), epic_eos.eos_platform.GetApplicationStatus().value))

        # Try to use epic login if available
        if eos_args.authtype:
            eos_auth = epic_eos.eos_platform.GetAuthInterface()
            if eos_args.authtype == 'exchangecode':
                # https://dev.epicgames.com/docs/epic-account-services/auth-interface#epic-games-launcher
                eos_credentials = cdefs.EOS_Auth_Credentials(
                    Token = str_to_bytes(eos_args.password),
                    Type = cdefs.EOS_LCT_ExchangeCode,
                )
            elif eos_args.authtype == 'developer':
                # https://dev.epicgames.com/docs/epic-account-services/developer-authentication-tool
                eos_credentials = cdefs.EOS_Auth_Credentials(
                    Id = str_to_bytes(eos_args.user),
                    Token = str_to_bytes(eos_args.password),
                    Type = cdefs.EOS_LCT_Developer,
                )
            else:
                if config.developer:
                    raise Exception("Unsupported Epic authtype: {}".format(eos_args.authtype))
                else:
                    epic_eos.ren.log(500, epic_eos.renpy_category, "Unsupported Epic authtype: {}".format(eos_args.authtype))
                    return False
            login_info = cdefs.EOS_Auth_LoginOptions(
                Credentials = ctypes.pointer(eos_credentials),
                ScopeFlags = cdefs.EOS_EAuthScopeFlags(config.epic_scopes if config.epic_scopes is not None else cdefs.EOS_AS_NoFlags.value),
            )
            eos_auth.Login(login_info, None, auth_login_callback)

        # Configure session keep-alive
        connect = epic_eos.eos_platform.GetConnectInterface().AddNotifyAuthExpiration(
            cdefs.EOS_Connect_AddNotifyAuthExpirationOptions(),
            None,
            session_keep_alive
        )
    else:
        epic_eos.ren.log(300, epic_eos.renpy_category, "Skipped platform creation and login because Epic Online Services v{} is already started (status: {})".format(bytes_to_str(cdefs.EOS_GetVersion()), epic_eos.eos_platform.GetApplicationStatus().value))

    if hasattr(config, 'at_exit_callbacks') and epic_shutdown not in config.at_exit_callbacks:
        config.at_exit_callbacks.append(epic_shutdown)

    return True

# Steam-like API functions

def is_logged_in(): # type: () -> None
    """Check whether the user is logged in."""
    if epic_eos.eos_platform is not None:
        return 0 < epic_eos.eos_platform.GetConnectInterface().GetLoggedInUsersCount()
    else:
        return False

def retrieve_stats(): # type: () -> None
    """Schedule a cached stats update."""
    if epic_eos.eos_platform is not None:
        # FIXME: this should retrieve stats, not achievements
        eos_achievements = epic_eos.eos_platform.GetAchievementsInterface()
        opts = cdefs.EOS_Achievements_QueryDefinitionsOptions()
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
    """Get all loaded achievements for a user. Call retrieve_stats and wait a bit before calling this."""
    achievement_list = []
    if epic_eos.eos_platform is not None:
        interface = epic_eos.eos_platform.GetAchievementsInterface()
        count = interface.GetAchievementDefinitionCount(cdefs.EOS_Achievements_GetAchievementDefinitionCountOptions())
        for i in range(count):
            opt = cdefs.EOS_Achievements_CopyAchievementDefinitionV2ByIndexOptions(AchievementIndex = i)
            achievement_ref = ctypes.POINTER(cdefs.EOS_Achievements_DefinitionV2)()
            interface.CopyAchievementDefinitionV2ByIndex(opt, ctypes.byref(achievement_ref))
            if achievement_ref:
                achievement = achievement_ref[0]
                achievement_list.append(bytes_to_str(achievement.AchievementId))
                achievement.Release()
    return achievement_list

def get_achievement(name): # type: (str) -> bool
    """Get a specific loaded achievement's information."""
    is_unlocked = None
    if epic_eos.eos_platform is not None:
        user = get_local_user_id()
        if user:
            opts = cdefs.EOS_Achievements_CopyPlayerAchievementByAchievementIdOptions(
                LocalUserId = user,
                TargetUserId = user,
                AchievementId = str_to_bytes(name),
            )
            achievement_ref = ctypes.POINTER(cdefs.EOS_Achievements_PlayerAchievement)()
            epic_eos.eos_platform.GetAchievementsInterface().CopyPlayerAchievementByAchievementId(
                opts, ctypes.byref(achievement_ref)
            )
            if achievement_ref:
                achievement = achievement_ref.contents
                is_unlocked = achievement.UnlockTime != cdefs.EOS_ACHIEVEMENTS_ACHIEVEMENT_UNLOCKTIME_UNDEFINED
                achievement.Release()
    return is_unlocked

def grant_achievement(name): # type: (str) -> None
    """Grant an achievement to the user."""
    if epic_eos.eos_platform is not None:
        user = get_local_user_id()
        if user:
            interface = epic_eos.eos_platform.GetAchievementsInterface()
            name_bytes = ctypes.c_char_p(str_to_bytes(name))

            opts = cdefs.EOS_Achievements_UnlockAchievementsOptions(
                UserId = user,
                AchievementIds = ctypes.pointer(name_bytes),
                AchievementsCount = 1,
            )
            status = interface.UnlockAchievements(
                opts, None, achievements_unlocked_callback
            )
            if status.value != cdefs.EOS_Success.value:
                epic_eos.ren.log(
                    400, epic_eos.renpy_category,
                    "An error occured while granting the achievement '{}': {} - {}".format(
                        name, status.value, bytes_to_str(status.ToString()))
                )

def add_int_stat(name, value):
    """Increment the value of a game stat."""
    if epic_eos.eos_platform is not None:
        user = get_local_user_id()
        if user:
            interface = epic_eos.eos_platform.GetStatsInterface()
            stat = cdefs.EOS_Stats_IngestData(
                StatName = str_to_bytes(name),
                IngestAmount = value,
            )
            opts = cdefs.EOS_Stats_IngestStatOptions(
                LocalUserId = user,
                TargetUserId = user,
                Stats = ctypes.pointer(stat),
                StatsCount = 1,
            )
            interface.IngestStat(opts, None, stats_ingest_callback)

# Internal API functions and data

account_id_map = {} # map a ProductUserId string to an EpicAccountId string

def map_product_user_to_epic_account(product_user):
    # type: (cdefs.EOS_ProductUserId) -> cdefs.EOS_EpicAccountId|None
    """Retrieve an EOS_EpicAccountId from an EOS_ProductUserId."""
    product_user_buffer_size = ctypes.c_int32(cdefs.EOS_PRODUCTUSERID_MAX_LENGTH+1)
    product_user_buffer = ctypes.create_string_buffer(product_user_buffer_size.value)
    retval = product_user.ToString(product_user_buffer, ctypes.byref(product_user_buffer_size))
    if retval.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to convert Product User ID to string")
        return None

    product_user_string = ctypes.c_char_p(product_user_buffer).value
    global account_id_map
    epic_accounts = account_id_map.get(product_user_string, set())
    if epic_accounts:
        for epic_account_string in epic_accounts:
            epic_account_string = account_id_map[product_user_string]
            epic_account = ctypes.c_char_p(epic_account_string.encode('utf-8'))
            epic_account_object = cdefs.EOS_EpicAccountId.FromString(epic_account)
            if epic_account_object.IsValid().value == cdefs.EOS_TRUE.value:
                epic_eos.ren.log(500, epic_eos.renpy_category, "Invalid epic account ID {} for local user {}".format(epic_account_string, product_user_string))
                continue
            return epic_account_object
    return None

def set_product_user_to_epic_account_mapping(product_user, epic_account):
    # type: (cdefs.EOS_ProductUserId, cdefs.EOS_EpicAccountId) -> None
    """Register the pairing between an EOS_ProductUserId and an EOS_EpicAccountId."""
    product_user_buffer_size = ctypes.c_int32(cdefs.EOS_PRODUCTUSERID_MAX_LENGTH+1)
    product_user_buffer = ctypes.create_string_buffer(product_user_buffer_size.value)
    retval = product_user.ToString(product_user_buffer, ctypes.byref(product_user_buffer_size))
    if retval.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to convert Product User ID to string")
        return

    epic_account_buffer_size = ctypes.c_int32(cdefs.EOS_EPICACCOUNTID_MAX_LENGTH+1)
    epic_account_buffer = ctypes.create_string_buffer(epic_account_buffer_size.value)
    retval = epic_account.ToString(epic_account_buffer, ctypes.byref(epic_account_buffer_size))
    if retval.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to convert Epic Account ID to string")
        return

    global account_id_map
    product_user_string = ctypes.c_char_p(product_user_buffer).value
    if product_user_string not in account_id_map:
        account_id_map[product_user_string] = set()
    account_id_map[product_user_string] = ctypes.c_char_p(epic_account_buffer).value

def get_local_user_id(): # type: () -> cdefs.EOS_ProductUserId
    """Get the current user's ID."""
    # Note that we assume that only one user is locally available and that it is the first connected user
    if epic_eos.eos_platform is not None:
        interface = epic_eos.eos_platform.GetConnectInterface()
        account_count = interface.GetLoggedInUsersCount()
        if account_count > 0:
            account = interface.GetLoggedInUserByIndex(0)
            #account_buffer = ctypes.create_string_buffer(cdefs.EOS_PRODUCTUSERID_MAX_LENGTH+1)
            #account.ToString(account_buffer, ctypes.byref(ctypes.c_int32(ctypes.sizeof(account_buffer))))
            #return bytes_to_str(account_buffer.value)
            return account
        else:
            epic_eos.ren.log(200, epic_eos.renpy_category, "Tried to get local user ID but no account was available")
    return None

# Generic native callback functions

@cdefs.EOS_Auth_OnLoginCallback
def auth_login_callback(login_info):
    # type: (ctypes.POINTER(cdefs.EOS_Auth_LoginCallbackInfo)) -> None
    """Callback used for the initial login attempt."""
    if not login_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Auth login callback did not receive data")
        return
    info = login_info[0]
    if info.ResultCode.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Auth login callback failed with error: {} - {}".format(info.ResultCode.value, bytes_to_str(info.ResultCode.ToString())))
        return

    # EOS_Auth_CopyIdToken EOS_Auth_CopyUserAuthToken
    token_ref = ctypes.POINTER(cdefs.EOS_Auth_Token)()
    copy_result = epic_eos.eos_platform.GetAuthInterface().CopyUserAuthToken(
        cdefs.EOS_Auth_CopyUserAuthTokenOptions(),
        info.SelectedAccountId,
        ctypes.byref(token_ref),
    )
    if copy_result.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to get token in auth login callback")
        return

    # Get Epic account ID as string for storage and pass-down
    epic_account_id = id_to_c_char_p(info.SelectedAccountId, cdefs.EOS_EPICACCOUNTID_MAX_LENGTH)
    if not epic_account_id:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to stringify epic account ID ({})".format(info.SelectedAccountId))
        return
    global ctypes_allocated_data
    ctypes_allocated_data.append(epic_account_id)

    # Login with connect interface
    creds = cdefs.EOS_Connect_Credentials(
        Token = token_ref.contents.AccessToken,
        Type = cdefs.EOS_ECT_EPIC,
    )
    opts = cdefs.EOS_Connect_LoginOptions(
        Credentials = ctypes.pointer(creds),
        UserLoginInfo = None,
    )
    connect = epic_eos.eos_platform.GetConnectInterface()
    connect.Login(ctypes.byref(opts), epic_account_id, connect_login_callback)
    token_ref.contents.Release()

@cdefs.EOS_Connect_OnLoginCallback
def connect_login_callback(login_info):
    # type: (ctypes.POINTER(ctypes.cdefs.EOS_Connect_LoginCallbackInfo)) -> None
    """Callback used for the secondary login attempt."""
    if not login_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Connect Login callback did not receive data")
        return

    info = login_info.contents
    if info.ResultCode.value == cdefs.EOS_Success.value:
        product_user_id = id_to_c_char_p(info.LocalUserId, cdefs.EOS_PRODUCTUSERID_MAX_LENGTH)
        epic_eos.ren.log(400, epic_eos.renpy_category, "Connected user {}".format(product_user_id.value))
        if info.ClientData: # ClientData is a c_char_p of the EpicAccountId
            epic_account_id_string = ctypes.cast(info.ClientData, ctypes.c_char_p)
            global account_id_map
            account_id_map[product_user_id.value] = epic_account_id_string.value
        retrieve_stats()
    elif info.ResultCode.value == cdefs.EOS_InvalidUser.value:
        opts = cdefs.EOS_Connect_CreateUserOptions()
        if info.ContinuanceToken:
            opts.ContinuanceToken = info.ContinuanceToken
        connect = epic_eos.eos_platform.GetConnectInterface()
        connect.CreateUser(opts, info.ClientData, connect_create_callback)
    else:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Connect login callback failed with error: {} - {}".format(info.ResultCode.value, bytes_to_str(info.ResultCode.ToString())))

@cdefs.EOS_Connect_OnCreateUserCallback
def connect_create_callback(create_info):
    # type: (cdefs.EOS_Connect_CreateUserCallbackInfo) -> None
    """Callback for when a user plays for the first time and their game account is created."""
    if not create_info:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Connect OnCreateUser callback did not receive data")
        return

    info = create_info.contents
    if info.ResultCode.value == cdefs.EOS_Success.value:
        product_user_id = id_to_c_char_p(info.LocalUserId, cdefs.EOS_PRODUCTUSERID_MAX_LENGTH)
        epic_eos.ren.log(100, epic_eos.renpy_category, "Created new EOS user {}".format(product_user_id.value))
        if info.ClientData: # ClientData is a c_char_p of the EpicAccountId
            epic_account_id_string = ctypes.cast(info.ClientData, ctypes.c_char_p)
            global account_id_map
            account_id_map[product_user_id.value] = epic_account_id_string.value
        retrieve_stats()
    else:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to created new EOS user")

@cdefs.EOS_Achievements_OnUnlockAchievementsCompleteCallback
def achievements_unlocked_callback(data):
    # type: (cdefs.EOS_Achievements_OnUnlockAchievementsCompleteCallbackInfo) -> None
    """Callback for when an achievement's local unlocking is done being notified to Epic."""
    if not data:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Achievements unlock callback did not receive data")
        return

    result = data[0]
    if result.ResultCode.value != cdefs.EOS_Success.value:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements unlock callback received error: {} - {}".format(data[0].ResultCode.value, bytes_to_str(data[0].ResultCode.ToString())))

@cdefs.EOS_Achievements_OnAchievementsUnlockedCallbackV2
def achievements_unlocknotify_callback(data):
    # type: (ctypes.POINTER(cdefs.EOS_Achievements_OnAchievementsUnlockedCallbackV2Info)) -> None
    """Callback for when an achievement was unlocked on epic's side instead of in-game."""
    if not data:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Achievements unlock notification callback did not receive data")
    else:
        achievement_info = data[0]
        productuser_buffer = ctypes.create_string_buffer(cdefs.EOS_PRODUCTUSERID_MAX_LENGTH + 1)
        achievement_info.UserId.ToString(productuser_buffer, ctypes.byref(ctypes.c_int32(ctypes.sizeof(productuser_buffer))))
        user_id = bytes_to_str(productuser_buffer)
        achievement_id = bytes_to_str(achievement_info.AchievementId)
        timestamp = achievement_info.UnlockTime.value
        epic_eos.ren.log(100, epic_eos.renpy_category, "User {} unlocked achievement {} at {}".format(user_id, achievement_id, datetime.fromtimestamp(timestamp)))
        # TODO: add renpy callbacks array

@cdefs.EOS_Achievements_OnQueryDefinitionsCompleteCallback
def achievements_querydefinitions_callback(data):
    # type: (ctypes.POINTER(cdefs.EOS_Achievements_OnQueryDefinitionsCompleteCallbackInfo)) -> None
    """Query definition callback."""
    if not epic_eos.ren.is_epic_available():
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements callback called after main handle expiration")
        return
    if data[0].ResultCode.value == cdefs.EOS_Success.value:
        eos_achievements = epic_eos.eos_platform.GetAchievementsInterface()
        cached_achievements_count = eos_achievements.GetAchievementDefinitionCount(cdefs.EOS_Achievements_GetAchievementDefinitionCountOptions())
        epic_eos.ren.log(200, epic_eos.renpy_category, "Done loading {} achievements".format(cached_achievements_count))
    else:
        epic_eos.ren.log(400, epic_eos.renpy_category, "Achievements definitions query received error: {} - {}".format(data[0].ResultCode.value, bytes_to_str(data[0].ResultCode.ToString())))

@cdefs.EOS_Stats_OnIngestStatCompleteCallback
def stats_ingest_callback(data):
    # type: (ctypes.POINTER(cdefs.EOS_Stats_IngestStatCompleteCallbackInfo)) -> None
    """Stats ingext callback."""
    if not data:
        epic_eos.ren.log(500, epic_eos.renpy_category, "Stats ingest notification callback did not receive data")
    else:
        if data.contents.ResultCode.value == cdefs.EOS_Success.value:
            epic_eos.ren.log(100, epic_eos.renpy_category, "Done ingesting stats")
        else:
            epic_eos.ren.log(400, epic_eos.renpy_category, "Failed to ingest stats: {} - {}".format(data.contents.ResultCode.value, bytes_to_str(data.contents.ResultCode.ToString())))

@cdefs.EOS_Connect_OnAuthExpirationCallback
def session_keep_alive(data):
    # type: (ctypes.POINTER(EOS_Connect_AuthExpirationCallbackInfo)) -> None
    """Handles logged in user's token renewal."""
    if epic_eos.eos_platform is not None:
        # Map local ID to Epic ID
        local_user_id_string = id_to_c_char_p(data.contents.LocalUserId, cdefs.EOS_PRODUCTUSERID_MAX_LENGTH)
        global account_id_map
        if local_user_id_string.value not in account_id_map:
            epic_eos.ren.log(500, epic_eos.renpy_category, "Failed to renew session for local user {} - no matching Epic Accound ID found".format(local_user_id_string.value))
            return
        epic_account_id = cdefs.EOS_EpicAccountId.FromString(ctypes.c_char_p(account_id_map[local_user_id_string.value]))

        # Get Token for Epic ID
        auth = epic_eos.eos_platform.GetAuthInterface()
        epic_account_token = ctypes.POINTER(cdefs.EOS_Auth_Token)()

        retval = auth.CopyUserAuthToken(
            cdefs.EOS_Auth_CopyUserAuthTokenOptions(),
            epic_account_id,
            ctypes.byref(epic_account_token),
        )
        if retval.value != cdefs.EOS_Success.value:
            epic_eos.ren.log(
                500, epic_eos.renpy_category,
                "Failed to get token for local user {} with Epic Accound {} (error {})".format(
                    local_user_id_string.value,
                    account_id_map[local_user_id_string.value],
                    retval.value,
                    )
                )
            return

        # Renew Connect session
        connect = epic_eos.eos_platform.GetConnectInterface()
        creds = cdefs.EOS_Connect_Credentials(
            Token = epic_account_token.contents.AccessToken,
            Type = cdefs.EOS_ECT_EPIC,
        )
        opts = cdefs.EOS_Connect_LoginOptions(
            Credentials = ctypes.pointer(creds),
            UserLoginInfo = None,
        )
        connect = epic_eos.eos_platform.GetConnectInterface()
        connect.Login(ctypes.byref(opts), None, connect_login_callback)
        epic_eos.ren.log(
            300, epic_eos.renpy_category,
            "Starting update flow for local user {} with Epic Accound {}".format(
                local_user_id_string.value,
                account_id_map[local_user_id_string.value],
                )
            )
        epic_account_token.contents.Release()

@cdefs.EOS_LogMessageFunc
def epic_logger(message):
    # type: (ctypes.POINTER(cdefs.EOS_LogMessage)) -> None
    """Logging callback provided to the SDK."""
    m = message.contents
    try:
        config.epic_logger(m.Level.value, bytes_to_str(m.Category), bytes_to_str(m.Message))
    except: # pylint: disable=bare-except
        print(f"500 {epic_eos.renpy_category} An error occured while logging a message.")
