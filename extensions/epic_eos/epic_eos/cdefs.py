from ctypes import (
    c_int32, c_int64, c_uint8, c_uint32, c_uint64,
    c_char_p, c_void_p, c_double, Structure,
    CFUNCTYPE, POINTER,)

try:
    from typing import Any
except ImportError:
    pass

def not_ready(*args): # type: (...) -> Any
    raise RuntimeError("Please call steamapi.load() before this function.")

# Alignement is statically enforced in the lib
PACK = 8

#####
# Commons
#####

# Base
class EOS_Bool(c_int32):
    pass
EOS_TRUE = EOS_Bool(1)
EOS_FALSE = EOS_Bool(0)

# Version
EOS_GetVersion = not_ready

# Common
class EOS_EResult(c_int32):
    def ToString(self):
        return EOS_EResult_ToString(self)
    def IsOperationComplete(self):
        return EOS_EResult_IsOperationComplete(self)
EOS_Success = EOS_EResult(0)
EOS_NoConnection = EOS_EResult(1)
EOS_InvalidCredentials = EOS_EResult(2)
EOS_InvalidUser = EOS_EResult(3)
EOS_InvalidAuth = EOS_EResult(4)
EOS_AccessDenied = EOS_EResult(5)
EOS_MissingPermissions = EOS_EResult(6)
EOS_Token_Not_Account = EOS_EResult(7)
EOS_TooManyRequests = EOS_EResult(8)
EOS_AlreadyPending = EOS_EResult(9)
EOS_InvalidParameters = EOS_EResult(10)
EOS_InvalidRequest = EOS_EResult(11)
EOS_UnrecognizedResponse = EOS_EResult(12)
EOS_IncompatibleVersion = EOS_EResult(13)
EOS_NotConfigured = EOS_EResult(14)
EOS_AlreadyConfigured = EOS_EResult(15)
EOS_NotImplemented = EOS_EResult(16)
EOS_Canceled = EOS_EResult(17)
EOS_NotFound = EOS_EResult(18)
EOS_OperationWillRetry = EOS_EResult(19)
EOS_NoChange = EOS_EResult(20)
EOS_VersionMismatch = EOS_EResult(21)
EOS_LimitExceeded = EOS_EResult(22)
EOS_Disabled = EOS_EResult(23)
EOS_DuplicateNotAllowed = EOS_EResult(24)
EOS_MissingParameters_DEPRECATED = EOS_EResult(25)
EOS_InvalidSandboxId = EOS_EResult(26)
EOS_TimedOut = EOS_EResult(27)
EOS_PartialResult = EOS_EResult(28)
EOS_Missing_Role = EOS_EResult(29)
EOS_Missing_Feature = EOS_EResult(30)
EOS_Invalid_Sandbox = EOS_EResult(31)
EOS_Invalid_Deployment = EOS_EResult(32)
EOS_Invalid_Product = EOS_EResult(33)
EOS_Invalid_ProductUserID = EOS_EResult(34)
EOS_ServiceFailure = EOS_EResult(35)
EOS_CacheDirectoryMissing = EOS_EResult(36)
EOS_CacheDirectoryInvalid = EOS_EResult(37)
EOS_InvalidState = EOS_EResult(38)
EOS_RequestInProgress = EOS_EResult(39)
EOS_ApplicationSuspended = EOS_EResult(40)
EOS_NetworkDisconnected = EOS_EResult(41)
EOS_Auth_AccountLocked = EOS_EResult(1001)
EOS_Auth_AccountLockedForUpdate = EOS_EResult(1002)
EOS_Auth_InvalidRefreshToken = EOS_EResult(1003)
EOS_Auth_InvalidToken = EOS_EResult(1004)
EOS_Auth_AuthenticationFailure = EOS_EResult(1005)
EOS_Auth_InvalidPlatformToken = EOS_EResult(1006)
EOS_Auth_WrongAccount = EOS_EResult(1007)
EOS_Auth_WrongClient = EOS_EResult(1008)
EOS_Auth_FullAccountRequired = EOS_EResult(1009)
EOS_Auth_HeadlessAccountRequired = EOS_EResult(1010)
EOS_Auth_PasswordResetRequired = EOS_EResult(1011)
EOS_Auth_PasswordCannotBeReused = EOS_EResult(1012)
EOS_Auth_Expired = EOS_EResult(1013)
EOS_Auth_ScopeConsentRequired = EOS_EResult(1014)
EOS_Auth_ApplicationNotFound = EOS_EResult(1015)
EOS_Auth_ScopeNotFound = EOS_EResult(1016)
EOS_Auth_AccountFeatureRestricted = EOS_EResult(1017)
EOS_Auth_AccountPortalLoadError = EOS_EResult(1018)
EOS_Auth_CorrectiveActionRequired = EOS_EResult(1019)
EOS_Auth_PinGrantCode = EOS_EResult(1020)
EOS_Auth_PinGrantExpired = EOS_EResult(1021)
EOS_Auth_PinGrantPending = EOS_EResult(1022)
EOS_Auth_ExternalAuthNotLinked = EOS_EResult(1030)
EOS_Auth_ExternalAuthRevoked = EOS_EResult(1032)
EOS_Auth_ExternalAuthInvalid = EOS_EResult(1033)
EOS_Auth_ExternalAuthRestricted = EOS_EResult(1034)
EOS_Auth_ExternalAuthCannotLogin = EOS_EResult(1035)
EOS_Auth_ExternalAuthExpired = EOS_EResult(1036)
EOS_Auth_ExternalAuthIsLastLoginType = EOS_EResult(1037)
EOS_Auth_ExchangeCodeNotFound = EOS_EResult(1040)
EOS_Auth_OriginatingExchangeCodeSessionExpired = EOS_EResult(1041)
EOS_Auth_AccountNotActive = EOS_EResult(1050)
EOS_Auth_MFARequired = EOS_EResult(1060)
EOS_Auth_ParentalControls = EOS_EResult(1070)
EOS_Auth_NoRealId = EOS_EResult(1080)
EOS_Friends_InviteAwaitingAcceptance = EOS_EResult(2000)
EOS_Friends_NoInvitation = EOS_EResult(2001)
EOS_Friends_AlreadyFriends = EOS_EResult(2003)
EOS_Friends_NotFriends = EOS_EResult(2004)
EOS_Friends_TargetUserTooManyInvites = EOS_EResult(2005)
EOS_Friends_LocalUserTooManyInvites = EOS_EResult(2006)
EOS_Friends_TargetUserFriendLimitExceeded = EOS_EResult(2007)
EOS_Friends_LocalUserFriendLimitExceeded = EOS_EResult(2008)
EOS_Presence_DataInvalid = EOS_EResult(3000)
EOS_Presence_DataLengthInvalid = EOS_EResult(3001)
EOS_Presence_DataKeyInvalid = EOS_EResult(3002)
EOS_Presence_DataKeyLengthInvalid = EOS_EResult(3003)
EOS_Presence_DataValueInvalid = EOS_EResult(3004)
EOS_Presence_DataValueLengthInvalid = EOS_EResult(3005)
EOS_Presence_RichTextInvalid = EOS_EResult(3006)
EOS_Presence_RichTextLengthInvalid = EOS_EResult(3007)
EOS_Presence_StatusInvalid = EOS_EResult(3008)
EOS_Ecom_EntitlementStale = EOS_EResult(4000)
EOS_Ecom_CatalogOfferStale = EOS_EResult(4001)
EOS_Ecom_CatalogItemStale = EOS_EResult(4002)
EOS_Ecom_CatalogOfferPriceInvalid = EOS_EResult(4003)
EOS_Ecom_CheckoutLoadError = EOS_EResult(4004)
EOS_Sessions_SessionInProgress = EOS_EResult(5000)
EOS_Sessions_TooManyPlayers = EOS_EResult(5001)
EOS_Sessions_NoPermission = EOS_EResult(5002)
EOS_Sessions_SessionAlreadyExists = EOS_EResult(5003)
EOS_Sessions_InvalidLock = EOS_EResult(5004)
EOS_Sessions_InvalidSession = EOS_EResult(5005)
EOS_Sessions_SandboxNotAllowed = EOS_EResult(5006)
EOS_Sessions_InviteFailed = EOS_EResult(5007)
EOS_Sessions_InviteNotFound = EOS_EResult(5008)
EOS_Sessions_UpsertNotAllowed = EOS_EResult(5009)
EOS_Sessions_AggregationFailed = EOS_EResult(5010)
EOS_Sessions_HostAtCapacity = EOS_EResult(5011)
EOS_Sessions_SandboxAtCapacity = EOS_EResult(5012)
EOS_Sessions_SessionNotAnonymous = EOS_EResult(5013)
EOS_Sessions_OutOfSync = EOS_EResult(5014)
EOS_Sessions_TooManyInvites = EOS_EResult(5015)
EOS_Sessions_PresenceSessionExists = EOS_EResult(5016)
EOS_Sessions_DeploymentAtCapacity = EOS_EResult(5017)
EOS_Sessions_NotAllowed = EOS_EResult(5018)
EOS_Sessions_PlayerSanctioned = EOS_EResult(5019)
EOS_PlayerDataStorage_FilenameInvalid = EOS_EResult(6000)
EOS_PlayerDataStorage_FilenameLengthInvalid = EOS_EResult(6001)
EOS_PlayerDataStorage_FilenameInvalidChars = EOS_EResult(6002)
EOS_PlayerDataStorage_FileSizeTooLarge = EOS_EResult(6003)
EOS_PlayerDataStorage_FileSizeInvalid = EOS_EResult(6004)
EOS_PlayerDataStorage_FileHandleInvalid = EOS_EResult(6005)
EOS_PlayerDataStorage_DataInvalid = EOS_EResult(6006)
EOS_PlayerDataStorage_DataLengthInvalid = EOS_EResult(6007)
EOS_PlayerDataStorage_StartIndexInvalid = EOS_EResult(6008)
EOS_PlayerDataStorage_RequestInProgress = EOS_EResult(6009)
EOS_PlayerDataStorage_UserThrottled = EOS_EResult(6010)
EOS_PlayerDataStorage_EncryptionKeyNotSet = EOS_EResult(6011)
EOS_PlayerDataStorage_UserErrorFromDataCallback = EOS_EResult(6012)
EOS_PlayerDataStorage_FileHeaderHasNewerVersion = EOS_EResult(6013)
EOS_PlayerDataStorage_FileCorrupted = EOS_EResult(6014)
EOS_Connect_ExternalTokenValidationFailed = EOS_EResult(7000)
EOS_Connect_UserAlreadyExists = EOS_EResult(7001)
EOS_Connect_AuthExpired = EOS_EResult(7002)
EOS_Connect_InvalidToken = EOS_EResult(7003)
EOS_Connect_UnsupportedTokenType = EOS_EResult(7004)
EOS_Connect_LinkAccountFailed = EOS_EResult(7005)
EOS_Connect_ExternalServiceUnavailable = EOS_EResult(7006)
EOS_Connect_ExternalServiceConfigurationFailure = EOS_EResult(7007)
EOS_Connect_LinkAccountFailedMissingNintendoIdAccount_DEPRECATED = EOS_EResult(7008)
EOS_UI_SocialOverlayLoadError = EOS_EResult(8000)
EOS_Lobby_NotOwner = EOS_EResult(9000)
EOS_Lobby_InvalidLock = EOS_EResult(9001)
EOS_Lobby_LobbyAlreadyExists = EOS_EResult(9002)
EOS_Lobby_SessionInProgress = EOS_EResult(9003)
EOS_Lobby_TooManyPlayers = EOS_EResult(9004)
EOS_Lobby_NoPermission = EOS_EResult(9005)
EOS_Lobby_InvalidSession = EOS_EResult(9006)
EOS_Lobby_SandboxNotAllowed = EOS_EResult(9007)
EOS_Lobby_InviteFailed = EOS_EResult(9008)
EOS_Lobby_InviteNotFound = EOS_EResult(9009)
EOS_Lobby_UpsertNotAllowed = EOS_EResult(9010)
EOS_Lobby_AggregationFailed = EOS_EResult(9011)
EOS_Lobby_HostAtCapacity = EOS_EResult(9012)
EOS_Lobby_SandboxAtCapacity = EOS_EResult(9013)
EOS_Lobby_TooManyInvites = EOS_EResult(9014)
EOS_Lobby_DeploymentAtCapacity = EOS_EResult(9015)
EOS_Lobby_NotAllowed = EOS_EResult(9016)
EOS_Lobby_MemberUpdateOnly = EOS_EResult(9017)
EOS_Lobby_PresenceLobbyExists = EOS_EResult(9018)
EOS_Lobby_VoiceNotEnabled = EOS_EResult(9019)
EOS_TitleStorage_UserErrorFromDataCallback = EOS_EResult(10000)
EOS_TitleStorage_EncryptionKeyNotSet = EOS_EResult(10001)
EOS_TitleStorage_FileCorrupted = EOS_EResult(10002)
EOS_TitleStorage_FileHeaderHasNewerVersion = EOS_EResult(10003)
EOS_Mods_ModSdkProcessIsAlreadyRunning = EOS_EResult(11000)
EOS_Mods_ModSdkCommandIsEmpty = EOS_EResult(11001)
EOS_Mods_ModSdkProcessCreationFailed = EOS_EResult(11002)
EOS_Mods_CriticalError = EOS_EResult(11003)
EOS_Mods_ToolInternalError = EOS_EResult(11004)
EOS_Mods_IPCFailure = EOS_EResult(11005)
EOS_Mods_InvalidIPCResponse = EOS_EResult(11006)
EOS_Mods_URILaunchFailure = EOS_EResult(11007)
EOS_Mods_ModIsNotInstalled = EOS_EResult(11008)
EOS_Mods_UserDoesNotOwnTheGame = EOS_EResult(11009)
EOS_Mods_OfferRequestByIdInvalidResult = EOS_EResult(11010)
EOS_Mods_CouldNotFindOffer = EOS_EResult(11011)
EOS_Mods_OfferRequestByIdFailure = EOS_EResult(11012)
EOS_Mods_PurchaseFailure = EOS_EResult(11013)
EOS_Mods_InvalidGameInstallInfo = EOS_EResult(11014)
EOS_Mods_CannotGetManifestLocation = EOS_EResult(11015)
EOS_Mods_UnsupportedOS = EOS_EResult(11016)
EOS_AntiCheat_ClientProtectionNotAvailable = EOS_EResult(12000)
EOS_AntiCheat_InvalidMode = EOS_EResult(12001)
EOS_AntiCheat_ClientProductIdMismatch = EOS_EResult(12002)
EOS_AntiCheat_ClientSandboxIdMismatch = EOS_EResult(12003)
EOS_AntiCheat_ProtectMessageSessionKeyRequired = EOS_EResult(12004)
EOS_AntiCheat_ProtectMessageValidationFailed = EOS_EResult(12005)
EOS_AntiCheat_ProtectMessageInitializationFailed = EOS_EResult(12006)
EOS_AntiCheat_PeerAlreadyRegistered = EOS_EResult(12007)
EOS_AntiCheat_PeerNotFound = EOS_EResult(12008)
EOS_AntiCheat_PeerNotProtected = EOS_EResult(12009)
EOS_AntiCheat_ClientDeploymentIdMismatch = EOS_EResult(12010)
EOS_AntiCheat_DeviceIdAuthIsNotSupported = EOS_EResult(12011)
EOS_RTC_TooManyParticipants = EOS_EResult(13000)
EOS_RTC_RoomAlreadyExists = EOS_EResult(13001)
EOS_RTC_UserKicked = EOS_EResult(13002)
EOS_RTC_UserBanned = EOS_EResult(13003)
EOS_RTC_RoomWasLeft = EOS_EResult(13004)
EOS_RTC_ReconnectionTimegateExpired = EOS_EResult(13005)
EOS_RTC_ShutdownInvoked = EOS_EResult(13006)
EOS_RTC_UserIsInBlocklist = EOS_EResult(13007)
EOS_ProgressionSnapshot_SnapshotIdUnavailable = EOS_EResult(14000)
EOS_KWS_ParentEmailMissing = EOS_EResult(15000)
EOS_KWS_UserGraduated = EOS_EResult(15001)
EOS_Android_JavaVMNotStored = EOS_EResult(17000)
EOS_Permission_RequiredPatchAvailable = EOS_EResult(18000)
EOS_Permission_RequiredSystemUpdate = EOS_EResult(18001)
EOS_Permission_AgeRestrictionFailure = EOS_EResult(18002)
EOS_Permission_AccountTypeFailure = EOS_EResult(18003)
EOS_Permission_ChatRestriction = EOS_EResult(18004)
EOS_Permission_UGCRestriction = EOS_EResult(18005)
EOS_Permission_OnlinePlayRestricted = EOS_EResult(18006)
EOS_DesktopCrossplay_ApplicationNotBootstrapped = EOS_EResult(19000)
EOS_DesktopCrossplay_ServiceNotInstalled = EOS_EResult(19001)
EOS_DesktopCrossplay_ServiceStartFailed = EOS_EResult(19002)
EOS_DesktopCrossplay_ServiceNotRunning = EOS_EResult(19003)
EOS_UnexpectedError = EOS_EResult(0x7FFFFFFF)

