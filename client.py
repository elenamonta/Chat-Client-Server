import socket
import threading as tr
import tkinter as tki

"""La funzione che segue gestisce l'invio dei messaggi."""
def send():
    # manda messaggi al server
    try:
        msg = insert_msg.get()
        if msg:
            # libera la casella di input.
            insert_msg.delete(0, tki.END)
            client.send(msg.encode())
            if(msg == "{quit}"):
                end()
    except:
        end()

"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    # riceve i messaggi (gestito da un thread)
    try:
        while True:
            msg = client.recv(BFR_SIZE).decode()
            if msg != "{quit}":
                #visualizziamo l'elenco dei messaggi sullo schermo
                messages.insert(tki.END, msg)
                messages.yview(tki.END)
            else:
                print("SERVER DISCONNESSO")
                end()
    except:
        return

def gen_view():
    global view
    global messages
    global insert_msg
    view = tki.Tk()
    view.title("Chat di " + nome)
    
    # Frame per contenere i messaggi
    msg_frame = tki.Frame(view)
    msg_frame.pack()
    
    # scrollbar per navigare tra i messaggi precedenti.
    lateral_bar = tki.Scrollbar(msg_frame)
    lateral_bar.pack(side=tki.RIGHT, fill=tki.Y)
    
    # La parte seguente contiene i messaggi.
    messages = tki.Listbox(msg_frame, height=15, width=50, yscrollcommand=lateral_bar.set)
    messages.pack(side=tki.LEFT, fill=tki.BOTH)
    lateral_bar.config(command=messages.yview)
    
    insert_msg = tki.Entry(view)
    insert_msg.pack(fill=tki.BOTH, padx=10, pady=10)
    insert_msg.bind("<Return>", lambda event: send())
    
    view.protocol("WM_DELETE_WINDOW", end)

def view_exists():
    try:
        view.winfo_exists()
        return True
    except tki.TclError:
        return False

def end():
    client.close()
    if view_exists():
        view.destroy()
    main()

def main():
    global BFR_SIZE
    global client
    global nome
    
    BFR_SIZE = 1024
    nome = ""
    host = ""
    port = 0
    
    #----Connessione al Server----
    try: 
        while not nome:
            nome = input("Inserisci il tuo username: ")
        
        while not host and port == 0:
            try:
                host = input("Inserisci indirizzo host: ")
                port = int(input("Inserisci numero di porta: "))
            except:
                pass
            if not host and port == 0:
                print("Informazioni errate, riprovare")

        addr = (host, port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.send(nome.encode()) 
        gen_view()
        start_receiver = tr.Thread(target=receive) 
        start_receiver.start()
        
        view.mainloop() 
        
        end()
    except Exception as e:
        print(e)
        end()

if __name__ == "__main__":
    main()

