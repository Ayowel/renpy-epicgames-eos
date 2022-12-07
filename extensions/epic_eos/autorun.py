import epic_eos
import renpy

if not hasattr(renpy.arguments, 'epic_arguments'):
    # We're on an old Ren'Py version without epic launcher support
    # This is based on changes made in 3429731ca5fb8447ed925a82d12517265f6eff80 in Ren'Py
    import sys
    has_epic_args = True
    for i in sys.argv[1:]:
        if i.lower().startswith("-epicapp="):
            break
    else:
        has_epic_args = False

    if has_epic_args:
        renpy.arguments.epic_arguments = sys.argv[1:]
        sys.argv = [ sys.argv[0] ]

# Add 'mandatory' config
renpy.store.config.epic_client = None
renpy.store.config.epic_clientsecret = None

# Add optional config
renpy.store.config.epic_product = None
renpy.store.config.epic_sandbox = None
renpy.store.config.epic_deployment = None

# Add feature flags
renpy.store.config.enable_epic_achievements = False
renpy.store.config.epic_scopes = None

# Add development flags and config
renpy.store.config.epic_log_console = False
renpy.store.config.epic_userlogin = None
renpy.store.config.epic_userpassword = None
renpy.store.config.epic_authtype = None

# Add store context
renpy.python.create_store('store.epicapi')
renpy.store.epicapi.__dict__.setdefault('init', epic_eos.epic_init)
renpy.store.epicapi.__dict__.setdefault('native', epic_eos.cdefs)
renpy.store.epicapi.__dict__.setdefault('shutdown', epic_eos.epic_shutdown)

renpy.store.epicapi.__dict__.setdefault('EpicBackend', epic_eos.ren.EpicBackend)
renpy.store.epicapi.__dict__.setdefault('is_logged_in', epic_eos.compat.is_logged_in)
renpy.store.epicapi.__dict__.setdefault('retrieve_stats', epic_eos.compat.retrieve_stats)
renpy.store.epicapi.__dict__.setdefault('list_achievements', epic_eos.compat.list_achievements)
renpy.store.epicapi.__dict__.setdefault('get_achievement', epic_eos.compat.get_achievement)
renpy.store.epicapi.__dict__.setdefault('grant_achievement', epic_eos.compat.grant_achievement)