EOS_EResult_ToString = not_ready
EOS_EResult_IsOperationComplete = not_ready
EOS_ByteArray_ToString = not_ready

class EOS_EpicAccountId(c_void_p):
    @staticmethod
    def FromString(AccountIdString):
        return EOS_EpicAccountId_FromString(AccountIdString)
    def ToString(self, OutBuffer, InOutBufferLength):
        return EOS_EpicAccountId_ToString(self, OutBuffer, InOutBufferLength)
    def IsValid(self):
        return EOS_EpicAccountId_IsValid(self)
EOS_EpicAccountId_IsValid = not_ready
EOS_EpicAccountId_ToString = not_ready
EOS_EpicAccountId_FromString = not_ready
EOS_EPICACCOUNTID_MAX_LENGTH = 32

class EOS_ProductUserId(c_void_p):
    @staticmethod
    def FromString(ProductUserIdString):
        return EOS_ProductUserId_FromString(ProductUserIdString)
    def ToString(self, OutBuffer, InOutBufferLength):
        return EOS_ProductUserId_ToString(self, OutBuffer, InOutBufferLength)
    def IsValid(self):
        return EOS_ProductUserId_IsValid(self)
EOS_ProductUserId_IsValid = not_ready
EOS_ProductUserId_ToString = not_ready
EOS_ProductUserId_FromString = not_ready
EOS_PRODUCTUSERID_MAX_LENGTH = 32

class EOS_NotificationId(c_uint64):
    pass
EOS_INVALID_NOTIFICATIONID = EOS_NotificationId(0)

class EOS_ContinuanceToken(c_void_p):
    def ToString(self, OutBuffer, InOutBufferLength):
        return EOS_ContinuanceToken_ToString(OutBuffer, InOutBufferLength)
EOS_ContinuanceToken_ToString = not_ready

EOS_PAGEQUERY_API_LATEST = 1
EOS_PAGINATION_API_LATEST = EOS_PAGEQUERY_API_LATEST
EOS_PAGEQUERY_MAXCOUNT_DEFAULT = 10
EOS_PAGEQUERY_MAXCOUNT_MAXIMUM = 100
class EOS_PageQuery(Structure):
    _pack_ = PACK
    _fields_ = [
    ('ApiVersion', c_int32),
    ('StartIndex', c_int32),
    ('MaxCount', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_PAGEQUERY_API_LATEST,
            StartIndex = 0, MaxCount = EOS_PAGEQUERY_MAXCOUNT_DEFAULT,
            **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, StartIndex = StartIndex,
            MaxCount = MaxCount, **kwargs)
class EOS_PageResult(Structure):
    _pack_ = PACK
    _fields_ = [
    ('StartIndex', c_int32),
    ('Count', c_int32),
    ('TotalCount', c_int32),
    ]

class EOS_ELoginStatus(c_int32):
    pass
EOS_LS_NotLoggedIn = EOS_ELoginStatus(0)
EOS_LS_UsingLocalProfile = EOS_ELoginStatus(1)
EOS_LS_LoggedIn = EOS_ELoginStatus(2)

class EOS_EAttributeType(c_int32):
    pass
EOS_AT_BOOLEAN = EOS_EAttributeType(0)
EOS_AT_INT64 = EOS_EAttributeType(1)
EOS_AT_DOUBLE = EOS_EAttributeType(2)
EOS_AT_STRING = EOS_EAttributeType(3)
EOS_ESessionAttributeType = EOS_EAttributeType
EOS_ELobbyAttributeType = EOS_EAttributeType

class EOS_EComparisonOp(c_int32):
    pass
EOS_CO_EQUAL = EOS_EComparisonOp(0)
EOS_CO_NOTEQUAL = EOS_EComparisonOp(1)
EOS_CO_GREATERTHAN = EOS_EComparisonOp(2)
EOS_CO_GREATERTHANOREQUAL = EOS_EComparisonOp(3)
EOS_CO_LESSTHAN = EOS_EComparisonOp(4)
EOS_CO_LESSTHANOREQUAL = EOS_EComparisonOp(5)
EOS_CO_DISTANCE = EOS_EComparisonOp(6)
EOS_CO_ANYOF = EOS_EComparisonOp(7)
EOS_CO_NOTANYOF = EOS_EComparisonOp(8)
EOS_CO_ONEOF = EOS_EComparisonOp(9)
EOS_CO_NOTONEOF = EOS_EComparisonOp(10)
EOS_CO_CONTAINS = EOS_EComparisonOp(11)
EOS_EOnlineComparisonOp = EOS_EComparisonOp

class EOS_EExternalAccountType(c_int32):
    pass
EOS_EAT_EPIC = EOS_EExternalAccountType(0)
EOS_EAT_STEAM = EOS_EExternalAccountType(1)
EOS_EAT_PSN = EOS_EExternalAccountType(2)
EOS_EAT_XBL = EOS_EExternalAccountType(3)
EOS_EAT_DISCORD = EOS_EExternalAccountType(4)
EOS_EAT_GOG = EOS_EExternalAccountType(5)
EOS_EAT_NINTENDO = EOS_EExternalAccountType(6)
EOS_EAT_UPLAY = EOS_EExternalAccountType(7)
EOS_EAT_OPENID = EOS_EExternalAccountType(8)
EOS_EAT_APPLE = EOS_EExternalAccountType(9)
EOS_EAT_GOOGLE = EOS_EExternalAccountType(10)
EOS_EAT_OCULUS = EOS_EExternalAccountType(11)
EOS_EAT_ITCHIO = EOS_EExternalAccountType(12)
EOS_EAT_AMAZON = EOS_EExternalAccountType(13)

class EOS_EExternalCredentialType(c_int32):
    pass
EOS_ECT_EPIC = EOS_EExternalCredentialType(0)
EOS_ECT_STEAM_APP_TICKET = EOS_EExternalCredentialType(1)
EOS_ECT_PSN_ID_TOKEN = EOS_EExternalCredentialType(2)
EOS_ECT_XBL_XSTS_TOKEN = EOS_EExternalCredentialType(3)
EOS_ECT_DISCORD_ACCESS_TOKEN = EOS_EExternalCredentialType(4)
EOS_ECT_GOG_SESSION_TICKET = EOS_EExternalCredentialType(5)
EOS_ECT_NINTENDO_ID_TOKEN = EOS_EExternalCredentialType(6)
EOS_ECT_NINTENDO_NSA_ID_TOKEN = EOS_EExternalCredentialType(7)
EOS_ECT_UPLAY_ACCESS_TOKEN = EOS_EExternalCredentialType(8)
EOS_ECT_OPENID_ACCESS_TOKEN = EOS_EExternalCredentialType(9)
EOS_ECT_DEVICEID_ACCESS_TOKEN = EOS_EExternalCredentialType(10)
EOS_ECT_APPLE_ID_TOKEN = EOS_EExternalCredentialType(11)
EOS_ECT_GOOGLE_ID_TOKEN = EOS_EExternalCredentialType(12)
EOS_ECT_OCULUS_USERID_NONCE = EOS_EExternalCredentialType(13)
EOS_ECT_ITCHIO_JWT = EOS_EExternalCredentialType(14)
EOS_ECT_ITCHIO_KEY = EOS_EExternalCredentialType(15)
EOS_ECT_EPIC_ID_TOKEN = EOS_EExternalCredentialType(16)
EOS_ECT_AMAZON_ACCESS_TOKEN = EOS_EExternalCredentialType(17)
EOS_ECT_STEAM_SESSION_TICKET = EOS_EExternalCredentialType(18)

EOS_IntegratedPlatformType = c_char_p
EOS_IPT_Unknown = c_char_p(None)

# Integrated Platform types
class EOS_HIntegratedPlatformOptionsContainer(c_void_p):
    pass

# Global types
class EOS_Platform_ClientCredentials(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientId', c_char_p),
        ('ClientSecret', c_char_p),
    ]
    def __init__(self, ClientId = None, ClientSecret = None, **kwargs):
        Structure.__init__(self,
            ClientId = ClientId, ClientSecret = ClientSecret,
            **kwargs)

EOS_PLATFORM_RTCOPTIONS_API_LATEST = 1
class EOS_Platform_RTCOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('PlatformSpecificOptions', c_void_p),
    ]
    def __init__(self,
            ApiVersion = EOS_PLATFORM_RTCOPTIONS_API_LATEST,
            PlatformSpecificOptions = None,
            **kwargs):
        Structure.__init__(
            self, ApiVersion = ApiVersion,
            PlatformSpecificOptions = PlatformSpecificOptions, **kwargs)
    
EOS_COUNTRYCODE_MAX_LENGTH = 4
EOS_COUNTRYCODE_MAX_BUFFER_LEN = (EOS_COUNTRYCODE_MAX_LENGTH + 1)
EOS_LOCALECODE_MAX_LENGTH = 9
EOS_LOCALECODE_MAX_BUFFER_LEN = (EOS_LOCALECODE_MAX_LENGTH + 1)
EOS_PLATFORM_OPTIONS_API_LATEST = 12

EOS_PF_LOADING_IN_EDITOR = 0x00001
EOS_PF_DISABLE_OVERLAY = 0x00002
EOS_PF_DISABLE_SOCIAL_OVERLAY = 0x00004
EOS_PF_RESERVED1 = 0x00008
EOS_PF_WINDOWS_ENABLE_OVERLAY_D3D9 = 0x00010
EOS_PF_WINDOWS_ENABLE_OVERLAY_D3D10 = 0x00020
EOS_PF_WINDOWS_ENABLE_OVERLAY_OPENGL = 0x00040

class EOS_Platform_Options(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Reserved', c_void_p),
        ('ProductId', c_char_p),
        ('SandboxId', c_char_p),
        ('ClientCredentials', EOS_Platform_ClientCredentials),
        ('bIsServer', EOS_Bool),
        ('EncryptionKey', c_char_p),
        ('OverrideCountryCode', c_char_p),
        ('OverrideLocaleCode', c_char_p),
        ('DeploymentId', c_char_p),
        ('Flags', c_uint64),
        ('CacheDirectory', c_char_p),
        ('TickBudgetInMilliseconds', c_uint32),
        ('RTCOptions', POINTER(EOS_Platform_RTCOptions)),
        ('IntegratedPlatformOptionsContainerHandle', EOS_HIntegratedPlatformOptionsContainer),
    ]
    def __init__(self,
            ApiVersion = EOS_PLATFORM_OPTIONS_API_LATEST, Reserved = None,
            ProductId = None, SandboxId = None, ClientCredentials = EOS_Platform_ClientCredentials(),
            bIsServer = False, EncryptionKey = None, OverrideCountryCode = None,
            OverrideLocaleCode = None, CacheDirectory = None, TickBudgetInMilliseconds = 0,
            RTCOptions = None, IntegratedPlatformOptionsContainerHandle = None, **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, Reserved = Reserved,
            ProductId = ProductId, SandboxId = SandboxId,
            ClientCredentials = ClientCredentials, bIsServer = bIsServer,
            EncryptionKey = EncryptionKey, OverrideCountryCode = OverrideCountryCode,
            OverrideLocaleCode = OverrideLocaleCode, CacheDirectory = CacheDirectory,
            TickBudgetInMilliseconds = TickBudgetInMilliseconds, RTCOptions = RTCOptions,
            IntegratedPlatformOptionsContainerHandle = IntegratedPlatformOptionsContainerHandle,
            **kwargs)

class EOS_EApplicationStatus(c_int32):
    pass
EOS_AS_BackgroundConstrained = EOS_EApplicationStatus(0)
EOS_AS_BackgroundUnconstrained = EOS_EApplicationStatus(1)
EOS_AS_BackgroundSuspended = EOS_EApplicationStatus(2)
EOS_AS_Foreground = EOS_EApplicationStatus(3)

class EOS_ENetworkStatus(c_int32):
    pass
EOS_NS_Disabled = EOS_ENetworkStatus(0)
EOS_NS_Offline = EOS_ENetworkStatus(1)
EOS_NS_Online = EOS_ENetworkStatus(2)

class EOS_EDesktopCrossplayStatus(c_int32):
    pass
EOS_DCS_OK = EOS_EDesktopCrossplayStatus(0)
EOS_DCS_ApplicationNotBootstrapped = EOS_EDesktopCrossplayStatus(1)
EOS_DCS_ServiceNotInstalled = EOS_EDesktopCrossplayStatus(2)
EOS_DCS_ServiceStartFailed = EOS_EDesktopCrossplayStatus(3)
EOS_DCS_ServiceNotRunning = EOS_EDesktopCrossplayStatus(4)
EOS_DCS_OverlayDisabled = EOS_EDesktopCrossplayStatus(5)
EOS_DCS_OverlayNotInstalled = EOS_EDesktopCrossplayStatus(6)
EOS_DCS_OverlayTrustCheckFailed = EOS_EDesktopCrossplayStatus(7)
EOS_DCS_OverlayLoadFailed = EOS_EDesktopCrossplayStatus(8)

EOS_PLATFORM_GETDESKTOPCROSSPLAYSTATUS_API_LATEST = 1

class EOS_Platform_GetDesktopCrossplayStatusOptions(Structure):
    _pack_ = PACK
    _fields_ = [('ApiVersion', c_int32)]
    def __init__(self,
            ApiVersion = EOS_PLATFORM_GETDESKTOPCROSSPLAYSTATUS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

class EOS_Platform_GetDesktopCrossplayStatusInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('Status', EOS_EDesktopCrossplayStatus),
        ('ServiceInitResult', c_int32),
    ]

#####
# Logging
#####

# Logging types

class EOS_ELogLevel(c_int32):
    pass
EOS_LOG_Off = EOS_ELogLevel(0)
EOS_LOG_Fatal = EOS_ELogLevel(100)
EOS_LOG_Error = EOS_ELogLevel(200)
EOS_LOG_Warning = EOS_ELogLevel(300)
EOS_LOG_Info = EOS_ELogLevel(400)
EOS_LOG_Verbose = EOS_ELogLevel(500)
EOS_LOG_VeryVerbose = EOS_ELogLevel(600)

class EOS_ELogCategory(c_int32):
    pass
EOS_LC_Core = EOS_ELogCategory(0)
EOS_LC_Auth = EOS_ELogCategory(1)
EOS_LC_Friends = EOS_ELogCategory(2)
EOS_LC_Presence = EOS_ELogCategory(3)
EOS_LC_UserInfo = EOS_ELogCategory(4)
EOS_LC_HttpSerialization = EOS_ELogCategory(5)
EOS_LC_Ecom = EOS_ELogCategory(6)
EOS_LC_P2P = EOS_ELogCategory(7)
EOS_LC_Sessions = EOS_ELogCategory(8)
EOS_LC_RateLimiter = EOS_ELogCategory(9)
EOS_LC_PlayerDataStorage = EOS_ELogCategory(10)
EOS_LC_Analytics = EOS_ELogCategory(11)
EOS_LC_Messaging = EOS_ELogCategory(12)
EOS_LC_Connect = EOS_ELogCategory(13)
EOS_LC_Overlay = EOS_ELogCategory(14)
EOS_LC_Achievements = EOS_ELogCategory(15)
EOS_LC_Stats = EOS_ELogCategory(16)
EOS_LC_UI = EOS_ELogCategory(17)
EOS_LC_Lobby = EOS_ELogCategory(18)
EOS_LC_Leaderboards = EOS_ELogCategory(19)
EOS_LC_Keychain = EOS_ELogCategory(20)
EOS_LC_IntegratedPlatform = EOS_ELogCategory(21)
EOS_LC_TitleStorage = EOS_ELogCategory(22)
EOS_LC_Mods = EOS_ELogCategory(23)
EOS_LC_AntiCheat = EOS_ELogCategory(24)
EOS_LC_Reports = EOS_ELogCategory(25)
EOS_LC_Sanctions = EOS_ELogCategory(26)
EOS_LC_ProgressionSnapshots = EOS_ELogCategory(27)
EOS_LC_KWS = EOS_ELogCategory(28)
EOS_LC_RTC = EOS_ELogCategory(29)
EOS_LC_RTCAdmin = EOS_ELogCategory(30)
EOS_LC_CustomInvites = EOS_ELogCategory(31)
EOS_LC_ALL_CATEGORIES = EOS_ELogCategory(0x7fffffff)

class EOS_LogMessage(Structure):
    _pack_ = PACK
    _fields_ = [
        ('Category', c_char_p),
        ('Message', c_char_p),
        ('Level', EOS_ELogLevel),
    ]

EOS_LogMessageFunc = CFUNCTYPE(
    None, POINTER(EOS_LogMessage))

EOS_Logging_SetCallback = not_ready
EOS_Logging_SetLogLevel = not_ready

#####
# Init
#####

# Init types
class EOS_AllocateMemoryFunc(c_void_p):
    # Not the actual signature
    pass
class EOS_ReallocateMemoryFunc(c_void_p):
    # Not the actual signature
    pass
class EOS_ReleaseMemoryFunc(c_void_p):
    # Not the actual signature
    pass


