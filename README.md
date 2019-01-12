# aetelbot

Telegram bot for the Asoc. Electrónica de Teleco.


Has the following commands:

* foto - sends a picture of AETEL right now (can only be used by members)
* gif - sends a gif of AETEL right now (can only be used by members)
* puerta - opens the door (can only be used by members)
* bus - deploys a menu to check when the next bus to or from Campus Sur comes
* bus line_Nº stop_Nº - shows when next bus is coming to said stop
* luz - Lights AETEL
	use: /luz color, /luz r g b (example /luz 120 30 40), /luz color first-led last-led (example /luz BLUE 30 80)
	supported colors: See Colores.txt
*Animations - /startanimation
	use: /startanimation 1
	supported animations 1 to 6: Random Pixel Fade, Orange Theather Chase, raibow theather chase, Fade In Fade Out, Rotate, Color Waves

Not implemented:

* add @someone - only can be used by @aetel admins, adds @someone to the list of AETEL members
* list - lists all current members and IDs
* comida - starts a poll to see who eats at school today (can only be started by members)
* list-comida - lists all the people who eat at school today
* shut-camera - turns off camera commands

---

Needs a data-and-settings.json file in the same directory to run.
