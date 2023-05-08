
define config.name = _("Epic demo app")

define build.name = "Epic_demo"
define build.executable_name = "epic_eos" # This is used in Epic_demo.ini to launch the game

init python:
    # Game files
    build.classify('game/**.rpy', 'all')
    build.classify('game/**.rpyc', 'all')
    build.classify('LICENSE', 'all')
    build.classify('CREDITS', 'all')

    ## Epic support, none of those files may be in an archive
    # Epic extension
    build.classify('game/epic_eos.rpe', 'linux mac windows')
    # Epic libs
    build.classify('libs/EOSSDK-Win*-Shipping.dll', 'windows')
    build.classify('libs/*/xaudio2_9redist.dll', 'windows')
    build.classify('libs/libEOSSDK-Linux-Shipping.so', 'linux')
    build.classify('libs/libEOSSDK-Mac-Shipping.dylib', 'mac')

    # Forbid non-explicitly added files
    # This is not required in regular games and is just a personnal whim
    build.classify('libs/**', 'all')
    build.classify('game/**', 'all')
    build.classify('**', None)