EOS_INITIALIZE_THREADAFFINITY_API_LATEST = 2
class EOS_Initialize_ThreadAffinity(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('NetworkWork', c_uint64),
        ('StorageIo', c_uint64),
        ('WebSocketIo', c_uint64),
        ('P2PIo', c_uint64),
        ('HttpRequestIo', c_uint64),
        ('RTCIo', c_uint64),
    ]
    def __init__(self,
            ApiVersion = EOS_INITIALIZE_THREADAFFINITY_API_LATEST,
            NetworkWork = 0, StorageIo = 0, WebSocketIo = 0, P2PIo = 0,
            HttpRequestIo = 0, RTCIo = 0, **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, NetworkWork = NetworkWork, StorageIo = StorageIo,
            WebSocketIo = WebSocketIo, P2PIo = P2PIo, HttpRequestIo = HttpRequestIo,
            RTCIo = RTCIo, **kwargs)

EOS_INITIALIZE_API_LATEST = 4
class EOS_InitializeOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AllocateMemoryFunction', EOS_AllocateMemoryFunc),
        ('ReallocateMemoryFunction', EOS_ReallocateMemoryFunc),
        ('ReleaseMemoryFunction', EOS_ReleaseMemoryFunc),
        ('ProductName', c_char_p),
        ('ProductVersion', c_char_p),
        ('Reserved', c_void_p),
        ('SystemInitializeOptions', c_void_p),
        ('OverrideThreadAffinity', POINTER(EOS_Initialize_ThreadAffinity)),
    ]
    def __init__(self,
        ApiVersion = EOS_INITIALIZE_API_LATEST, AllocateMemoryFunction = None,
        ReallocateMemoryFunction = None, ReleaseMemoryFunction = None,
        Reserved = None, SystemInitializeOptions = None,
        OverrideThreadAffinity = None,
        **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, AllocateMemoryFunction = AllocateMemoryFunction,
            ReallocateMemoryFunction = ReallocateMemoryFunction, ReleaseMemoryFunction = ReleaseMemoryFunction,
            Reserved = Reserved, SystemInitializeOptions = SystemInitializeOptions,
            OverrideThreadAffinity = OverrideThreadAffinity,
            **kwargs)
EOS_Initialize = not_ready
EOS_Shutdown = not_ready
EOS_Platform_Create = not_ready
EOS_Platform_Release = not_ready

#####
# Achievements
#####

# Achievements types

EOS_ACHIEVEMENTS_QUERYDEFINITIONS_API_LATEST = c_int32(3)
class EOS_Achievements_QueryDefinitionsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('EpicUserId_DEPRECATED', EOS_EpicAccountId),
        ('HiddenAchievementIds_DEPRECATED', POINTER(c_char_p)),
        ('HiddenAchievementsCount_DEPRECATED', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_QUERYDEFINITIONS_API_LATEST,
            LocalUserId = None,
            EpicUserId_DEPRECATED = None, HiddenAchievementIds_DEPRECATED = None,
            HiddenAchievementsCount_DEPRECATED = 0,
            **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, LocalUserId = LocalUserId,
            EpicUserId_DEPRECATED = EpicUserId_DEPRECATED,
            HiddenAchievementIds_DEPRECATED = HiddenAchievementIds_DEPRECATED,
            HiddenAchievementsCount_DEPRECATED = HiddenAchievementsCount_DEPRECATED,
            **kwargs)

EOS_ACHIEVEMENTS_STATTHRESHOLDS_API_LATEST = c_int32(1)
EOS_ACHIEVEMENTS_STATTHRESHOLD_API_LATEST = EOS_ACHIEVEMENTS_STATTHRESHOLDS_API_LATEST
class EOS_Achievements_StatThresholds(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Name', c_char_p),
        ('Threshold', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_STATTHRESHOLDS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_PLAYERSTATINFO_API_LATEST = c_int32(1)
class EOS_Achievements_PlayerStatInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Name', c_char_p),
        ('CurrentValue', c_int32),
        ('ThresholdValue', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_PLAYERSTATINFO_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_DEFINITIONV2_API_LATEST = c_int32(2)
class EOS_Achievements_DefinitionV2(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
        ('UnlockedDisplayName', c_char_p),
        ('UnlockedDescription', c_char_p),
        ('LockedDisplayName', c_char_p),
        ('LockedDescription', c_char_p),
        ('FlavorText', c_char_p),
        ('UnlockedIconURL', c_char_p),
        ('LockedIconURL', c_char_p),
        ('bIsHidden', EOS_Bool),
        ('StatThresholdsCount', c_uint32),
        ('StatThresholds', POINTER(EOS_Achievements_StatThresholds))
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_DEFINITIONV2_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
    def Release(self):
        EOS_Achievements_DefinitionV2_Release(self)
EOS_Achievements_DefinitionV2_Release = not_ready

EOS_ACHIEVEMENTS_GETACHIEVEMENTDEFINITIONCOUNT_API_LATEST = c_int32(1)
class EOS_Achievements_GetAchievementDefinitionCountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_GETACHIEVEMENTDEFINITIONCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYINDEX_API_LATEST = c_int32(2)
EOS_ACHIEVEMENTS_COPYDEFINITIONV2BYINDEX_API_LATEST = EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYINDEX_API_LATEST
class EOS_Achievements_CopyAchievementDefinitionV2ByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementIndex', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYINDEX_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYACHIEVEMENTID_API_LATEST = c_int32(2)
EOS_ACHIEVEMENTS_COPYDEFINITIONV2BYACHIEVEMENTID_API_LATEST = EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYACHIEVEMENTID_API_LATEST
class EOS_Achievements_CopyAchievementDefinitionV2ByAchievementIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_COPYACHIEVEMENTDEFINITIONV2BYACHIEVEMENTID_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Achievements_OnQueryDefinitionsCompleteCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
    ]
EOS_Achievements_OnQueryDefinitionsCompleteCallback = CFUNCTYPE(
    None, POINTER(EOS_Achievements_OnQueryDefinitionsCompleteCallbackInfo))

EOS_ACHIEVEMENTS_QUERYPLAYERACHIEVEMENTS_API_LATEST = c_int32(2)
class EOS_Achievements_QueryPlayerAchievementsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('LocalUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_QUERYPLAYERACHIEVEMENTS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_ACHIEVEMENT_UNLOCKTIME_UNDEFINED = c_int32(-1)
EOS_ACHIEVEMENTS_PLAYERACHIEVEMENT_API_LATEST = c_int32(2)
class EOS_Achievements_PlayerAchievement(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
        ('Progress', c_double),
        ('UnlockTime', c_int64),
        ('StatInfoCount', c_int32),
        ('StatInfo', POINTER(EOS_Achievements_PlayerStatInfo)),
        ('DisplayName', c_char_p),
        ('Description', c_char_p),
        ('IconURL', c_char_p),
        ('FlavorText', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_PLAYERACHIEVEMENT_API_LATEST,
            UnlockTime = EOS_ACHIEVEMENTS_ACHIEVEMENT_UNLOCKTIME_UNDEFINED,
            IconURL = None, FlavorText = None,
            **kwargs):
        Structure.__init__(self,
            ApiVersion = ApiVersion, UnlockTime = UnlockTime,
            IconURL = IconURL, FlavorText = FlavorText,
            **kwargs)
    def Release(self):
        return EOS_Achievements_PlayerAchievement_Release(self)

EOS_ACHIEVEMENTS_GETPLAYERACHIEVEMENTCOUNT_API_LATEST = c_int32(1)
class EOS_Achievements_GetPlayerAchievementCountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_GETPLAYERACHIEVEMENTCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_COPYPLAYERACHIEVEMENTBYINDEX_API_LATEST = c_int32(2)
class EOS_Achievements_CopyPlayerAchievementByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('AchievementIndex', c_uint32),
        ('LocalUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_COPYPLAYERACHIEVEMENTBYINDEX_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_ACHIEVEMENTS_COPYPLAYERACHIEVEMENTBYACHIEVEMENTID_API_LATEST = c_int32(2)
class EOS_Achievements_CopyPlayerAchievementByAchievementIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('AchievementId', c_char_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_COPYPLAYERACHIEVEMENTBYACHIEVEMENTID_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_Achievements_PlayerAchievement_Release = not_ready

class EOS_Achievements_OnQueryPlayerAchievementsCompleteCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('UserId', EOS_ProductUserId),
    ]
EOS_Achievements_OnQueryPlayerAchievementsCompleteCallback = CFUNCTYPE(
    None, POINTER(EOS_Achievements_OnQueryPlayerAchievementsCompleteCallbackInfo))

EOS_ACHIEVEMENTS_UNLOCKACHIEVEMENTS_API_LATEST = c_int32(1)
class EOS_Achievements_UnlockAchievementsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserId', EOS_ProductUserId),
        ('AchievementIds', POINTER(c_char_p)),
        ('AchievementsCount', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_UNLOCKACHIEVEMENTS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Achievements_OnUnlockAchievementsCompleteCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('UserId', EOS_ProductUserId),
        ('AchievementsCount', c_uint32),
    ]
EOS_Achievements_OnUnlockAchievementsCompleteCallback = CFUNCTYPE(
    None, POINTER(EOS_Achievements_OnUnlockAchievementsCompleteCallbackInfo))

EOS_ACHIEVEMENTS_ADDNOTIFYACHIEVEMENTSUNLOCKEDV2_API_LATEST = c_int32(2)
class EOS_Achievements_AddNotifyAchievementsUnlockedV2Options(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_ACHIEVEMENTS_ADDNOTIFYACHIEVEMENTSUNLOCKEDV2_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Achievements_OnAchievementsUnlockedCallbackV2Info(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientData', c_void_p),
        ('UserId', EOS_ProductUserId),
        ('AchievementId', c_char_p),
        ('UnlockTime', c_int64),
    ]
EOS_Achievements_OnAchievementsUnlockedCallbackV2 = CFUNCTYPE(
    None, POINTER(EOS_Achievements_OnAchievementsUnlockedCallbackV2Info))

# DEPRECATED Achievements types

EOS_ACHIEVEMENTS_DEFINITION_API_LATEST = 1
class EOS_Achievements_Definition(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
        ('DisplayName', c_char_p),
        ('Description', c_char_p),
        ('LockedDisplayName', c_char_p),
        ('LockedDescription', c_char_p),
        ('HiddenDescription', c_char_p),
        ('CompletionDescription', c_char_p),
        ('UnlockedIconId', c_char_p),
        ('LockedIconId', c_char_p),
        ('bIsHidden', EOS_Bool),
        ('StatThresholdsCount', c_int32),
        ('StatThresholds', POINTER(EOS_Achievements_StatThresholds)),
    ]
    def Release(self):
        return EOS_Achievements_Definition_Release(self)
EOS_Achievements_Definition_Release = not_ready

EOS_ACHIEVEMENTS_COPYDEFINITIONBYINDEX_API_LATEST = 1
class EOS_Achievements_CopyAchievementDefinitionByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementIndex', c_uint32),
    ]

EOS_ACHIEVEMENTS_COPYDEFINITIONBYACHIEVEMENTID_API_LATEST = 1
class EOS_Achievements_CopyAchievementDefinitionByAchievementIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
    ]

EOS_ACHIEVEMENTS_UNLOCKEDACHIEVEMENT_API_LATEST = 1
class EOS_Achievements_UnlockedAchievement(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AchievementId', c_char_p),
        ('UnlockTime', c_int64),
    ]
    def Release(self):
        return EOS_Achievements_UnlockedAchievement_Release(self)

EOS_ACHIEVEMENTS_GETUNLOCKEDACHIEVEMENTCOUNT_API_LATEST = 1
class EOS_Achievements_GetUnlockedAchievementCountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserId', EOS_ProductUserId),
    ]

EOS_ACHIEVEMENTS_COPYUNLOCKEDACHIEVEMENTBYINDEX_API_LATEST = 1
class EOS_Achievements_CopyUnlockedAchievementByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserId', EOS_ProductUserId),
        ('AchievementIndex', c_uint32),
    ]

EOS_ACHIEVEMENTS_COPYUNLOCKEDACHIEVEMENTBYACHIEVEMENTID_API_LATEST = 1
class EOS_Achievements_CopyUnlockedAchievementByAchievementIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserId', EOS_ProductUserId),
        ('AchievementId', c_char_p),
    ]

EOS_ACHIEVEMENTS_ADDNOTIFYACHIEVEMENTSUNLOCKED_API_LATEST = 1
class EOS_Achievements_AddNotifyAchievementsUnlockedOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
class EOS_Achievements_OnAchievementsUnlockedCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientData', c_void_p),
        ('UserId', EOS_ProductUserId),
        ('AchievementsCount', c_uint32),
        ('AchievementIds', POINTER(c_char_p)),
    ]
EOS_Achievements_OnAchievementsUnlockedCallback = CFUNCTYPE(
    None, POINTER(EOS_Achievements_OnAchievementsUnlockedCallbackInfo))
EOS_Achievements_UnlockedAchievement_Release = not_ready

# Achievements functions

EOS_Achievements_QueryDefinitions = not_ready
EOS_Achievements_GetAchievementDefinitionCount = not_ready
EOS_Achievements_CopyAchievementDefinitionV2ByIndex = not_ready
EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId = not_ready
EOS_Achievements_QueryPlayerAchievements = not_ready
EOS_Achievements_GetPlayerAchievementCount = not_ready
EOS_Achievements_CopyPlayerAchievementByIndex = not_ready
EOS_Achievements_CopyPlayerAchievementByAchievementId = not_ready
EOS_Achievements_UnlockAchievements = not_ready
EOS_Achievements_AddNotifyAchievementsUnlockedV2 = not_ready
EOS_Achievements_RemoveNotifyAchievementsUnlocked = not_ready

# DEPRECATED Achievements functions

EOS_Achievements_CopyAchievementDefinitionByIndex = not_ready
EOS_Achievements_CopyAchievementDefinitionByAchievementId = not_ready
EOS_Achievements_GetUnlockedAchievementCount = not_ready
EOS_Achievements_CopyUnlockedAchievementByIndex = not_ready
EOS_Achievements_CopyUnlockedAchievementByAchievementId = not_ready
EOS_Achievements_AddNotifyAchievementsUnlocked = not_ready

#####
# Auth
#####

# Auth types

class EOS_ELoginCredentialType(c_int32):
    pass
EOS_LCT_Password = EOS_ELoginCredentialType(0)
EOS_LCT_ExchangeCode = EOS_ELoginCredentialType(1)
EOS_LCT_PersistentAuth = EOS_ELoginCredentialType(2)
EOS_LCT_DeviceCode = EOS_ELoginCredentialType(3)
EOS_LCT_Developer = EOS_ELoginCredentialType(4)
EOS_LCT_RefreshToken = EOS_ELoginCredentialType(5)
EOS_LCT_AccountPortal = EOS_ELoginCredentialType(6)
EOS_LCT_ExternalAuth = EOS_ELoginCredentialType(7)

EOS_AUTH_TOKEN_API_LATEST = 2
class EOS_EAuthTokenType(c_int32):
    pass
EOS_ATT_Client = EOS_EAuthTokenType(0)
EOS_ATT_User = EOS_EAuthTokenType(1)

class EOS_Auth_Token(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('App', c_char_p),
        ('ClientId', c_char_p),
        ('AccountId', EOS_EpicAccountId),
        ('AccessToken', c_char_p),
        ('ExpiresIn', c_double),
        ('ExpiresAt', c_char_p),
        ('AuthType', EOS_EAuthTokenType),
        ('RefreshToken', c_char_p),
        ('RefreshExpiresIn', c_double),
        ('RefreshExpiresAt', c_char_p),
    ]
    def __init__(self, ApiVersion = EOS_AUTH_TOKEN_API_LATEST, **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
    def Release(self):
        return EOS_Auth_Token_Release(self)
EOS_Auth_Token_Release = not_ready

EOS_AUTH_CREDENTIALS_API_LATEST = 3
class EOS_Auth_Credentials(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Id', c_char_p),
        ('Token', c_char_p),
        ('Type', EOS_ELoginCredentialType),
        ('SystemAuthCredentialsOptions', c_void_p),
        ('ExternalType', EOS_EExternalCredentialType),
    ]
    def __init__(self, ApiVersion = EOS_AUTH_CREDENTIALS_API_LATEST, **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_AUTH_PINGRANTINFO_API_LATEST = 2
class EOS_Auth_PinGrantInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('UserCode', c_char_p),
        ('VerificationURI', c_char_p),
        ('ExpiresIn', c_int32),
        ('VerificationURIComplete', c_char_p),
    ]
    def __init__(self, ApiVersion = EOS_AUTH_PINGRANTINFO_API_LATEST, **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_AUTH_ACCOUNTFEATURERESTRICTEDINFO_API_LATEST = 1
class EOS_Auth_AccountFeatureRestrictedInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('VerificationURI', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_ACCOUNTFEATURERESTRICTEDINFO_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

class EOS_EAuthScopeFlags(c_int32):
    pass
EOS_AS_NoFlags = EOS_EAuthScopeFlags(0x0)
EOS_AS_BasicProfile = EOS_EAuthScopeFlags(0x1)
EOS_AS_FriendsList = EOS_EAuthScopeFlags(0x2)
EOS_AS_Presence = EOS_EAuthScopeFlags(0x4)
EOS_AS_FriendsManagement = EOS_EAuthScopeFlags(0x8)
EOS_AS_Email = EOS_EAuthScopeFlags(0x10)
EOS_AS_Country = EOS_EAuthScopeFlags(0x20)

EOS_AUTH_LOGIN_API_LATEST = 2
class EOS_Auth_LoginOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Credentials', POINTER(EOS_Auth_Credentials)),
        ('ScopeFlags', EOS_EAuthScopeFlags),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_LOGIN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_LoginCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_EpicAccountId),
        ('PinGrantInfo', POINTER(EOS_Auth_PinGrantInfo)),
        ('ContinuanceToken', EOS_ContinuanceToken),
        ('AccountFeatureRestrictedInfo', POINTER(EOS_Auth_AccountFeatureRestrictedInfo)),
        ('SelectedAccountId', EOS_EpicAccountId),
    ]
EOS_Auth_OnLoginCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_LoginCallbackInfo))

