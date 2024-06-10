"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone."""

import socket
import threading
import tkinter as tk

def write(msg):
    # scrive sul tkinter del server
    messages.insert(tk.END, msg)
    messages.yview(tk.END)

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg):
    #manda un messaggio a tutti i client attivi (in questo caso quit segnala l'interruzione del server)
    if msg != "{quit}":
        write(msg)
    for c in clients:
        try:
            c.send(msg.encode())
        except:
            pass

def delete(client):
    #toglie un client dalla lista e dice che si è disconnesso
    try:
        broadcast("SERVER: si è disconnesso " + clients[client])
        del clients[client]
    except:
        pass

"""La funzione seguente gestisce la connessione di un singolo client."""
def client_man(client):
    # prende il nome che il client gli manda appena connesso, lo comunica agli altri client e poi continua a tentare di ricevere un messaggio
    try:
        nome = client.recv(BFR_SIZE).decode()
        #aggiorna il dizionario
        clients[client] = nome
        #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
        broadcast("SERVER: è entrato " + nome)
        #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
        while True:
            try:
                msg = client.recv(BFR_SIZE).decode()
                if msg == "{quit}":
                    delete(client)
                else:
                    broadcast(clients[client] + ": " + msg)
            except:
                break
        delete(client)
    except:
        delete(client)
    
def fine():
    #chiude tutto, e manda l'avviso ai client
    view.destroy()
    broadcast("{quit}")
    server.close()
    exit(0)
    
def gen_view():
    global view
    global messages
    
    view = tk.Tk()
    view.title("SERVER")
    
    msg_frame = tk.Frame(view)
    msg_frame.pack()
    
    scrollbar = tk.Scrollbar(msg_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    messages = tk.Listbox(msg_frame, height=15, width=50, font=("Arial", 12), yscrollcommand=scrollbar.set)
    messages.pack(side=tk.LEFT, fill=tk.BOTH)
    view.message_list = messages
    
    scrollbar.config(command=messages.yview)
    
    #richiama fine in chiusura
    view.protocol("WM_DELETE_WINDOW", fine)

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def client_accept():
    while True:
        try:
            client, acc = server.accept()
            #diamo inizio all'attività del Thread - uno per ciascun client
            threading.Thread(target=client_man, args=(client,)).start()
        except:
            break

def main():
    global BFR_SIZE
    global clients
    global server
    
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5001
    ADDR = (HOST, PORT)
    BFR_SIZE = 1024
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = {} #questo è il dizionario dei client
    
    try:
        server.bind(ADDR)
        server.listen()
        gen_view()
        write("Server in ascolto su " + str(ADDR))
        threading.Thread(target=client_accept).start() #fa iniziare l'accettazione
        view.mainloop() #fa partire la finestra
        
    except Exception as e:
        print(e)
        fine()

if __name__ == "__main__":
    main()

