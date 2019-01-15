# aetelbot

Telegram bot for the Asoc. Electrónica de Teleco.


Has the following commands:

* foto - sends a picture of AETEL right now (can only be used by members)
* gif - sends a gif of AETEL right now (can only be used by members)
* puerta - opens the door (can only be used by members)
* bus - deploys a menu to check when the next bus to or from Campus Sur comes
* bus line_Nº stop_Nº - shows when next bus is coming to said stop
* abono - shows when you CRTM abono ends  
	- use: /abono 001 0000023768
	- substitute with your number  
* luz - lights AETEL  
	- use: /luz color, /luz r g b (example /luz 120 30 40), /luz color first-led last-led (example /luz BLUE 30 80)  
	- /apagarluz to turn off  
	- supported colors: See Colores.txt  
* animations - starts light animation  
	- use: /startanimation 1  
	- /stopanimation to turn it off  
	- supported animations 1 to 6: Random Pixel Fade, Orange Theather Chase, Raibow Theather Chase, Fade In Fade Out, Rotate, Color Waves  

Not implemented:

* comida - starts a poll to see who eats at school today (can only be started by members)
* list-comida - lists all the people who eat at school today
* shut-camera - turns off camera commands (only admins)

---

Needs a data-and-settings.json file in the same directory to run.