EOS_AUTH_LOGOUT_API_LATEST = 1
class EOS_Auth_LogoutOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_EpicAccountId),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_LOGOUT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_LogoutCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_EpicAccountId),
    ]
EOS_Auth_OnLogoutCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_LogoutCallbackInfo))

class EOS_ELinkAccountFlags(c_int32):
    pass
EOS_LA_NoFlags = EOS_ELinkAccountFlags(0x0)
EOS_LA_NintendoNsaId = EOS_ELinkAccountFlags(0x1)

EOS_AUTH_LINKACCOUNT_API_LATEST = 1
class EOS_Auth_LinkAccountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LinkAccountFlags', EOS_ELinkAccountFlags),
        ('ContinuanceToken', EOS_ContinuanceToken),
        ('LocalUserId', EOS_EpicAccountId),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_LINKACCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_LinkAccountCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_EpicAccountId),
        ('PinGrantInfo', EOS_Auth_PinGrantInfo),
        ('SelectedAccountId', EOS_EpicAccountId),
    ]
EOS_Auth_OnLinkAccountCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_LinkAccountCallbackInfo))

EOS_AUTH_VERIFYUSERAUTH_API_LATEST = 1
class EOS_Auth_VerifyUserAuthOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AuthToken', POINTER(EOS_Auth_Token)),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_VERIFYUSERAUTH_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_VerifyUserAuthCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
    ]
EOS_Auth_OnVerifyUserAuthCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_VerifyUserAuthCallbackInfo))

EOS_AUTH_COPYUSERAUTHTOKEN_API_LATEST = 1
class EOS_Auth_CopyUserAuthTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_COPYUSERAUTHTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
EOS_AUTH_COPYIDTOKEN_API_LATEST = 1
class EOS_Auth_CopyIdTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AccountId', EOS_EpicAccountId),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_COPYIDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_AUTH_IDTOKEN_API_LATEST = 1
class EOS_Auth_IdToken(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('AccountId', EOS_EpicAccountId),
        ('JsonWebToken', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_IDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
    def Release(self):
        return EOS_Auth_IdToken_Release(self)
EOS_Auth_IdToken_Release = not_ready

EOS_AUTH_QUERYIDTOKEN_API_LATEST = 1
class EOS_Auth_QueryIdTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_EpicAccountId),
        ('TargetAccountId', EOS_EpicAccountId),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_QUERYIDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_QueryIdTokenCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_EpicAccountId),
        ('TargetAccountId', EOS_EpicAccountId),
    ]
EOS_Auth_OnQueryIdTokenCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_QueryIdTokenCallbackInfo))

EOS_AUTH_VERIFYIDTOKEN_API_LATEST = 1
class EOS_Auth_VerifyIdTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('IdToken', POINTER(EOS_Auth_IdToken)),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_VERIFYIDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Auth_VerifyIdTokenCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('ApplicationId', c_char_p),
        ('ClientId', c_char_p),
        ('ProductId', c_char_p),
        ('SandboxId', c_char_p),
        ('DeploymentId', c_char_p),
        ('DisplayName', c_char_p),
        ('bIsExternalAccountInfoPresent', EOS_Bool),
        ('ExternalAccountIdType', EOS_EExternalAccountType),
        ('ExternalAccountId', c_char_p),
        ('ExternalAccountDisplayName', c_char_p),
        ('Platform', c_char_p),
    ]
EOS_Auth_OnVerifyIdTokenCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_VerifyIdTokenCallbackInfo))

EOS_AUTH_ADDNOTIFYLOGINSTATUSCHANGED_API_LATEST = 1
class EOS_Auth_AddNotifyLoginStatusChangedOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_ADDNOTIFYLOGINSTATUSCHANGED_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_AUTH_DELETEPERSISTENTAUTH_API_LATEST = 2
class EOS_Auth_DeletePersistentAuthOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('RefreshToken', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_AUTH_DELETEPERSISTENTAUTH_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

class EOS_Auth_DeletePersistentAuthCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
    ]
EOS_Auth_OnDeletePersistentAuthCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_DeletePersistentAuthCallbackInfo))

class EOS_Auth_LoginStatusChangedCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_EpicAccountId),
        ('PrevStatus', EOS_ELoginStatus),
        ('CurrentStatus', EOS_ELoginStatus),
    ]
EOS_Auth_OnLoginStatusChangedCallback = CFUNCTYPE(
    None, POINTER(EOS_Auth_LoginStatusChangedCallbackInfo))

# Auth functions

EOS_Auth_Login = not_ready
EOS_Auth_Logout = not_ready
EOS_Auth_LinkAccount = not_ready
EOS_Auth_DeletePersistentAuth = not_ready
EOS_Auth_VerifyUserAuth = not_ready
EOS_Auth_GetLoggedInAccountsCount = not_ready
EOS_Auth_GetLoggedInAccountByIndex = not_ready
EOS_Auth_GetLoginStatus = not_ready
EOS_Auth_CopyUserAuthToken = not_ready
EOS_Auth_CopyIdToken = not_ready
EOS_Auth_QueryIdToken = not_ready
EOS_Auth_VerifyIdToken = not_ready
EOS_Auth_GetSelectedAccountId = not_ready
EOS_Auth_GetMergedAccountsCount = not_ready
EOS_Auth_GetMergedAccountByIndex = not_ready
EOS_Auth_AddNotifyLoginStatusChanged = not_ready
EOS_Auth_RemoveNotifyLoginStatusChanged = not_ready

#####
# Connect
#####

# Connect types

EOS_CONNECT_EXTERNAL_ACCOUNT_ID_MAX_LENGTH = 256
EOS_CONNECT_CREDENTIALS_API_LATEST = 1
class EOS_Connect_Credentials(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Token', c_char_p),
        ('Type', EOS_EExternalCredentialType),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_CREDENTIALS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_USERLOGININFO_DISPLAYNAME_MAX_LENGTH = 32
EOS_CONNECT_USERLOGININFO_API_LATEST = 1
class EOS_Connect_UserLoginInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('DisplayName', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_USERLOGININFO_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_LOGIN_API_LATEST = 2
class EOS_Connect_LoginOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Credentials', POINTER(EOS_Connect_Credentials)),
        ('UserLoginInfo', POINTER(EOS_Connect_UserLoginInfo)),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_LOGIN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_LoginCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
        ('ContinuanceToken', EOS_ContinuanceToken),
    ]
EOS_Connect_OnLoginCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_LoginCallbackInfo))

EOS_CONNECT_CREATEUSER_API_LATEST = 1
class EOS_Connect_CreateUserOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('ContinuanceToken', EOS_ContinuanceToken),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_CREATEUSER_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_CreateUserCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnCreateUserCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_CreateUserCallbackInfo))

EOS_CONNECT_LINKACCOUNT_API_LATEST = 1
class EOS_Connect_LinkAccountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('ContinuanceToken', EOS_ContinuanceToken),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_LINKACCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_LinkAccountCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnLinkAccountCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_LinkAccountCallbackInfo))

EOS_CONNECT_UNLINKACCOUNT_API_LATEST = 1
class EOS_Connect_UnlinkAccountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_UNLINKACCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_UnlinkAccountCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnUnlinkAccountCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_UnlinkAccountCallbackInfo))

EOS_CONNECT_CREATEDEVICEID_API_LATEST = 1
EOS_CONNECT_CREATEDEVICEID_DEVICEMODEL_MAX_LENGTH = 64
class EOS_Connect_CreateDeviceIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('DeviceModel', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_CREATEDEVICEID_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_CreateDeviceIdCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
    ]
EOS_Connect_OnCreateDeviceIdCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_CreateDeviceIdCallbackInfo))

EOS_CONNECT_DELETEDEVICEID_API_LATEST = 1
class EOS_Connect_DeleteDeviceIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_DELETEDEVICEID_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_DeleteDeviceIdCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
    ]
EOS_Connect_OnDeleteDeviceIdCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_DeleteDeviceIdCallbackInfo))

EOS_CONNECT_TRANSFERDEVICEIDACCOUNT_API_LATEST = 1
class EOS_Connect_TransferDeviceIdAccountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('PrimaryLocalUserId', EOS_ProductUserId),
        ('LocalDeviceUserId', EOS_ProductUserId),
        ('ProductUserIdToPreserve', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_TRANSFERDEVICEIDACCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_TransferDeviceIdAccountCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnTransferDeviceIdAccountCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_TransferDeviceIdAccountCallbackInfo))

EOS_CONNECT_QUERYEXTERNALACCOUNTMAPPINGS_API_LATEST = 1
EOS_CONNECT_QUERYEXTERNALACCOUNTMAPPINGS_MAX_ACCOUNT_IDS = 128
class EOS_Connect_QueryExternalAccountMappingsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('AccountIdType', EOS_EExternalAccountType),
        ('ExternalAccountIds', POINTER(c_char_p)),
        ('ExternalAccountIdCount', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_QUERYEXTERNALACCOUNTMAPPINGS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_QueryExternalAccountMappingsCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnQueryExternalAccountMappingsCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_QueryExternalAccountMappingsCallbackInfo))

EOS_CONNECT_GETEXTERNALACCOUNTMAPPING_API_LATEST = 1
EOS_CONNECT_GETEXTERNALACCOUNTMAPPINGS_API_LATEST = EOS_CONNECT_GETEXTERNALACCOUNTMAPPING_API_LATEST
class EOS_Connect_GetExternalAccountMappingsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('AccountIdType', EOS_EExternalAccountType),
        ('TargetExternalUserId', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_GETEXTERNALACCOUNTMAPPING_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_QUERYPRODUCTUSERIDMAPPINGS_API_LATEST = 2
class EOS_Connect_QueryProductUserIdMappingsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('AccountIdType_DEPRECATED', EOS_EExternalAccountType),
        ('ProductUserIds', POINTER(EOS_ProductUserId)),
        ('ProductUserIdCount', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_QUERYPRODUCTUSERIDMAPPINGS_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_QueryProductUserIdMappingsCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnQueryProductUserIdMappingsCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_QueryProductUserIdMappingsCallbackInfo))

EOS_CONNECT_GETPRODUCTUSERIDMAPPING_API_LATEST = 1
class EOS_Connect_GetProductUserIdMappingOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('AccountIdType', EOS_EExternalAccountType),
        ('TargetProductUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_GETPRODUCTUSERIDMAPPING_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_GETPRODUCTUSEREXTERNALACCOUNTCOUNT_API_LATEST = 1
class EOS_Connect_GetProductUserExternalAccountCountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_GETPRODUCTUSEREXTERNALACCOUNTCOUNT_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYINDEX_API_LATEST = 1
class EOS_Connect_CopyProductUserExternalAccountByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('ExternalAccountInfoIndex', c_uint32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYINDEX_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYACCOUNTTYPE_API_LATEST = 1
class EOS_Connect_CopyProductUserExternalAccountByAccountTypeOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('AccountIdType', EOS_EExternalAccountType),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYACCOUNTTYPE_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYACCOUNTID_API_LATEST = 1
class EOS_Connect_CopyProductUserExternalAccountByAccountIdOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('AccountId', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_COPYPRODUCTUSEREXTERNALACCOUNTBYACCOUNTID_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_COPYPRODUCTUSERINFO_API_LATEST = 1
class EOS_Connect_CopyProductUserInfoOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_COPYPRODUCTUSERINFO_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_TIME_UNDEFINED = -1
EOS_CONNECT_EXTERNALACCOUNTINFO_API_LATEST = 1
class EOS_Connect_ExternalAccountInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('ProductUserId', EOS_ProductUserId),
        ('DisplayName', c_char_p),
        ('AccountId', c_char_p),
        ('AccountIdType', EOS_EExternalAccountType),
        ('LastLoginTime', c_int64),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_EXTERNALACCOUNTINFO_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
    def Release(self): # type: () -> None
        return EOS_Connect_ExternalAccountInfo_Release(self)
EOS_Connect_ExternalAccountInfo_Release = not_ready

EOS_CONNECT_ADDNOTIFYAUTHEXPIRATION_API_LATEST = 1
class EOS_Connect_AddNotifyAuthExpirationOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_ADDNOTIFYAUTHEXPIRATION_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_ONAUTHEXPIRATIONCALLBACK_API_LATEST = 1 # deprecated
class EOS_Connect_AuthExpirationCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
    ]
EOS_Connect_OnAuthExpirationCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_AuthExpirationCallbackInfo))

EOS_CONNECT_ADDNOTIFYLOGINSTATUSCHANGED_API_LATEST = 1
class EOS_Connect_AddNotifyLoginStatusChangedOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_ADDNOTIFYLOGINSTATUSCHANGED_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_LoginStatusChangedCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
        ('PreviousStatus', EOS_ELoginStatus),
        ('CurrentStatus', EOS_ELoginStatus),
    ]
EOS_Connect_OnLoginStatusChangedCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_LoginStatusChangedCallbackInfo))

EOS_CONNECT_IDTOKEN_API_LATEST = 1
class EOS_Connect_IdToken(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('ProductUserId', EOS_ProductUserId),
        ('JsonWebToken', c_char_p),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_IDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
    def Release(self): # type: () -> None
        return EOS_Connect_IdToken_Release(self)
EOS_Connect_IdToken_Release = not_ready

EOS_CONNECT_COPYIDTOKEN_API_LATEST = 1
class EOS_Connect_CopyIdTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_COPYIDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)

EOS_CONNECT_VERIFYIDTOKEN_API_LATEST = 1
class EOS_Connect_VerifyIdTokenOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('IdToken', POINTER(EOS_Connect_IdToken)),
    ]
    def __init__(self,
            ApiVersion = EOS_CONNECT_VERIFYIDTOKEN_API_LATEST,
            **kwargs):
        Structure.__init__(self, ApiVersion = ApiVersion, **kwargs)
class EOS_Connect_VerifyIdTokenCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('ProductUserId', EOS_ProductUserId),
        ('bIsAccountInfoPresent', EOS_Bool),
        ('AccountIdType', EOS_EExternalAccountType),
        ('AccountId', c_char_p),
        ('Platform', c_char_p),
        ('DeviceType', c_char_p),
        ('ClientId', c_char_p),
        ('ProductId', c_char_p),
        ('SandboxId', c_char_p),
        ('DeploymentId', c_char_p),
    ]
EOS_Connect_OnVerifyIdTokenCallback = CFUNCTYPE(
    None, POINTER(EOS_Connect_VerifyIdTokenCallbackInfo))

# Connect functions

EOS_Connect_Login = not_ready
EOS_Connect_CreateUser = not_ready
EOS_Connect_LinkAccount = not_ready
EOS_Connect_UnlinkAccount = not_ready
EOS_Connect_CreateDeviceId = not_ready
EOS_Connect_DeleteDeviceId = not_ready
EOS_Connect_TransferDeviceIdAccount = not_ready
EOS_Connect_QueryExternalAccountMappings = not_ready
EOS_Connect_QueryProductUserIdMappings = not_ready
EOS_Connect_GetExternalAccountMapping = not_ready
EOS_Connect_GetProductUserIdMapping = not_ready
EOS_Connect_GetProductUserExternalAccountCount = not_ready
EOS_Connect_CopyProductUserExternalAccountByIndex = not_ready
EOS_Connect_CopyProductUserExternalAccountByAccountType = not_ready
EOS_Connect_CopyProductUserExternalAccountByAccountId = not_ready
EOS_Connect_CopyProductUserInfo = not_ready
EOS_Connect_GetLoggedInUsersCount = not_ready
EOS_Connect_GetLoggedInUserByIndex = not_ready
EOS_Connect_GetLoginStatus = not_ready
EOS_Connect_AddNotifyAuthExpiration = not_ready
EOS_Connect_RemoveNotifyAuthExpiration = not_ready
EOS_Connect_AddNotifyLoginStatusChanged = not_ready
EOS_Connect_RemoveNotifyLoginStatusChanged = not_ready
EOS_Connect_CopyIdToken = not_ready
EOS_Connect_VerifyIdToken = not_ready

#####
# Stats
#####

# Stats types

EOS_STATS_INGESTDATA_API_LATEST = 1
class EOS_Stats_IngestData(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('StatName', c_char_p),
        ('IngestAmount', c_int32),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_INGESTDATA_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)

EOS_STATS_MAX_INGEST_STATS = 3000
EOS_STATS_INGESTSTAT_API_LATEST = 3
class EOS_Stats_IngestStatOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('Stats', POINTER(EOS_Stats_IngestData)),
        ('StatsCount', c_uint32),
        ('TargetUserId', EOS_ProductUserId),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_INGESTSTAT_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)
