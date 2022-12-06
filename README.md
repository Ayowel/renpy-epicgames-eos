# Epic Online Services extension for Ren'Py

This extension adds Epic Games achievements support to Ren'Py.

In the future, the extension will be updated to cover more EOS features such as authentication.
The end goal is to provide a thin ctypes wrapper around all EOS functions as well as helpers for the most commonly used features.

## Usage

1. Unpack a release archive of the extension in your game's directory
2. Update `EOS_runner.ini` to point towards the game's generated exe file. This is most easily done and maintained by setting `define build.executable_name`.
3. Create a new `game/epic.rpy` file with the following information:

```py
# Get all attribute values under "Product Settings" -> "SDK Download & Credentials" at dev.epicgames.com
# You may need to create an EOS client for your game in "Product Settings" -> "Clients"
define config.epic_product = '0123456789abcdef0123456789abcdef'
define config.epic_sandbox = 'abcdef0123456789abcdef0123456789'
define config.epic_deployment = '456789abcdef0123456789abcdef0123'
define config.epic_client = 'AbCdEfGhIjKlMnOpQrStUv0123456789'
define config.epic_clientsecret = 'OT60Kvx3QM0ivZTncg8+yypmnNC1bcawfmQQ5C+8AGX'

# The client's policy MUST have the following Achievements features:
# - findAchievementsForLocalUser, unlockAchievementForLocalUser
# The client's policy MAY have the following Achievements features:
# - findAchievementDefinitions, readAchievementDefinition, 
define config.enable_epic_achievements = True

# The requested permissions. See EOS_EAuthScopeFlags for potential value
define config.epic_scopes = 0x0

init -1499 python:
    achievement.backends.insert(0, epicapi.EpicBackend())

init python in epicapi:
    # Start the Epic EOS handler here
    init()
```

4. Add the library files to your packaging rules file (usually `game/options.rpy`):

```py
init python:
    ## Epic support, none of those files may be in an archive
    # Epic extension
    build.classify('game/epic_eos.rpe', 'all')
    # Renamed EOSBootstrapperTool.exe from the SDK
    build.classify('EOS_runner.exe', 'windows')
    build.classify('EOS_runner.ini', 'windows')
    # Epic libs
    build.classify('libs/EOSSDK-Win*-Shipping.dll', 'windows')
    build.classify('libs/*/xaudio2_9redist.dll', 'windows')
    build.classify('libs/libEOSSDK-Linux-Shipping.so', 'linux')
    build.classify('libs/libEOSSDK-Mac-Shipping.dylib', 'mac')
```

*Loading the Epic DLL on windows requires that the player has the [Visual C++ Redistributable](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) installed.*

## Game configuration in Epic Games Store

Creating a new game in the Epic Games Store and configuring it to be useable can be tricky. The following instructions will lead you step by step in the creation and configuration of a client for a new game.

* Go to https://dev.epicgames.com/portal/ to connect to your developer portal
* Create a new game:
  * Press `+ Create Product` in the left menu to create a new product
  * Input an arbitrary name and follow the setup instructions
  * Click on the new product in the left menu to access its configuration
* Create a new game client:
  * Go to `Product Settings` in the left menu
  * Open the `Clients` tab
  * Press `Add new client`
  * Input an arbitrary client name
  * Create a new client policy (or select an existing one):
    * Press `Add new client policy` 
    * Input an arbitrary client policy name
    * Select the `Custom` client policy type
    * Set the `User required` client policy condition
    * Enable the following achievements features:
      * `findAchievementsForLocalUser`
      * `unlockAchievementForLocalUser`
    * Press `Save & Exit`
  * Press `Save & Exit`
* Bind the new client to your application:
  * Go to `Epic Account Services` in the left menu
  * Press `Linked Clients` on your application
  * Select the new client and press `Save changes`
* Ensure that permissions are configured:
  * Go to `Epic Account Services` in the left menu
  * Press `Permissions` on your application
  * Press `Save changes`
* Update Ren'Py configuration:
  * Go to `Product Settings`
  * Open the `SDK Download & Credentials` tab
  * Scroll down to view all the IDs that should be updated in `game/epic.rpy`:
    * Set `config.epic_product` to your `Product ID`
    * Set `config.epic_sandbox` to your `Sandbox ID`
    * Set `config.epic_deployment` to your `Deployment ID`
    * Set `config.epic_client` to your `Client ID`
    * Set `config.epic_clientsecret` to your `Client Secret`

*Note that when running a game from the Epic Games Store, only the `config.epic_client` and `config.epic_clientsecret` are used as all other values are provided as parameters by Epic and the configuration is ignored.*
