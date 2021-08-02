# Client-side-server

The objective of this project was to create a network distributed system for a group-based client-server communication with a GUI.

I utilized PyQt5 in order to create and to edit the GUI used in the program.

The server constantly awaits users input and when an input is detected the server informations updates for all users.
There is a designated admin,the admin is the first user to join the chat and when the current admin either leaves or has an unexpected shutdown a new admin is selected.
The admin has permission to kick or ban users(the ban currently only works for nickname ban not an IP ban),if any other users tries to kick or ban anyone the server informs the user that he does not have permissions for using said commands.
The data is encrypted when leaving the client and is then decrypted by the server.