class EOS_Stats_IngestStatCompleteCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
        ('TargetUserId', EOS_ProductUserId),
    ]
EOS_Stats_OnIngestStatCompleteCallback = CFUNCTYPE(
    None, POINTER(EOS_Stats_IngestStatCompleteCallbackInfo))

EOS_STATS_MAX_QUERY_STATS = 1000
EOS_STATS_QUERYSTATS_API_LATEST = 3
class EOS_Stats_QueryStatsOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('LocalUserId', EOS_ProductUserId),
        ('StartTime', c_int64),
        ('EndTime', c_int64),
        ('StatNames', POINTER(c_char_p)),
        ('StatNamesCount', c_uint32),
        ('TargetUserId', EOS_ProductUserId),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_QUERYSTATS_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)

EOS_STATS_TIME_UNDEFINED = -1
EOS_STATS_STAT_API_LATEST = 1
class EOS_Stats_Stat(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('Name', c_char_p),
        ('StartTime', c_int64),
        ('EndTime', c_int64),
        ('Value', c_int32),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_STAT_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)
    def Release(self):
        return EOS_Stats_Stat_Release(self)

EOS_STATS_GETSTATSCOUNT_API_LATEST = 1
EOS_STATS_GETSTATCOUNT_API_LATEST = EOS_STATS_GETSTATSCOUNT_API_LATEST
class EOS_Stats_GetStatCountOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_GETSTATSCOUNT_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)

EOS_STATS_COPYSTATBYINDEX_API_LATEST = 1
class EOS_Stats_CopyStatByIndexOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('StatIndex', c_uint32),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_COPYSTATBYINDEX_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)

EOS_STATS_COPYSTATBYNAME_API_LATEST = 1
class EOS_Stats_CopyStatByNameOptions(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ApiVersion', c_int32),
        ('TargetUserId', EOS_ProductUserId),
        ('Name', c_char_p),
    ]
    def __init__(self,
        ApiVersion = EOS_STATS_COPYSTATBYNAME_API_LATEST,
        **kwargs):
        Structure.__init__(self, ApiVersion, **kwargs)
EOS_Stats_Stat_Release = not_ready
class EOS_Stats_OnQueryStatsCompleteCallbackInfo(Structure):
    _pack_ = PACK
    _fields_ = [
        ('ResultCode', EOS_EResult),
        ('ClientData', c_void_p),
        ('LocalUserId', EOS_ProductUserId),
        ('TargetUserId', EOS_ProductUserId),
    ]
EOS_Stats_OnQueryStatsCompleteCallback = CFUNCTYPE(
    None, POINTER(EOS_Stats_OnQueryStatsCompleteCallbackInfo))

# Stats functions

EOS_Stats_IngestStat = not_ready
EOS_Stats_QueryStats = not_ready
EOS_Stats_GetStatsCount = not_ready
EOS_Stats_CopyStatByIndex = not_ready
EOS_Stats_CopyStatByName = not_ready

#####
# SDK
#####

# SDK functions

EOS_Platform_Tick = not_ready
EOS_Platform_GetMetricsInterface = not_ready
EOS_Platform_GetAuthInterface = not_ready
EOS_Platform_GetConnectInterface = not_ready
EOS_Platform_GetEcomInterface = not_ready
EOS_Platform_GetUIInterface = not_ready
EOS_Platform_GetFriendsInterface = not_ready
EOS_Platform_GetPresenceInterface = not_ready
EOS_Platform_GetSessionsInterface = not_ready
EOS_Platform_GetLobbyInterface = not_ready
EOS_Platform_GetUserInfoInterface = not_ready
EOS_Platform_GetP2PInterface = not_ready
EOS_Platform_GetRTCInterface = not_ready
EOS_Platform_GetRTCAdminInterface = not_ready
EOS_Platform_GetPlayerDataStorageInterface = not_ready
EOS_Platform_GetTitleStorageInterface = not_ready
EOS_Platform_GetAchievementsInterface = not_ready
EOS_Platform_GetStatsInterface = not_ready
EOS_Platform_GetLeaderboardsInterface = not_ready
EOS_Platform_GetModsInterface = not_ready
EOS_Platform_GetAntiCheatClientInterface = not_ready
EOS_Platform_GetAntiCheatServerInterface = not_ready
EOS_Platform_GetProgressionSnapshotInterface = not_ready
EOS_Platform_GetReportsInterface = not_ready
EOS_Platform_GetSanctionsInterface = not_ready
EOS_Platform_GetKWSInterface = not_ready
EOS_Platform_GetCustomInvitesInterface = not_ready
EOS_Platform_GetActiveCountryCode = not_ready
EOS_Platform_GetActiveLocaleCode = not_ready
EOS_Platform_GetOverrideCountryCode = not_ready
EOS_Platform_GetOverrideLocaleCode = not_ready
EOS_Platform_SetOverrideCountryCode = not_ready
EOS_Platform_SetOverrideLocaleCode = not_ready
EOS_Platform_CheckForLauncherAndRestart = not_ready
EOS_Platform_GetDesktopCrossplayStatus = not_ready
EOS_Platform_SetApplicationStatus = not_ready
EOS_Platform_GetApplicationStatus = not_ready
EOS_Platform_SetNetworkStatus = not_ready
EOS_Platform_GetNetworkStatus = not_ready

# SDK handle wrappers for exposed functions

class EOS_HPlatform(c_void_p):
    @staticmethod
    def Create(Options):
        # type: (POINTER(EOS_Platform_Options)) -> EOS_HPlatform
        return EOS_Platform_Create(Options)
    def Release(self): # type: () -> None
        return EOS_Platform_Release(self)
    def GetAchievementsInterface(self): # type: () -> EOS_HAchievements
        return EOS_Platform_GetAchievementsInterface(self)
    def GetApplicationStatus(self): # type: () -> EOS_EApplicationStatus
        return EOS_Platform_GetApplicationStatus(self)
    def GetAuthInterface(self): # type: () -> EOS_HAuth
        return EOS_Platform_GetAuthInterface(self)
    def GetConnectInterface(self): # type: () -> EOS_HConnect
        return EOS_Platform_GetConnectInterface(self)
    def GetDesktopCrossplayStatus(self, Options, OutDesktopCrossplayStatusInfo):
        # type: (POINTER(EOS_Platform_GetDesktopCrossplayStatusOptions), POINTER(EOS_Platform_GetDesktopCrossplayStatusInfo)) -> EOS_EResult
        return EOS_Platform_GetDesktopCrossplayStatus(self, Options, OutDesktopCrossplayStatusInfo)
    def GetUserInfoInterface(self): # type: () -> EOS_HUserInfo
        return EOS_Platform_GetUserInfoInterface(self)
    def GetStatsInterface(self): # type: () -> EOS_HStats
        return EOS_Platform_GetStatsInterface(self)
    def Tick(self): # type: () -> None
        return EOS_Platform_Tick(self)

class EOS_HAchievements(c_void_p):
    def AddNotifyAchievementsUnlockedV2(self, Options, ClientData, NotificationFn):
        # type: (POINTER(EOS_Achievements_AddNotifyAchievementsUnlockedV2Options), c_void_p, EOS_Achievements_OnAchievementsUnlockedCallbackV2) -> EOS_NotificationId
        return EOS_Achievements_AddNotifyAchievementsUnlockedV2(self, Options, ClientData, NotificationFn)
    def CopyAchievementDefinitionV2ByAchievementId(self, Options, OutDefinition):
        # type: (POINTER(EOS_Achievements_CopyAchievementDefinitionV2ByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_DefinitionV2))) -> EOS_EResult
        return EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId(self, Options, OutDefinition)
    def CopyAchievementDefinitionV2ByIndex(self, Options, OutDefinition):
        # type: (POINTER(EOS_Achievements_CopyAchievementDefinitionV2ByIndexOptions), POINTER(POINTER(EOS_Achievements_DefinitionV2))) -> EOS_EResult
        return EOS_Achievements_CopyAchievementDefinitionV2ByIndex(self, Options, OutDefinition)
    def CopyPlayerAchievementByAchievementId(self, Options, OutAchievement):
        # type: (POINTER(EOS_Achievements_CopyPlayerAchievementByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_PlayerAchievement))) -> EOS_EResult
        return EOS_Achievements_CopyPlayerAchievementByAchievementId(self, Options, OutAchievement)
    def CopyPlayerAchievementByIndex(self, Options, OutAchievement):
        # type: (POINTER(EOS_Achievements_CopyPlayerAchievementByIndexOptions), POINTER(POINTER(EOS_Achievements_PlayerAchievement))) -> EOS_EResult
        return EOS_Achievements_CopyPlayerAchievementByIndex(self, Options, OutAchievement)
    def GetAchievementDefinitionCount(self, Options):
        # type: (POINTER(EOS_Achievements_GetAchievementDefinitionCountOptions)) -> c_uint32
        return EOS_Achievements_GetAchievementDefinitionCount(self, Options)
    def GetPlayerAchievementCount(self, Options):
        # type: (POINTER(EOS_Achievements_GetPlayerAchievementCountOptions)) -> c_uint32
        return EOS_Achievements_GetPlayerAchievementCount(self, Options)
    def QueryDefinitions(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Achievements_QueryDefinitionsOptions), c_void_p, EOS_Achievements_OnQueryDefinitionsCompleteCallback) -> EOS_EResult
        return EOS_Achievements_QueryDefinitions(self, Options, ClientData, CompletionDelegate)
    def QueryPlayerAchievements(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Achievements_QueryPlayerAchievementsOptions), c_void_p, EOS_Achievements_OnQueryPlayerAchievementsCompleteCallback) -> EOS_EResult
        return EOS_Achievements_QueryPlayerAchievements(self, Options, ClientData, CompletionDelegate)
    def RemoveNotifyAchievementsUnlocked(self, InId):
        # type: (EOS_NotificationId) -> None
        return EOS_Achievements_RemoveNotifyAchievementsUnlocked(self, InId)
    def UnlockAchievements(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Achievements_UnlockAchievementsOptions), c_void_p, EOS_Achievements_OnUnlockAchievementsCompleteCallback) -> EOS_EResult
        return EOS_Achievements_UnlockAchievements(self, Options, ClientData, CompletionDelegate)

class EOS_HAuth(c_void_p):
    def AddNotifyLoginStatusChanged(self, Options, ClientData, Notification):
        # type: (POINTER(EOS_Auth_AddNotifyLoginStatusChangedOptions), c_void_p, EOS_Auth_OnLoginStatusChangedCallback) -> EOS_NotificationId
        return EOS_Auth_AddNotifyLoginStatusChanged(self, Options, ClientData, Notification)
    def CopyIdToken(self, Options, OutIdToken):
        # type: (POINTER(EOS_Auth_CopyIdTokenOptions), POINTER(POINTER(EOS_Auth_IdToken))) -> EOS_EResult
        return EOS_Auth_CopyIdToken(self, Options, OutIdToken)
    def CopyUserAuthToken(self, Options, LocalUserId, OutUserAuthToken):
        # type: (POINTER(EOS_Auth_CopyUserAuthTokenOptions), EOS_EpicAccountId, POINTER(POINTER(EOS_Auth_Token))) -> EOS_EResult
        return EOS_Auth_CopyUserAuthToken(self, Options, LocalUserId, OutUserAuthToken)
    def DeletePersistentAuth(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_DeletePersistentAuthOptions), c_void_p, EOS_Auth_OnDeletePersistentAuthCallback) -> None
        return EOS_Auth_DeletePersistentAuth(self, Options, ClientData, CompletionDelegate)
    def GetLoggedInAccountByIndex(self, Index):
        # type: (c_int32) -> EOS_EpicAccountId
        return EOS_Auth_GetLoggedInAccountByIndex(self, Index)
    def GetLoggedInAccountsCount(self):
        # type: () -> c_uint32
        return EOS_Auth_GetLoggedInAccountsCount(self)
    def GetLoginStatus(self, LocalUserId):
        # type: (EOS_EpicAccountId) -> EOS_ELoginStatus
        return EOS_Auth_GetLoginStatus(self, LocalUserId)
    def GetMergedAccountByIndex(self, LocalUserId, Index):
        # type: (EOS_EpicAccountId, c_uint32) -> EOS_EpicAccountId
        return EOS_Auth_GetMergedAccountByIndex(self, LocalUserId, Index)
    def GetMergedAccountsCount(self, LocalUserId):
        # type: (EOS_EpicAccountId) -> c_uint32
        return EOS_Auth_GetMergedAccountsCount(self, LocalUserId)
    def GetSelectedAccountId(self, LocalUserId, OutSelectedAccoundId):
        # type: (EOS_EpicAccountId, POINTER(EOS_EpicAccountId)) -> EOS_EResult
        return EOS_Auth_GetSelectedAccountId(self, LocalUserId, OutSelectedAccoundId)
    def LinkAccount(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_LinkAccountOptions), c_void_p, EOS_Auth_OnLinkAccountCallback) -> None
        return EOS_Auth_LinkAccount(self, Options, ClientData, CompletionDelegate)
    def Login(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_LoginOptions), c_void_p, EOS_Auth_OnLoginCallback) -> None
        return EOS_Auth_Login(self, Options, ClientData, CompletionDelegate)
    def Logout(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_LogoutOptions), c_void_p, EOS_Auth_OnLogoutCallback) -> None
        return EOS_Auth_Logout(self, Options, ClientData, CompletionDelegate)
    def QueryIdToken(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_QueryIdTokenOptions), c_void_p, EOS_Auth_OnQueryIdTokenCallback) -> None
        return EOS_Auth_QueryIdToken(self, Options, ClientData, CompletionDelegate)
    def RemoveNotifyLoginStatusChanged(self, InId):
        # type: (EOS_NotificationId) -> None
        return EOS_Auth_RemoveNotifyLoginStatusChanged(self, InId)
    def VerifyIdToken(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_VerifyIdTokenOptions), c_void_p, EOS_Auth_OnVerifyIdTokenCallback) -> None
        return EOS_Auth_VerifyIdToken(self, Options, ClientData, CompletionDelegate)
    def VerifyUserAuth(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Auth_VerifyUserAuthOptions), c_void_p, EOS_Auth_OnVerifyUserAuthCallback) -> None
        return EOS_Auth_VerifyUserAuth(self, Options, ClientData, CompletionDelegate)

