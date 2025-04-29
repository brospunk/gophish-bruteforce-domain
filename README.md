necessary for using the code:
- linux
- apt install tor
- pip install requests os time bs4

the codes do:
- input the gophish login domain
- input the Wordlist Path
- automated --> take the cookie and CSRF Token (with Tor)
- automated --> sends passwords to the login page with the tor connection
               (if there is an error in sending or a "Too Many Request" it acquires a new cookie, new CSRF Token and new Tor IP)

***********************************************************
- if the program gives an error immediately after entering the 2 inputs then try to start the Tor service. Comand: systemctl start tor
- the program continues until it finds the password
- the password is found when it receives a status code like 302
