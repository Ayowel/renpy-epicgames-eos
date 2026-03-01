init python:
    achievement.register('simple')
    achievement.register('button', stat_max = 3)

label achievements():
    menu:
        "Unlock simple achievements (is unlocked: [achievement.has('simple')])":
            $ achievement.grant('simple')
        "Progress button achievement (progress: [epicapi.get_stat_value('button')]/3)":
            # FIXME: The current implementation takes progress, not expected new value (expected by other Ren'Py achievement systems).
            $ achievement.progress('button', 1 + epicapi.get_stat_value('button'))
        "Go back to start":
            return
    "Wait a second to mask epic data reload after update." (multiple=2)
    pause 1
    "{nw}" (multiple=2)
    jump achievements