class EOS_HConnect(c_void_p):
    def AddNotifyAuthExpiration(self, Options, ClientData, Notification):
        # type: (POINTER(EOS_Connect_AddNotifyAuthExpirationOptions), c_void_p, EOS_Connect_OnAuthExpirationCallback) -> EOS_NotificationId
        return EOS_Connect_AddNotifyAuthExpiration(self, Options, ClientData, Notification)
    def AddNotifyLoginStatusChanged(self, Options, ClientData, Notification):
        # type: (POINTER(EOS_Connect_AddNotifyLoginStatusChangedOptions), c_void_p, EOS_Connect_OnLoginStatusChangedCallback) -> EOS_NotificationId
        return EOS_Connect_AddNotifyLoginStatusChanged(self, Options, ClientData, Notification)
    def CopyIdToken(self, Options, OutIdToken):
        # type: (POINTER(EOS_Connect_CopyIdTokenOptions), POINTER(POINTER(EOS_Connect_IdToken))) -> EOS_EResult
        return EOS_Connect_CopyIdToken(self, Options, OutIdToken)
    def CopyProductUserExternalAccountByAccountId(self, Options, OutExternalAccountInfo):
        # type: (POINTER(EOS_Connect_CopyProductUserExternalAccountByAccountIdOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))) -> EOS_EResult
        return EOS_Connect_CopyProductUserExternalAccountByAccountId(self, Options, OutExternalAccountInfo)
    def CopyProductUserExternalAccountByAccountType(self, Options, OutExternalAccountInfo):
        # type: (POINTER(EOS_Connect_CopyProductUserExternalAccountByAccountTypeOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))) -> EOS_EResult
        return EOS_Connect_CopyProductUserExternalAccountByAccountType(self, Options, OutExternalAccountInfo)
    def CopyProductUserExternalAccountByIndex(self, Options, OutExternalAccountInfo):
        # type: (POINTER(EOS_Connect_CopyProductUserExternalAccountByIndexOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))) -> EOS_EResult
        return EOS_Connect_CopyProductUserExternalAccountByIndex(self, Options, OutExternalAccountInfo)
    def CopyProductUserInfo(self, Options, OutExternalAccountInfo):
        # type: (POINTER(EOS_Connect_CopyProductUserInfoOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))) -> EOS_EResult
        return EOS_Connect_CopyProductUserInfo(self, Options, OutExternalAccountInfo)
    def CreateDeviceId(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_CreateDeviceIdOptions), c_void_p, EOS_Connect_OnCreateDeviceIdCallback) -> None
        return EOS_Connect_CreateDeviceId(self, Options, ClientData, CompletionDelegate)
    def CreateUser(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_CreateUserOptions), c_void_p, EOS_Connect_OnCreateUserCallback) -> None
        return EOS_Connect_CreateUser(self, Options, ClientData, CompletionDelegate)
    def DeleteDeviceId(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_DeleteDeviceIdOptions), c_void_p, EOS_Connect_OnDeleteDeviceIdCallback) -> None
        return EOS_Connect_DeleteDeviceId(self, Options, ClientData, CompletionDelegate)
    def GetExternalAccountMapping(self, Options):
        # type: (POINTER(EOS_Connect_GetExternalAccountMappingsOptions)) -> EOS_ProductUserId
        return EOS_Connect_GetExternalAccountMapping(self, Options)
    def GetLoggedInUserByIndex(self, Index):
        # type: (c_int32) -> EOS_ProductUserId
        return EOS_Connect_GetLoggedInUserByIndex(self, Index)
    def GetLoggedInUsersCount(self): # type: () -> c_int32
        return EOS_Connect_GetLoggedInUsersCount(self)
    def GetLoginStatus(self, LocalUserId):
        # type: (EOS_ProductUserId) -> EOS_ELoginStatus
        return EOS_Connect_GetLoginStatus(self, LocalUserId)
    def GetProductUserExternalAccountCount(self, Options):
        # type: (POINTER(EOS_Connect_GetProductUserExternalAccountCountOptions)) -> c_uint32
        return EOS_Connect_GetProductUserExternalAccountCount(self, Options)
    def GetProductUserIdMapping(self, Options, OutBuffer, InOutBufferLength):
        # type: (POINTER(EOS_Connect_GetProductUserIdMappingOptions), c_char_p, POINTER(c_int32)) -> EOS_EResult
        return EOS_Connect_GetProductUserIdMapping(self, Options, OutBuffer, InOutBufferLength)
    def QueryExternalAccountMappings(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_QueryExternalAccountMappingsOptions), c_void_p, EOS_Connect_OnQueryExternalAccountMappingsCallback) -> None
        return EOS_Connect_QueryExternalAccountMappings(self, Options, ClientData, CompletionDelegate)
    def QueryProductUserIdMappings(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_QueryProductUserIdMappingsOptions), c_void_p, EOS_Connect_OnQueryProductUserIdMappingsCallback) -> None
        return EOS_Connect_QueryProductUserIdMappings(self, Options, ClientData, CompletionDelegate)
    def LinkAccount(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_LinkAccountOptions), c_void_p, EOS_Connect_OnLinkAccountCallback) -> None
        return EOS_Connect_LinkAccount(self, Options, ClientData, CompletionDelegate)
    def Login(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_LoginOptions), c_void_p, EOS_Connect_OnLoginCallback) -> None
        return EOS_Connect_Login(self, Options, ClientData, CompletionDelegate)
    def RemoveNotifyAuthExpiration(self, InId):
        # type: (EOS_NotificationId) -> None
        return EOS_Connect_RemoveNotifyAuthExpiration(self, InId)
    def RemoveNotifyLoginStatusChanged(self, InId):
        # type: (EOS_NotificationId) -> None
        return EOS_Connect_RemoveNotifyLoginStatusChanged(self, InId)
    def TransferDeviceIdAccount(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_TransferDeviceIdAccountOptions), c_void_p, EOS_Connect_OnTransferDeviceIdAccountCallback) -> None
        return EOS_Connect_TransferDeviceIdAccount(self, Options, ClientData, CompletionDelegate)
    def UnlinkAccount(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_UnlinkAccountOptions), c_void_p, EOS_Connect_OnUnlinkAccountCallback) -> None
        return EOS_Connect_UnlinkAccount(self, Options, ClientData, CompletionDelegate)
    def VerifyIdToken(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Connect_VerifyIdTokenOptions), c_void_p, EOS_Connect_OnVerifyIdTokenCallback) -> None
        return EOS_Connect_VerifyIdToken(self, Options, ClientData, CompletionDelegate)

class EOS_HMetrics(c_void_p):
    pass
class EOS_HEcom(c_void_p):
    pass
class EOS_HUI(c_void_p):
    pass
class EOS_HFriends(c_void_p):
    pass
class EOS_HPresence(c_void_p):
    pass
class EOS_HSessions(c_void_p):
    pass
class EOS_HLobby(c_void_p):
    pass
class EOS_HUserInfo(c_void_p):
    pass
class EOS_HP2P(c_void_p):
    pass
class EOS_HRTC(c_void_p):
    pass
class EOS_HRTCAdmin(c_void_p):
    pass
class EOS_HPlayerDataStorage(c_void_p):
    pass
class EOS_HTitleStorage(c_void_p):
    pass
class EOS_HStats(c_void_p):
    def IngestStat(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Stats_IngestStatOptions), c_void_p, EOS_Stats_OnIngestStatCompleteCallback) -> None
        return EOS_Stats_IngestStat(self, Options, ClientData, CompletionDelegate)
    def QueryStats(self, Options, ClientData, CompletionDelegate):
        # type: (POINTER(EOS_Stats_QueryStatsOptions), c_void_p, EOS_Stats_OnQueryStatsCompleteCallback) -> None
        return EOS_Stats_QueryStats(self, Options, ClientData, CompletionDelegate)
    def GetStatsCount(self, Options):
        # type: (POINTER(EOS_Stats_GetStatCountOptions)) -> c_uint32
        return EOS_Stats_GetStatsCount(self, Options)
    def EOS_Stats_CopyStatByIndex(self, Options, OutStat):
        # type: (POINTER(EOS_Stats_CopyStatByIndexOptions), POINTER(POINTER(EOS_Stats_Stat))) -> EOS_EResult
        return EOS_Stats_CopyStatByIndex(self, Options, OutStat)
    def EOS_Stats_CopyStatByName(self, Options, OutStat):
        # type: (POINTER(EOS_Stats_CopyStatByNameOptions), POINTER(POINTER(EOS_Stats_Stat))) -> EOS_EResult
        return EOS_Stats_CopyStatByIndex(self, Options, OutStat)

class EOS_HLeaderboards(c_void_p):
    pass
class EOS_HMods(c_void_p):
    pass
class EOS_HAntiCheatClient(c_void_p):
    pass
class EOS_HAntiCheatServer(c_void_p):
    pass
class EOS_HProgressionSnapshot(c_void_p):
    pass
class EOS_HReports(c_void_p):
    pass
class EOS_HSanctions(c_void_p):
    pass
class EOS_HKWS(c_void_p):
    pass
class EOS_HCustomInvites(c_void_p):
    pass

