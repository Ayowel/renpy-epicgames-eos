label start():
    "Hello"
    menu:
        "Achievements":
            call achievements
        "Back to main menu":
            $ renpy.run(MainMenu(confirm=False))
        "Quit":
            $ renpy.quit()
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

# Required to test normal game flow and return to main screen
label main_menu:
    call screen main_menu

screen main_menu():
    tag menu
    vbox:
        align (0.5, 0.5) spacing 20
        textbutton "Start" action Start() xalign 0.5
        textbutton "Exit" action Quit() xalign 0.5

style button_text:
    hover_color "#f00"
