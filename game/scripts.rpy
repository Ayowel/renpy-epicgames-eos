label start:
    "Hello"
    menu:
        "Quit":
            $ renpy.quit()
        "Continue":
            "Restarting"
    jump start

screen yesno_prompt(message='Are you sure?', yes_action = [], no_action = []):
    image 'black'
    vbox:
        align (0.5, 0.5)
        text message:
            xalign 0.5
        textbutton 'Yes':
            xalign 0.5
            action yes_action
        textbutton 'No':
            xalign 0.5
            action no_action