def load(dll):

    # Version

    global EOS_GetVersion
    EOS_GetVersion = dll.EOS_GetVersion
    EOS_GetVersion.argtypes = []
    EOS_GetVersion.restype = c_char_p

    # Commons

    global EOS_EResult_ToString
    EOS_EResult_ToString = dll.EOS_EResult_ToString
    EOS_EResult_ToString.argtypes = [EOS_EResult]
    EOS_EResult_ToString.restype = c_char_p

    global EOS_EResult_IsOperationComplete
    EOS_EResult_IsOperationComplete = dll.EOS_EResult_IsOperationComplete
    EOS_EResult_IsOperationComplete.argtypes = [EOS_EResult]
    EOS_EResult_IsOperationComplete.restype = EOS_Bool

    global EOS_ByteArray_ToString
    EOS_ByteArray_ToString = dll.EOS_ByteArray_ToString
    EOS_ByteArray_ToString.argtypes = [POINTER(c_uint8), c_uint32, c_char_p, POINTER(c_uint32)]
    EOS_ByteArray_ToString.restype = EOS_EResult

    global EOS_EpicAccountId_IsValid
    EOS_EpicAccountId_IsValid = dll.EOS_EpicAccountId_IsValid
    EOS_EpicAccountId_IsValid.argtypes = [EOS_EpicAccountId]
    EOS_EpicAccountId_IsValid.restype = EOS_Bool

    global EOS_EpicAccountId_ToString
    EOS_EpicAccountId_ToString = dll.EOS_EpicAccountId_ToString
    EOS_EpicAccountId_ToString.argtypes = [EOS_EpicAccountId, c_char_p, POINTER(c_int32)]
    EOS_EpicAccountId_ToString.restype = EOS_EResult

    global EOS_EpicAccountId_FromString
    EOS_EpicAccountId_FromString = dll.EOS_EpicAccountId_FromString
    EOS_EpicAccountId_FromString.argtypes = [c_char_p]
    EOS_EpicAccountId_FromString.restype = EOS_EpicAccountId

    global EOS_ProductUserId_IsValid
    EOS_ProductUserId_IsValid = dll.EOS_ProductUserId_IsValid
    EOS_ProductUserId_IsValid.argtypes = [EOS_ProductUserId]
    EOS_ProductUserId_IsValid.restype = EOS_Bool

    global EOS_ProductUserId_ToString
    EOS_ProductUserId_ToString = dll.EOS_ProductUserId_ToString
    EOS_ProductUserId_ToString.argtypes = [EOS_ProductUserId, c_char_p, POINTER(c_int32)]
    EOS_ProductUserId_ToString.restype = EOS_EResult

    global EOS_ProductUserId_FromString
    EOS_ProductUserId_FromString = dll.EOS_ProductUserId_FromString
    EOS_ProductUserId_FromString.argtypes = [c_char_p]
    EOS_ProductUserId_FromString.restype = EOS_ProductUserId

    global EOS_ContinuanceToken_ToString
    EOS_ContinuanceToken_ToString = dll.EOS_ContinuanceToken_ToString
    EOS_ContinuanceToken_ToString.argtypes = [EOS_ContinuanceToken, c_char_p, POINTER(c_int32)]
    EOS_ContinuanceToken_ToString.restype = EOS_EResult

    # Logging

    global EOS_Logging_SetCallback
    EOS_Logging_SetCallback = dll.EOS_Logging_SetCallback
    EOS_Logging_SetCallback.argtypes = [EOS_LogMessageFunc]
    EOS_Logging_SetCallback.restype = EOS_EResult

    global EOS_Logging_SetLogLevel
    EOS_Logging_SetLogLevel = dll.EOS_Logging_SetLogLevel
    EOS_Logging_SetLogLevel.argtypes = [EOS_ELogCategory, EOS_ELogLevel]
    EOS_Logging_SetLogLevel.restype = EOS_EResult

    # Init

    global EOS_Initialize
    EOS_Initialize = dll.EOS_Initialize
    EOS_Initialize.argtypes = [POINTER(EOS_InitializeOptions)]
    EOS_Initialize.restype = EOS_EResult

    global EOS_Shutdown
    EOS_Shutdown = dll.EOS_Shutdown
    EOS_Shutdown.argtypes = []
    EOS_Shutdown.restype = EOS_EResult

    global EOS_Platform_Create
    EOS_Platform_Create = dll.EOS_Platform_Create
    EOS_Platform_Create.argtypes = [POINTER(EOS_Platform_Options)]
    EOS_Platform_Create.restype = EOS_HPlatform

    global EOS_Platform_Release
    EOS_Platform_Release = dll.EOS_Platform_Release
    EOS_Platform_Release.argtypes = [EOS_HPlatform]
    EOS_Platform_Release.restype = c_void_p

    # Auth types

    global EOS_Auth_Token_Release
    EOS_Auth_Token_Release = dll.EOS_Auth_Token_Release
    EOS_Auth_Token_Release.argtypes = [POINTER(EOS_Auth_Token)]
    EOS_Auth_Token_Release.restype = None

    global EOS_Auth_IdToken_Release
    EOS_Auth_IdToken_Release = dll.EOS_Auth_IdToken_Release
    EOS_Auth_IdToken_Release.argtypes = [POINTER(EOS_Auth_IdToken)]
    EOS_Auth_IdToken_Release.restype = None

    # Auth

    global EOS_Auth_Login
    EOS_Auth_Login = dll.EOS_Auth_Login
    EOS_Auth_Login.argtypes = [EOS_HAuth, POINTER(EOS_Auth_LoginOptions), c_void_p, EOS_Auth_OnLoginCallback]
    EOS_Auth_Login.restype = None

    global EOS_Auth_Logout
    EOS_Auth_Logout = dll.EOS_Auth_Logout
    EOS_Auth_Logout.argtypes = [EOS_HAuth, POINTER(EOS_Auth_LogoutOptions), c_void_p, EOS_Auth_OnLogoutCallback]
    EOS_Auth_Logout.restype = None

    global EOS_Auth_LinkAccount
    EOS_Auth_LinkAccount = dll.EOS_Auth_LinkAccount
    EOS_Auth_LinkAccount.argtypes = [EOS_HAuth, POINTER(EOS_Auth_LinkAccountOptions), c_void_p, EOS_Auth_OnLinkAccountCallback]
    EOS_Auth_LinkAccount.restype = None

    global EOS_Auth_DeletePersistentAuth
    EOS_Auth_DeletePersistentAuth = dll.EOS_Auth_DeletePersistentAuth
    EOS_Auth_DeletePersistentAuth.argtypes = [EOS_HAuth, POINTER(EOS_Auth_DeletePersistentAuthOptions), c_void_p, EOS_Auth_OnDeletePersistentAuthCallback]
    EOS_Auth_DeletePersistentAuth.restype = None

    global EOS_Auth_VerifyUserAuth
    EOS_Auth_VerifyUserAuth = dll.EOS_Auth_VerifyUserAuth
    EOS_Auth_VerifyUserAuth.argtypes = [EOS_HAuth, POINTER(EOS_Auth_VerifyUserAuthOptions), c_void_p, EOS_Auth_OnVerifyUserAuthCallback]
    EOS_Auth_VerifyUserAuth.restype = None

    global EOS_Auth_GetLoggedInAccountsCount
    EOS_Auth_GetLoggedInAccountsCount = dll.EOS_Auth_GetLoggedInAccountsCount
    EOS_Auth_GetLoggedInAccountsCount.argtypes = [EOS_HAuth]
    EOS_Auth_GetLoggedInAccountsCount.restype = c_int32

    global EOS_Auth_GetLoggedInAccountByIndex
    EOS_Auth_GetLoggedInAccountByIndex = dll.EOS_Auth_GetLoggedInAccountByIndex
    EOS_Auth_GetLoggedInAccountByIndex.argtypes = [EOS_HAuth, c_int32]
    EOS_Auth_GetLoggedInAccountByIndex.restype = EOS_EpicAccountId

    global EOS_Auth_GetLoginStatus
    EOS_Auth_GetLoginStatus = dll.EOS_Auth_GetLoginStatus
    EOS_Auth_GetLoginStatus.argtypes = [EOS_HAuth, EOS_EpicAccountId]
    EOS_Auth_GetLoginStatus.restype = EOS_ELoginStatus

    global EOS_Auth_CopyUserAuthToken
    EOS_Auth_CopyUserAuthToken = dll.EOS_Auth_CopyUserAuthToken
    EOS_Auth_CopyUserAuthToken.argtypes = [EOS_HAuth, POINTER(EOS_Auth_CopyUserAuthTokenOptions), EOS_EpicAccountId, POINTER(POINTER(EOS_Auth_Token))]
    EOS_Auth_CopyUserAuthToken.restype = EOS_EResult

    global EOS_Auth_CopyIdToken
    EOS_Auth_CopyIdToken = dll.EOS_Auth_CopyIdToken
    EOS_Auth_CopyIdToken.argtypes = [EOS_HAuth, POINTER(EOS_Auth_CopyIdTokenOptions), POINTER(POINTER(EOS_Auth_IdToken))]
    EOS_Auth_CopyIdToken.restype = EOS_EResult

    global EOS_Auth_QueryIdToken
    EOS_Auth_QueryIdToken = dll.EOS_Auth_QueryIdToken
    EOS_Auth_QueryIdToken.argtypes = [EOS_HAuth, POINTER(EOS_Auth_QueryIdTokenOptions), c_void_p, EOS_Auth_OnQueryIdTokenCallback]
    EOS_Auth_QueryIdToken.restype = None

    global EOS_Auth_VerifyIdToken
    EOS_Auth_VerifyIdToken = dll.EOS_Auth_VerifyIdToken
    EOS_Auth_VerifyIdToken.argtypes = [EOS_HAuth, POINTER(EOS_Auth_VerifyIdTokenOptions), c_void_p, EOS_Auth_OnVerifyIdTokenCallback]
    EOS_Auth_VerifyIdToken.restype = None

    global EOS_Auth_GetSelectedAccountId
    EOS_Auth_GetSelectedAccountId = dll.EOS_Auth_GetSelectedAccountId
    EOS_Auth_GetSelectedAccountId.argtypes = [EOS_HAuth, EOS_EpicAccountId, POINTER(EOS_EpicAccountId)]
    EOS_Auth_GetSelectedAccountId.restype = EOS_EResult

    global EOS_Auth_GetMergedAccountsCount
    EOS_Auth_GetMergedAccountsCount = dll.EOS_Auth_GetMergedAccountsCount
    EOS_Auth_GetMergedAccountsCount.argtypes = [EOS_HAuth, EOS_EpicAccountId]
    EOS_Auth_GetMergedAccountsCount.restype = c_uint32

    global EOS_Auth_GetMergedAccountByIndex
    EOS_Auth_GetMergedAccountByIndex = dll.EOS_Auth_GetMergedAccountByIndex
    EOS_Auth_GetMergedAccountByIndex.argtypes = [EOS_HAuth, EOS_EpicAccountId, c_uint32]
    EOS_Auth_GetMergedAccountByIndex.restype = EOS_EpicAccountId

    global EOS_Auth_AddNotifyLoginStatusChanged
    EOS_Auth_AddNotifyLoginStatusChanged = dll.EOS_Auth_AddNotifyLoginStatusChanged
    EOS_Auth_AddNotifyLoginStatusChanged.argtypes = [EOS_HAuth, POINTER(EOS_Auth_AddNotifyLoginStatusChangedOptions), c_void_p, EOS_Auth_OnLoginStatusChangedCallback]
    EOS_Auth_AddNotifyLoginStatusChanged.restype = EOS_NotificationId

    global EOS_Auth_RemoveNotifyLoginStatusChanged
    EOS_Auth_RemoveNotifyLoginStatusChanged = dll.EOS_Auth_RemoveNotifyLoginStatusChanged
    EOS_Auth_RemoveNotifyLoginStatusChanged.argtypes = [EOS_HAuth, EOS_NotificationId]
    EOS_Auth_RemoveNotifyLoginStatusChanged.restype = None

    # Achievements

    global EOS_Achievements_AddNotifyAchievementsUnlockedV2
    EOS_Achievements_AddNotifyAchievementsUnlockedV2 = dll.EOS_Achievements_AddNotifyAchievementsUnlockedV2
    EOS_Achievements_AddNotifyAchievementsUnlockedV2.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_AddNotifyAchievementsUnlockedV2Options), c_void_p, EOS_Achievements_OnAchievementsUnlockedCallbackV2]
    EOS_Achievements_AddNotifyAchievementsUnlockedV2.restype = EOS_EResult

    global EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId
    EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId = dll.EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId
    EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyAchievementDefinitionV2ByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_DefinitionV2))]
    EOS_Achievements_CopyAchievementDefinitionV2ByAchievementId.restype = EOS_EResult

    global EOS_Achievements_CopyAchievementDefinitionV2ByIndex
    EOS_Achievements_CopyAchievementDefinitionV2ByIndex = dll.EOS_Achievements_CopyAchievementDefinitionV2ByIndex
    EOS_Achievements_CopyAchievementDefinitionV2ByIndex.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyAchievementDefinitionV2ByIndexOptions), POINTER(POINTER(EOS_Achievements_DefinitionV2))]
    EOS_Achievements_CopyAchievementDefinitionV2ByIndex.restype = EOS_EResult

    global EOS_Achievements_CopyPlayerAchievementByAchievementId
    EOS_Achievements_CopyPlayerAchievementByAchievementId = dll.EOS_Achievements_CopyPlayerAchievementByAchievementId
    EOS_Achievements_CopyPlayerAchievementByAchievementId.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyPlayerAchievementByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_PlayerAchievement))]
    EOS_Achievements_CopyPlayerAchievementByAchievementId.restype = EOS_EResult

    global EOS_Achievements_CopyPlayerAchievementByIndex
    EOS_Achievements_CopyPlayerAchievementByIndex = dll.EOS_Achievements_CopyPlayerAchievementByIndex
    EOS_Achievements_CopyPlayerAchievementByIndex.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyPlayerAchievementByIndexOptions), POINTER(POINTER(EOS_Achievements_PlayerAchievement))]
    EOS_Achievements_CopyPlayerAchievementByIndex.restype = EOS_EResult

    global EOS_Achievements_DefinitionV2_Release
    EOS_Achievements_DefinitionV2_Release = dll.EOS_Achievements_DefinitionV2_Release
    EOS_Achievements_DefinitionV2_Release.argtypes = [POINTER(EOS_Achievements_DefinitionV2)]
    EOS_Achievements_DefinitionV2_Release.restype = EOS_EResult

    global EOS_Achievements_GetAchievementDefinitionCount
    EOS_Achievements_GetAchievementDefinitionCount = dll.EOS_Achievements_GetAchievementDefinitionCount
    EOS_Achievements_GetAchievementDefinitionCount.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_GetAchievementDefinitionCountOptions)]
    EOS_Achievements_GetAchievementDefinitionCount.restype = c_uint32

    global EOS_Achievements_GetPlayerAchievementCount
    EOS_Achievements_GetPlayerAchievementCount = dll.EOS_Achievements_GetPlayerAchievementCount
    EOS_Achievements_GetPlayerAchievementCount.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_GetPlayerAchievementCountOptions)]
    EOS_Achievements_GetPlayerAchievementCount.restype = c_uint32

    global EOS_Achievements_PlayerAchievement_Release
    EOS_Achievements_PlayerAchievement_Release = dll.EOS_Achievements_PlayerAchievement_Release
    EOS_Achievements_PlayerAchievement_Release.argtypes = [POINTER(EOS_Achievements_PlayerAchievement)]
    EOS_Achievements_PlayerAchievement_Release.restype = EOS_EResult

    global EOS_Achievements_QueryDefinitions
    EOS_Achievements_QueryDefinitions = dll.EOS_Achievements_QueryDefinitions
    EOS_Achievements_QueryDefinitions.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_QueryDefinitionsOptions), c_void_p, EOS_Achievements_OnQueryDefinitionsCompleteCallback]
    EOS_Achievements_QueryDefinitions.restype = None

    global EOS_Achievements_QueryPlayerAchievements
    EOS_Achievements_QueryPlayerAchievements = dll.EOS_Achievements_QueryPlayerAchievements
    EOS_Achievements_QueryPlayerAchievements.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_QueryPlayerAchievementsOptions), c_void_p, EOS_Achievements_OnQueryPlayerAchievementsCompleteCallback]
    EOS_Achievements_QueryPlayerAchievements.restype = EOS_EResult

    global EOS_Achievements_RemoveNotifyAchievementsUnlocked
    EOS_Achievements_RemoveNotifyAchievementsUnlocked = dll.EOS_Achievements_RemoveNotifyAchievementsUnlocked
    EOS_Achievements_RemoveNotifyAchievementsUnlocked.argtypes = [EOS_HAchievements, EOS_NotificationId]
    EOS_Achievements_RemoveNotifyAchievementsUnlocked.restype = EOS_EResult

    global EOS_Achievements_UnlockAchievements
    EOS_Achievements_UnlockAchievements = dll.EOS_Achievements_UnlockAchievements
    EOS_Achievements_UnlockAchievements.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_UnlockAchievementsOptions), c_void_p, EOS_Achievements_OnUnlockAchievementsCompleteCallback]
    EOS_Achievements_UnlockAchievements.restype = EOS_EResult

    # DEPRECATED Achievements

    global EOS_Achievements_Definition_Release
    EOS_Achievements_Definition_Release = dll.EOS_Achievements_Definition_Release
    EOS_Achievements_Definition_Release.argtypes = [POINTER(EOS_Achievements_Definition)]
    EOS_Achievements_Definition_Release.restype = None

    global EOS_Achievements_UnlockedAchievement_Release
    EOS_Achievements_UnlockedAchievement_Release = dll.EOS_Achievements_UnlockedAchievement_Release
    EOS_Achievements_UnlockedAchievement_Release.argtypes = [POINTER(EOS_Achievements_UnlockedAchievement)]
    EOS_Achievements_UnlockedAchievement_Release.restype = None

    global EOS_Achievements_AddNotifyAchievementsUnlocked
    EOS_Achievements_AddNotifyAchievementsUnlocked = dll.EOS_Achievements_AddNotifyAchievementsUnlocked
    EOS_Achievements_AddNotifyAchievementsUnlocked.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_AddNotifyAchievementsUnlockedOptions), c_void_p, EOS_Achievements_OnAchievementsUnlockedCallback]
    EOS_Achievements_AddNotifyAchievementsUnlocked.restype = EOS_NotificationId

    global EOS_Achievements_CopyAchievementDefinitionByAchievementId
    EOS_Achievements_CopyAchievementDefinitionByAchievementId = dll.EOS_Achievements_CopyAchievementDefinitionByAchievementId
    EOS_Achievements_CopyAchievementDefinitionByAchievementId.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyAchievementDefinitionByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_Definition))]
    EOS_Achievements_CopyAchievementDefinitionByAchievementId.restype = EOS_EResult

    global EOS_Achievements_CopyAchievementDefinitionByIndex
    EOS_Achievements_CopyAchievementDefinitionByIndex = dll.EOS_Achievements_CopyAchievementDefinitionByIndex
    EOS_Achievements_CopyAchievementDefinitionByIndex.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyAchievementDefinitionByIndexOptions), POINTER(POINTER(EOS_Achievements_Definition))]
    EOS_Achievements_CopyAchievementDefinitionByIndex.restype = EOS_EResult

    global EOS_Achievements_CopyUnlockedAchievementByAchievementId
    EOS_Achievements_CopyUnlockedAchievementByAchievementId = dll.EOS_Achievements_CopyUnlockedAchievementByAchievementId
    EOS_Achievements_CopyUnlockedAchievementByAchievementId.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyUnlockedAchievementByAchievementIdOptions), POINTER(POINTER(EOS_Achievements_UnlockedAchievement))]
    EOS_Achievements_CopyUnlockedAchievementByAchievementId.restype = EOS_EResult

    global EOS_Achievements_CopyUnlockedAchievementByIndex
    EOS_Achievements_CopyUnlockedAchievementByIndex = dll.EOS_Achievements_CopyUnlockedAchievementByIndex
    EOS_Achievements_CopyUnlockedAchievementByIndex.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_CopyUnlockedAchievementByIndexOptions), POINTER(POINTER(EOS_Achievements_UnlockedAchievement))]
    EOS_Achievements_CopyUnlockedAchievementByIndex.restype = EOS_EResult

    global EOS_Achievements_GetUnlockedAchievementCount
    EOS_Achievements_GetUnlockedAchievementCount = dll.EOS_Achievements_GetUnlockedAchievementCount
    EOS_Achievements_GetUnlockedAchievementCount.argtypes = [EOS_HAchievements, POINTER(EOS_Achievements_GetUnlockedAchievementCountOptions)]
    EOS_Achievements_GetUnlockedAchievementCount.restype = c_uint32

    # Connect

    global EOS_Connect_ExternalAccountInfo_Release
    EOS_Connect_ExternalAccountInfo_Release = dll.EOS_Connect_ExternalAccountInfo_Release
    EOS_Connect_ExternalAccountInfo_Release.argtypes = [POINTER(EOS_Connect_ExternalAccountInfo)]
    EOS_Connect_ExternalAccountInfo_Release.restype = None

    global EOS_Connect_IdToken_Release
    EOS_Connect_IdToken_Release = dll.EOS_Connect_IdToken_Release
    EOS_Connect_IdToken_Release.argtypes = [POINTER(EOS_Connect_IdToken)]
    EOS_Connect_IdToken_Release.restype = None

    global EOS_Connect_Login
    EOS_Connect_Login = dll.EOS_Connect_Login
    EOS_Connect_Login.argtypes = [EOS_HConnect, POINTER(EOS_Connect_LoginOptions), c_void_p, EOS_Connect_OnLoginCallback]
    EOS_Connect_Login.restype = None

    global EOS_Connect_CreateUser
    EOS_Connect_CreateUser = dll.EOS_Connect_CreateUser
    EOS_Connect_CreateUser.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CreateUserOptions), c_void_p, EOS_Connect_OnCreateUserCallback]
    EOS_Connect_CreateUser.restype = None

    global EOS_Connect_LinkAccount
    EOS_Connect_LinkAccount = dll.EOS_Connect_LinkAccount
    EOS_Connect_LinkAccount.argtypes = [EOS_HConnect, POINTER(EOS_Connect_LinkAccountOptions), c_void_p, EOS_Connect_OnLinkAccountCallback]
    EOS_Connect_LinkAccount.restype = None

    global EOS_Connect_UnlinkAccount
    EOS_Connect_UnlinkAccount = dll.EOS_Connect_UnlinkAccount
    EOS_Connect_UnlinkAccount.argtypes = [EOS_HConnect, POINTER(EOS_Connect_UnlinkAccountOptions), c_void_p, EOS_Connect_OnUnlinkAccountCallback]
    EOS_Connect_UnlinkAccount.restype = None

    global EOS_Connect_CreateDeviceId
    EOS_Connect_CreateDeviceId = dll.EOS_Connect_CreateDeviceId
    EOS_Connect_CreateDeviceId.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CreateDeviceIdOptions), c_void_p, EOS_Connect_OnCreateDeviceIdCallback]
    EOS_Connect_CreateDeviceId.restype = None

    global EOS_Connect_DeleteDeviceId
    EOS_Connect_DeleteDeviceId = dll.EOS_Connect_DeleteDeviceId
    EOS_Connect_DeleteDeviceId.argtypes = [EOS_HConnect, POINTER(EOS_Connect_DeleteDeviceIdOptions), c_void_p, EOS_Connect_OnDeleteDeviceIdCallback]
    EOS_Connect_DeleteDeviceId.restype = None

    global EOS_Connect_TransferDeviceIdAccount
    EOS_Connect_TransferDeviceIdAccount = dll.EOS_Connect_TransferDeviceIdAccount
    EOS_Connect_TransferDeviceIdAccount.argtypes = [EOS_HConnect, POINTER(EOS_Connect_TransferDeviceIdAccountOptions), c_void_p, EOS_Connect_OnTransferDeviceIdAccountCallback]
    EOS_Connect_TransferDeviceIdAccount.restype = None

    global EOS_Connect_QueryExternalAccountMappings
    EOS_Connect_QueryExternalAccountMappings = dll.EOS_Connect_QueryExternalAccountMappings
    EOS_Connect_QueryExternalAccountMappings.argtypes = [EOS_HConnect, POINTER(EOS_Connect_QueryExternalAccountMappingsOptions), c_void_p, EOS_Connect_OnQueryExternalAccountMappingsCallback]
    EOS_Connect_QueryExternalAccountMappings.restype = None

    global EOS_Connect_QueryProductUserIdMappings
    EOS_Connect_QueryProductUserIdMappings = dll.EOS_Connect_QueryProductUserIdMappings
    EOS_Connect_QueryProductUserIdMappings.argtypes = [EOS_HConnect, POINTER(EOS_Connect_QueryProductUserIdMappingsOptions), c_void_p, EOS_Connect_OnQueryProductUserIdMappingsCallback]
    EOS_Connect_QueryProductUserIdMappings.restype = None

    global EOS_Connect_GetExternalAccountMapping
    EOS_Connect_GetExternalAccountMapping = dll.EOS_Connect_GetExternalAccountMapping
    EOS_Connect_GetExternalAccountMapping.argtypes = [EOS_HConnect, POINTER(EOS_Connect_GetExternalAccountMappingsOptions)]
    EOS_Connect_GetExternalAccountMapping.restype = EOS_ProductUserId

    global EOS_Connect_GetProductUserIdMapping
    EOS_Connect_GetProductUserIdMapping = dll.EOS_Connect_GetProductUserIdMapping
    EOS_Connect_GetProductUserIdMapping.argtypes = [EOS_HConnect, POINTER(EOS_Connect_GetProductUserIdMappingOptions), c_char_p, POINTER(c_int32)]
    EOS_Connect_GetProductUserIdMapping.restype = EOS_EResult

    global EOS_Connect_GetProductUserExternalAccountCount
    EOS_Connect_GetProductUserExternalAccountCount = dll.EOS_Connect_GetProductUserExternalAccountCount
    EOS_Connect_GetProductUserExternalAccountCount.argtypes = [EOS_HConnect, POINTER(EOS_Connect_GetProductUserExternalAccountCountOptions)]
    EOS_Connect_GetProductUserExternalAccountCount.restype = c_uint32

    global EOS_Connect_CopyProductUserExternalAccountByIndex
    EOS_Connect_CopyProductUserExternalAccountByIndex = dll.EOS_Connect_CopyProductUserExternalAccountByIndex
    EOS_Connect_CopyProductUserExternalAccountByIndex.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CopyProductUserExternalAccountByIndexOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))]
    EOS_Connect_CopyProductUserExternalAccountByIndex.restype = EOS_EResult

    global EOS_Connect_CopyProductUserExternalAccountByAccountType
    EOS_Connect_CopyProductUserExternalAccountByAccountType = dll.EOS_Connect_CopyProductUserExternalAccountByAccountType
    EOS_Connect_CopyProductUserExternalAccountByAccountType.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CopyProductUserExternalAccountByAccountTypeOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))]
    EOS_Connect_CopyProductUserExternalAccountByAccountType.restype = EOS_EResult

    global EOS_Connect_CopyProductUserExternalAccountByAccountId
    EOS_Connect_CopyProductUserExternalAccountByAccountId = dll.EOS_Connect_CopyProductUserExternalAccountByAccountId
    EOS_Connect_CopyProductUserExternalAccountByAccountId.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CopyProductUserExternalAccountByAccountIdOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))]
    EOS_Connect_CopyProductUserExternalAccountByAccountId.restype = EOS_EResult

    global EOS_Connect_CopyProductUserInfo
    EOS_Connect_CopyProductUserInfo = dll.EOS_Connect_CopyProductUserInfo
    EOS_Connect_CopyProductUserInfo.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CopyProductUserInfoOptions), POINTER(POINTER(EOS_Connect_ExternalAccountInfo))]
    EOS_Connect_CopyProductUserInfo.restype = EOS_EResult

    global EOS_Connect_GetLoggedInUsersCount
    EOS_Connect_GetLoggedInUsersCount = dll.EOS_Connect_GetLoggedInUsersCount
    EOS_Connect_GetLoggedInUsersCount.argtypes = [EOS_HConnect]
    EOS_Connect_GetLoggedInUsersCount.restype = c_int32

    global EOS_Connect_GetLoggedInUserByIndex
    EOS_Connect_GetLoggedInUserByIndex = dll.EOS_Connect_GetLoggedInUserByIndex
    EOS_Connect_GetLoggedInUserByIndex.argtypes = [EOS_HConnect, c_int32]
    EOS_Connect_GetLoggedInUserByIndex.restype = EOS_ProductUserId

    global EOS_Connect_GetLoginStatus
    EOS_Connect_GetLoginStatus = dll.EOS_Connect_GetLoginStatus
    EOS_Connect_GetLoginStatus.argtypes = [EOS_HConnect, EOS_ProductUserId]
    EOS_Connect_GetLoginStatus.restype = EOS_ELoginStatus

    global EOS_Connect_AddNotifyAuthExpiration
    EOS_Connect_AddNotifyAuthExpiration = dll.EOS_Connect_AddNotifyAuthExpiration
    EOS_Connect_AddNotifyAuthExpiration.argtypes = [EOS_HConnect, POINTER(EOS_Connect_AddNotifyAuthExpirationOptions), c_void_p, EOS_Connect_OnAuthExpirationCallback]
    EOS_Connect_AddNotifyAuthExpiration.restype = EOS_NotificationId

    global EOS_Connect_RemoveNotifyAuthExpiration
    EOS_Connect_RemoveNotifyAuthExpiration = dll.EOS_Connect_RemoveNotifyAuthExpiration
    EOS_Connect_RemoveNotifyAuthExpiration.argtypes = [EOS_HConnect, EOS_NotificationId]
    EOS_Connect_RemoveNotifyAuthExpiration.restype = None

    global EOS_Connect_AddNotifyLoginStatusChanged
    EOS_Connect_AddNotifyLoginStatusChanged = dll.EOS_Connect_AddNotifyLoginStatusChanged
    EOS_Connect_AddNotifyLoginStatusChanged.argtypes = [EOS_HConnect, POINTER(EOS_Connect_AddNotifyLoginStatusChangedOptions), c_void_p, EOS_Connect_OnLoginStatusChangedCallback]
    EOS_Connect_AddNotifyLoginStatusChanged.restype = EOS_NotificationId

    global EOS_Connect_RemoveNotifyLoginStatusChanged
    EOS_Connect_RemoveNotifyLoginStatusChanged = dll.EOS_Connect_RemoveNotifyLoginStatusChanged
    EOS_Connect_RemoveNotifyLoginStatusChanged.argtypes = [EOS_HConnect, EOS_NotificationId]
    EOS_Connect_RemoveNotifyLoginStatusChanged.restype = None

    global EOS_Connect_CopyIdToken
    EOS_Connect_CopyIdToken = dll.EOS_Connect_CopyIdToken
    EOS_Connect_CopyIdToken.argtypes = [EOS_HConnect, POINTER(EOS_Connect_CopyIdTokenOptions), POINTER(POINTER(EOS_Connect_IdToken))]
    EOS_Connect_CopyIdToken.restype = EOS_EResult

    global EOS_Connect_VerifyIdToken
    EOS_Connect_VerifyIdToken = dll.EOS_Connect_VerifyIdToken
    EOS_Connect_VerifyIdToken.argtypes = [EOS_HConnect, POINTER(EOS_Connect_VerifyIdTokenOptions), c_void_p, EOS_Connect_OnVerifyIdTokenCallback]
    EOS_Connect_VerifyIdToken.restype = None

    # Stats

    global EOS_Stats_Stat_Release
    EOS_Stats_Stat_Release = dll.EOS_Stats_Stat_Release
    EOS_Stats_Stat_Release.argtypes = [POINTER(EOS_Stats_Stat)]
    EOS_Stats_Stat_Release.restype = None

    global EOS_Stats_IngestStat
    EOS_Stats_IngestStat = dll.EOS_Stats_IngestStat
    EOS_Stats_IngestStat.argtypes = [EOS_HStats, POINTER(EOS_Stats_IngestStatOptions), c_void_p, EOS_Stats_OnIngestStatCompleteCallback]
    EOS_Stats_IngestStat.restype = None

    global EOS_Stats_QueryStats
    EOS_Stats_QueryStats = dll.EOS_Stats_QueryStats
    EOS_Stats_QueryStats.argtypes = [EOS_HStats, POINTER(EOS_Stats_QueryStatsOptions), c_void_p, EOS_Stats_OnQueryStatsCompleteCallback]
    EOS_Stats_QueryStats.restype = None

    global EOS_Stats_GetStatsCount
    EOS_Stats_GetStatsCount = dll.EOS_Stats_GetStatsCount
    EOS_Stats_GetStatsCount.argtypes = [EOS_HStats, POINTER(EOS_Stats_GetStatCountOptions)]
    EOS_Stats_GetStatsCount.restype = c_uint32

    global EOS_Stats_CopyStatByIndex
    EOS_Stats_CopyStatByIndex = dll.EOS_Stats_CopyStatByIndex
    EOS_Stats_CopyStatByIndex.argtypes = [EOS_HStats, POINTER(EOS_Stats_CopyStatByIndexOptions), POINTER(POINTER(EOS_Stats_Stat))]
    EOS_Stats_CopyStatByIndex.restype = EOS_EResult

    global EOS_Stats_CopyStatByName
    EOS_Stats_CopyStatByName = dll.EOS_Stats_CopyStatByName
    EOS_Stats_CopyStatByName.argtypes = [EOS_HStats, POINTER(EOS_Stats_CopyStatByNameOptions), POINTER(POINTER(EOS_Stats_Stat))]
    EOS_Stats_CopyStatByName.restype = EOS_EResult

    # SDK

    global EOS_Platform_Tick
    EOS_Platform_Tick = dll.EOS_Platform_Tick
    EOS_Platform_Tick.argtypes = [EOS_HPlatform]
    EOS_Platform_Tick.restype = None

    global EOS_Platform_GetMetricsInterface
    EOS_Platform_GetMetricsInterface = dll.EOS_Platform_GetMetricsInterface
    EOS_Platform_GetMetricsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetMetricsInterface.restype = EOS_HMetrics

    global EOS_Platform_GetAuthInterface
    EOS_Platform_GetAuthInterface = dll.EOS_Platform_GetAuthInterface
    EOS_Platform_GetAuthInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetAuthInterface.restype = EOS_HAuth

    global EOS_Platform_GetConnectInterface
    EOS_Platform_GetConnectInterface = dll.EOS_Platform_GetConnectInterface
    EOS_Platform_GetConnectInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetConnectInterface.restype = EOS_HConnect

    global EOS_Platform_GetEcomInterface
    EOS_Platform_GetEcomInterface = dll.EOS_Platform_GetEcomInterface
    EOS_Platform_GetEcomInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetEcomInterface.restype = EOS_HEcom

    global EOS_Platform_GetUIInterface
    EOS_Platform_GetUIInterface = dll.EOS_Platform_GetUIInterface
    EOS_Platform_GetUIInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetUIInterface.restype = EOS_HUI

    global EOS_Platform_GetFriendsInterface
    EOS_Platform_GetFriendsInterface = dll.EOS_Platform_GetFriendsInterface
    EOS_Platform_GetFriendsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetFriendsInterface.restype = EOS_HFriends

    global EOS_Platform_GetPresenceInterface
    EOS_Platform_GetPresenceInterface = dll.EOS_Platform_GetPresenceInterface
    EOS_Platform_GetPresenceInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetPresenceInterface.restype = EOS_HPresence

    global EOS_Platform_GetSessionsInterface
    EOS_Platform_GetSessionsInterface = dll.EOS_Platform_GetSessionsInterface
    EOS_Platform_GetSessionsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetSessionsInterface.restype = EOS_HSessions

    global EOS_Platform_GetLobbyInterface
    EOS_Platform_GetLobbyInterface = dll.EOS_Platform_GetLobbyInterface
    EOS_Platform_GetLobbyInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetLobbyInterface.restype = EOS_HLobby

    global EOS_Platform_GetUserInfoInterface
    EOS_Platform_GetUserInfoInterface = dll.EOS_Platform_GetUserInfoInterface
    EOS_Platform_GetUserInfoInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetUserInfoInterface.restype = EOS_HUserInfo

    global EOS_Platform_GetP2PInterface
    EOS_Platform_GetP2PInterface = dll.EOS_Platform_GetP2PInterface
    EOS_Platform_GetP2PInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetP2PInterface.restype = EOS_HP2P

    global EOS_Platform_GetRTCInterface
    EOS_Platform_GetRTCInterface = dll.EOS_Platform_GetRTCInterface
    EOS_Platform_GetRTCInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetRTCInterface.restype = EOS_HRTC

    global EOS_Platform_GetRTCAdminInterface
    EOS_Platform_GetRTCAdminInterface = dll.EOS_Platform_GetRTCAdminInterface
    EOS_Platform_GetRTCAdminInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetRTCAdminInterface.restype = EOS_HRTCAdmin

    global EOS_Platform_GetPlayerDataStorageInterface
    EOS_Platform_GetPlayerDataStorageInterface = dll.EOS_Platform_GetPlayerDataStorageInterface
    EOS_Platform_GetPlayerDataStorageInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetPlayerDataStorageInterface.restype = EOS_HPlayerDataStorage

    global EOS_Platform_GetTitleStorageInterface
    EOS_Platform_GetTitleStorageInterface = dll.EOS_Platform_GetTitleStorageInterface
    EOS_Platform_GetTitleStorageInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetTitleStorageInterface.restype = EOS_HTitleStorage

    global EOS_Platform_GetAchievementsInterface
    EOS_Platform_GetAchievementsInterface = dll.EOS_Platform_GetAchievementsInterface
    EOS_Platform_GetAchievementsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetAchievementsInterface.restype = EOS_HAchievements

    global EOS_Platform_GetStatsInterface
    EOS_Platform_GetStatsInterface = dll.EOS_Platform_GetStatsInterface
    EOS_Platform_GetStatsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetStatsInterface.restype = EOS_HStats

    global EOS_Platform_GetLeaderboardsInterface
    EOS_Platform_GetLeaderboardsInterface = dll.EOS_Platform_GetLeaderboardsInterface
    EOS_Platform_GetLeaderboardsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetLeaderboardsInterface.restype = EOS_HLeaderboards

    global EOS_Platform_GetModsInterface
    EOS_Platform_GetModsInterface = dll.EOS_Platform_GetModsInterface
    EOS_Platform_GetModsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetModsInterface.restype = EOS_HMods

    global EOS_Platform_GetAntiCheatClientInterface
    EOS_Platform_GetAntiCheatClientInterface = dll.EOS_Platform_GetAntiCheatClientInterface
    EOS_Platform_GetAntiCheatClientInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetAntiCheatClientInterface.restype = EOS_HAntiCheatClient

    global EOS_Platform_GetAntiCheatServerInterface
    EOS_Platform_GetAntiCheatServerInterface = dll.EOS_Platform_GetAntiCheatServerInterface
    EOS_Platform_GetAntiCheatServerInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetAntiCheatServerInterface.restype = EOS_HAntiCheatServer

    global EOS_Platform_GetProgressionSnapshotInterface
    EOS_Platform_GetProgressionSnapshotInterface = dll.EOS_Platform_GetProgressionSnapshotInterface
    EOS_Platform_GetProgressionSnapshotInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetProgressionSnapshotInterface.restype = EOS_HProgressionSnapshot

    global EOS_Platform_GetReportsInterface
    EOS_Platform_GetReportsInterface = dll.EOS_Platform_GetReportsInterface
    EOS_Platform_GetReportsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetReportsInterface.restype = EOS_HReports

    global EOS_Platform_GetSanctionsInterface
    EOS_Platform_GetSanctionsInterface = dll.EOS_Platform_GetSanctionsInterface
    EOS_Platform_GetSanctionsInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetSanctionsInterface.restype = EOS_HSanctions

    global EOS_Platform_GetKWSInterface
    EOS_Platform_GetKWSInterface = dll.EOS_Platform_GetKWSInterface
    EOS_Platform_GetKWSInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetKWSInterface.restype = EOS_HKWS

    global EOS_Platform_GetCustomInvitesInterface
    EOS_Platform_GetCustomInvitesInterface = dll.EOS_Platform_GetCustomInvitesInterface
    EOS_Platform_GetCustomInvitesInterface.argtypes = [EOS_HPlatform]
    EOS_Platform_GetCustomInvitesInterface.restype = EOS_HCustomInvites

    global EOS_Platform_GetActiveCountryCode
    EOS_Platform_GetActiveCountryCode = dll.EOS_Platform_GetActiveCountryCode
    EOS_Platform_GetActiveCountryCode.argtypes = [EOS_HPlatform, EOS_EpicAccountId, c_char_p, POINTER(c_int32)]
    EOS_Platform_GetActiveCountryCode.restype = EOS_EResult

    global EOS_Platform_GetActiveLocaleCode
    EOS_Platform_GetActiveLocaleCode = dll.EOS_Platform_GetActiveLocaleCode
    EOS_Platform_GetActiveLocaleCode.argtypes = [EOS_HPlatform, EOS_EpicAccountId, c_char_p, POINTER(c_int32)]
    EOS_Platform_GetActiveLocaleCode.restype = EOS_EResult

    global EOS_Platform_GetOverrideCountryCode
    EOS_Platform_GetOverrideCountryCode = dll.EOS_Platform_GetOverrideCountryCode
    EOS_Platform_GetOverrideCountryCode.argtypes = [EOS_HPlatform, c_char_p, POINTER(c_int32)]
    EOS_Platform_GetOverrideCountryCode.restype = EOS_EResult

    global EOS_Platform_GetOverrideLocaleCode
    EOS_Platform_GetOverrideLocaleCode = dll.EOS_Platform_GetOverrideLocaleCode
    EOS_Platform_GetOverrideLocaleCode.argtypes = [EOS_HPlatform, c_char_p, POINTER(c_int32)]
    EOS_Platform_GetOverrideLocaleCode.restype = EOS_EResult

    global EOS_Platform_SetOverrideCountryCode
    EOS_Platform_SetOverrideCountryCode = dll.EOS_Platform_SetOverrideCountryCode
    EOS_Platform_SetOverrideCountryCode.argtypes = [EOS_HPlatform, c_char_p]
    EOS_Platform_SetOverrideCountryCode.restype = EOS_EResult

    global EOS_Platform_SetOverrideLocaleCode
    EOS_Platform_SetOverrideLocaleCode = dll.EOS_Platform_SetOverrideLocaleCode
    EOS_Platform_SetOverrideLocaleCode.argtypes = [EOS_HPlatform, c_char_p]
    EOS_Platform_SetOverrideLocaleCode.restype = EOS_EResult

    global EOS_Platform_CheckForLauncherAndRestart
    EOS_Platform_CheckForLauncherAndRestart = dll.EOS_Platform_CheckForLauncherAndRestart
    EOS_Platform_CheckForLauncherAndRestart.argtypes = [EOS_HPlatform]
    EOS_Platform_CheckForLauncherAndRestart.restype = EOS_EResult

    global EOS_Platform_GetDesktopCrossplayStatus
    EOS_Platform_GetDesktopCrossplayStatus = dll.EOS_Platform_GetDesktopCrossplayStatus
    EOS_Platform_GetDesktopCrossplayStatus.argtypes = [EOS_HPlatform, POINTER(EOS_Platform_GetDesktopCrossplayStatusOptions), POINTER(EOS_Platform_GetDesktopCrossplayStatusInfo)]
    EOS_Platform_GetDesktopCrossplayStatus.restype = EOS_EResult

    global EOS_Platform_SetApplicationStatus
    EOS_Platform_SetApplicationStatus = dll.EOS_Platform_SetApplicationStatus
    EOS_Platform_SetApplicationStatus.argtypes = [EOS_HPlatform, EOS_EApplicationStatus]
    EOS_Platform_SetApplicationStatus.restype = EOS_EResult

    global EOS_Platform_GetApplicationStatus
    EOS_Platform_GetApplicationStatus = dll.EOS_Platform_GetApplicationStatus
    EOS_Platform_GetApplicationStatus.argtypes = [EOS_HPlatform]
    EOS_Platform_GetApplicationStatus.restype = EOS_EApplicationStatus

    global EOS_Platform_SetNetworkStatus
    EOS_Platform_SetNetworkStatus = dll.EOS_Platform_SetNetworkStatus
    EOS_Platform_SetNetworkStatus.argtypes = [EOS_HPlatform, EOS_ENetworkStatus]
    EOS_Platform_SetNetworkStatus.restype = EOS_EResult

    global EOS_Platform_GetNetworkStatus
    EOS_Platform_GetNetworkStatus = dll.EOS_Platform_GetNetworkStatus
    EOS_Platform_GetNetworkStatus.argtypes = [EOS_HPlatform]
    EOS_Platform_GetNetworkStatus.restype = EOS_ENetworkStatus
