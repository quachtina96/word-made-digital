#!/usr/bin/python

"""
email_terminal.py is a script written by Tina Quach (quachtina96@gmail.com). It 
is meant to be game that reflects the email experiences of  the typical MIT 
undergraduate living in East Campus. Given that the script prompts for your email
information, and pulls real emails out of your inbox for the purpose of the game
interaction, it is ideal if you are an undergraduate MIT student living in East 
Campus. No guarantees if you aren't.

At the same time, you should feel free to download a local version of the code 
and tinker with it! 
"""
import email, getpass, imaplib, os
from cmd import Cmd
import random
from collections import defaultdict
import time

type_to_filter_dict = {'EC':  '(TO "ec-discuss@mit.edu")',
     'Piazza': '(FROM "no-reply@piazza.com>")',
      "Jobs":   '(TO "eecs-jobs-announce@csail.mit.edu")'}

class Email():
    def __init__(self, header, content, email_type):
        self.sender = header[header.find('['): header.find(']')+1]
        self.subject = header[header.find(':')+1 :]
        self.header = header
        self.content = content
        self.type = email_type

class EmailClient():
    def __init__(self, opt_email_list=None):
        # self.map maps email type to a list of 
        if opt_email_list:
            self.map = self.generate_map_from_email_list(opt_email_list)
        else:
            self.map = defaultdict(list)
        self.user = None

    def generate_map_from_email_list(self, email_list):
        email_map = defaultdict(list)
        for email in email_list:
            email_map[email.email_type].append(email)
        return email_map
    
    def add_to_map(self, email_list):
        for email in email_list:
            self.map[email.type].append(email)
        return self.map

    def get_emails(self, opt_count=None, opt_email_type=None):
        if opt_email_type:
            result = self.map[opt_email_type]
        else:
            result = []
            for values in self.map.values():
                result += [value for value in values]

        if opt_count:
            return result[:min(len(result), opt_count)]
        else:
            return result

    def get_random_email(self, opt_email_type=None):
        if opt_email_type:
            rand_email = random.choice(self.get_emails(email_type))
        else:
            rand_email = random.choice(self.get_emails())
        return rand_email

    def populate_basic_map(self, num_emails):
        if not test:
            self.user = raw_input("your email (without the @gmail.com): ")
            #pwd = raw_input("password: ")
            pwd=getpass.getpass()
        else:
            self.user = 'quachtina96'
            pwd = '0mgGoogle!'

        print('Loading...')
        
        # of emails to fetch per category.
        fetch = num_emails

        # connecting to the gmail imap server
        m = imaplib.IMAP4_SSL("imap.gmail.com")
        m.login(self.user+str("@gmail.com"),pwd)
        m.select("INBOX") # here you a can choose a mail box like INBOX instead
        # use m.list() to get all the mailboxes
        
        email_list = []

        date = (datetime.date.today() - datetime.timedelta(3)).strftime("%d-%b-%Y")
        result, data = m.uid('search', None, '(SENTSINCE {date})'.format(date=date))
        items = data[0].split()

        if (int(fetch)>0):
            sublist=items[-1*(min(int(fetch), len(items))):]
        else:
            sublist=items

        for emailid in sublist:
            resp, data = m.uid('fetch', emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
            email_body = data[0][1] # getting the mail content
            mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

            header =  "["+mail["From"]+"] : Re:" + mail["Subject"]
            
            # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
            content = []
            for part in mail.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    content.append(body)
                else:
                    continue
            email_obj = Email(header, '\n'.join(content), 'any')
            email_list.append(email_obj)
        self.add_to_map(email_list)

    def populate_map(self, type_to_filter_dict, num_emails_per_filter):
        self.user = raw_input("your email (without the @gmail.com): ")
        #pwd = raw_input("password: ")
        pwd=getpass.getpass()
        filename = 'emails'

        print('Loading...')
        
        # of emails to fetch per category.
        fetch = num_emails_per_filter

        # connecting to the gmail imap server
        m = imaplib.IMAP4_SSL("imap.gmail.com")
        m.login(self.user+str("@gmail.com"),pwd)
        m.select("INBOX") # here you a can choose a mail box like INBOX instead
        # use m.list() to get all the mailboxes
        
        for email_type, email_filter in type_to_filter_dict.items():
            print email_type
            try:
                email_list = []
                

                resp, items = m.search(None, email_filter) # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
                items = items[0].split() # getting the mails id

                f=open(filename,'w')

                if (int(fetch)>0):
                    sublist=items[-1*(min(int(fetch), len(items))):]
                else:
                    sublist=items

                for emailid in sublist:
                    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
                    email_body = data[0][1] # getting the mail content
                    mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

                    header =  "["+mail["From"]+"] : Re:" + mail["Subject"]
                    
                    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
                    content = []
                    for part in mail.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True)
                            content.append(body)
                        else:
                            continue
                    email_obj = Email(header.decode('utf-8').strip(), '\n'.join(content).decode('utf-8').strip(), email_type)
                    email_list.append(email_obj)
                self.add_to_map(email_list)
            except:
                print('FAILED')

    def preview_email(self, email):
        OKBLUE = '\033[94m'
        ENDC = '\033[0m'
        print OKBLUE + email.header + ENDC

    def read_email(self, email):
        OKBLUE = '\033[94m'
        ENDC = '\033[0m'
        print OKBLUE + email.content + ENDC

    def get_email_address(self):
        return self.user + '@gmail.com'

