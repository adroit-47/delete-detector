import imaplib
import email
import tkinter as tk
import pickle as p
from threading import Timer

def alert():
    Illegal = tk.Tk()
    Illegal.title('Alert!!')
    Illegal.geometry('300x140')
    Label = tk.Label(Illegal, text='Screenshot now!!')
    Label.config(font=("Bahnschrift Light", 12))
    Label.place(x=150, y=70, anchor=tk.CENTER)
    Illegal.mainloop()
    return ""

def emails_read():
    print("Reading emails")
    imap_host = 'imap.gmail.com'
    imap_user = 'kyappytongue@gmail.com'
    imap_pass = 'sffkN5KY*$x$bo'

    # connect to host using SSL
    imap = imaplib.IMAP4_SSL(imap_host)

    ## login to server
    imap.login(imap_user, imap_pass)

    imap.select('Inbox')
    subject_list = []
    tmp, data = imap.search(None, 'ALL')
    emails = data[0].split()
    for num in emails[-1:-30:-1]:
        tmp, data = imap.fetch(num, '(RFC822)')
        for response in data:       
            if isinstance(response, tuple):
                message = email.message_from_bytes(response[1])
                mail_subject = message['subject']
                subject_list.append(mail_subject)
    imap.close()
    return subject_list


def previter_read():
    with open('previter.dat','rb') as f:
        data = p.load(f)
        return data

def previter_write():
    with open('previter.dat','wb') as f:
        p.dump(emails_read(), f)
        print("Email list updated")



def check_delete():
    try: 
        previous_list = previter_read()
        print("Checking for deletions")
        print("Previous list: ", previous_list) #debug statement
        current_list = emails_read()
        print() #debug statement
        print("Current list: ",current_list) #debug statement
        first_element = previous_list[0]
        if first_element in current_list:
            req_index = current_list.index(first_element)
            list_length = len(previous_list) - req_index
            prev_req = previous_list[0:list_length]
            current_req = current_list[req_index:]
            if prev_req != current_req:
                print("Deletion found")
                #alert()
            else:
                print("No deleted emails")
        else:
            ("Deletion found")
            #alert()
    except:
        print("First pass. Ignoring comparisons.")        
    previter_write()  






check_delete()
t = Timer(30.0, check_delete)
t.start()
t = Timer(30.0, check_delete)
t.start()