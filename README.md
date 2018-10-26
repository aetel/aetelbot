# aetelbot

Telegram bot for the Asoc. Electrónica de Teleco.


Has the following commands:

* foto - sends a picture of AETEL right now (can only be used by members)
* gif - sends a gif of AETEL right now (can only be used by members)
* puerta - opens the door (can only be used by members)
* bus - deploys a menu to check when the next bus to or from Campus Sur comes
* bus line_Nº stop_Nº - shows when next bus is coming to said stop
* luz - Lights AETEL
	use: /luz color
	supported colors: rojo, naranja, amarillo, verde, azul, indigo, violeta, magenta, blanco

Not implemented:

* add @someone - only can be used by @aetel admins, adds @someone to the list of AETEL members
* list - lists all current members and IDs
* comida - starts a poll to see who eats at school today (can only be started by members)
* list-comida - lists all the people who eat at school today
* shut-camera - turns off camera commands

---

Needs a data-and-settings.json file in the same directory to run.