class JayGame(Cmd):
    def __init__(self, email_client, jay):
        Cmd.__init__(self)
        self.email_client = email_client
        self.jay = jay
        self.current_email = self.email_client.get_random_email()
        self.inbox = [self.current_email]
        self.outbox = []
        self.inbox_zero = False

    def send_emails(self, opt_email_type_count_dict=None, opt_count=None):
        emails_to_send = []
        if opt_email_type_count_dict:
            for email_type, count in opt_email_type_count_dict.items():
                emails_to_send += self.email_client.get_emails(count, email_type)
        elif opt_count:
            # Send only the number of emails specified
            emails_to_send = self.email_client.get_emails(opt_count)
        else: 
            emails_to_send = self.email_client.get_emails()
        random.shuffle(emails_to_send)
        self.inbox = emails_to_send + self.inbox
        self.jay.speak('You got mail!')

    def do_read(self, args):
        """Given an email number, displays the contents of the email."""   
        try:
            current_email = self.inbox[int(args)]
            self.email_client.read_email(current_email)
        except:
            self.jay.speak('You need to tell me the number of the email you want to read!')

    def do_check(self, args):
        if len(self.inbox) == 0:
            self.inbox_zero = True
            self.jay.speak("CONGRATULATIONS! You've reached inbox zero!")
            self.send_emails({"EC": 15, "Jobs": 10, "Piazza": 5})
        """Given an email, displays the contents of the email."""
        for i, email in enumerate(self.inbox):
            if email != None:
                print i, self.email_client.preview_email(email)

    def do_reply(self, args):
        """Given an email number, replies to that email. Removes the email from 
        your inbox. """
        try:
            arg_list = args.split(' ')
            email_index = arg_list[0]
            reply = ' '.join(arg_list[1:])
            current_email = self.inbox[int(email_index)]
        except:
            self.jay.speak('You need to tell me the number of the email you want to reply to and then follow with the message you want to send!')
            return

        header =  "["+self.email_client.get_email_address()+"] :" + current_email.header
        content = reply
        email_type = "Response"
        reply = Email(header, content, email_type)
        self.email_client.preview_email(reply)
        self.email_client.read_email(reply)
        self.jay.speak('Response sent!')

        # Rules for response
        if current_email.type == "EC":
            self.send_emails({"EC": 10})
        else:
            self.send_emails(opt_count=3)

    def do_delete(self, args):
        # Remove email(s) from your inbox.
        if args == "":
            self.jay.speak('You need to tell me the number of the email(s) you want to delete or tell me if you want to delete all of them.')
        elif args.find('all') != -1:
            self.inbox = []
            self.do_check('')
        else:
            try:
                to_delete = args.split(' ')
                for ind in to_delete:
                    current_email = self.inbox[int(ind)]
                    if current_email.type == "Jobs":
                        if random.random() > .7:
                            self.send_emails({"Jobs": 7})
                    self.inbox[int(ind)] = None

                new_inbox = [email for email in self.inbox if email != None]
                self.inbox = new_inbox
                self.do_check('')
            except: 
                self.jay.speak("Sorry, I don't understand")
                self.jay.speak("You need to tell me the number of the email(s) you want to delete or tell me if you want to delete all of them.")

    def do_quit(self, args):
        """Quits the program."""
        self.jay.speak("Closing your email.")
        self.jay.speak("Bye!")
        raise SystemExit

class Jay():
    def speak(self, words):
        OKYELLOW = '\033[93m'
        ENDC = '\033[0m'
        print OKYELLOW + words + ENDC
        time.sleep(2)

def intro(jay):
    jay.speak("Hi, I'm Jay!")
    jay.speak("I help MIT students like you manage your email!")

    name = raw_input("What's your name?\n> ")
    while name == "":
        time.sleep(1)
        name = raw_input("Please, what's your name?\n")
    time.sleep(1)
    jay.speak("Great to meet you, " + name)
    jay.speak(name + ", I'm going to help you by turning email into a game where you want to keep your inbox as small as possible!")
    jay.speak("Hint: be careful about the emails you delete and reply to!")
    time.sleep(2)

if __name__ == '__main__':
    jay = Jay()
    intro(jay)
    ec = EmailClient()
    num_emails_per_filter = 5
    ec.populate_map(type_to_filter_dict, num_emails_per_filter)

    jay.speak("Oh!")
    jay.speak("You got mail!")
    prompt = JayGame(ec, jay)
    prompt.prompt = '> '
    prompt.cmdloop('')
