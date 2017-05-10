#!/usr/bin/python
import email, getpass, imaplib, os
from cmd import Cmd
import random
from collections import defaultdict
import time
import re
import datetime
import nltk
from Markov import Markov
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

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
        # Get user email information
        self.user = raw_input("your email (without the @gmail.com): ")
        pwd=getpass.getpass()

        print('Loading...')
        
        # of emails to fetch per category.
        fetch = num_emails

        # connecting to the gmail imap server
        m = imaplib.IMAP4_SSL("imap.gmail.com")
        m.login(self.user+str("@gmail.com"),pwd)
        m.select("INBOX") # here you a can choose a mail box like INBOX instead
        # use m.list() to get all the mailboxes
        
        email_list = []

        # Search for all emails sent within the last 3 days
        date = (datetime.date.today() - datetime.timedelta(3)).strftime("%d-%b-%Y")
        result, data = m.uid('search', None, '(SENTSINCE {date})'.format(date=date))
        items = data[0].split()

        # Only take the first "num_emails" IDs from the result
        if (int(fetch)>0):
            sublist=items[-1*(min(int(fetch), len(items))):]
        else:
            sublist=items

        # Create Email instances and save them to the email list.
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
        # Add the email list to the client's map of emails
        self.add_to_map(email_list)

    def populate_map(self, type_to_filter_dict, num_emails_per_filter):
        self.user = raw_input("your email (without the @gmail.com): ")
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

class Jay():
    """Jay is the character that represents the email assistant's speech with a 
    yellow voice"""
    def speak(self, words):
        OKYELLOW = '\033[93m'
        ENDC = '\033[0m'
        print OKYELLOW + words + ENDC
        time.sleep(2)

class EmailBot:
    """The EmailBot class describes a bots that can be trained on Email instances 
    and """
    def __init__(self, name, opt_emails=None):
        self.name = name
        # Set the "voice" of the email bot to be a random color from selection:
        # purple, magenta, green, red
        self.voice = random.choice(['\033[95m','\033[96m', '\033[92m', '\033[91m'])
        
        if opt_emails:
            # Initialize the bot with a markov model w/ given list of email
            self.markov = self.build_model(opt_emails)
            # List of Email objects fed to the bot
            self.emails = opt_emails
        else: 
            self.markov = None
            self.emails = []
        # List of emails that have not yet been incorporated into the markov model.
        self.new_emails = []

    def speak(self, words):
        ENDC = '\033[0m'
        print self.voice + words + ENDC
        time.sleep(2)

    def ask_yes_no(self, question):
        self.speak(question)
        res = raw_input('>')
        return res.find('yes') != -1 or res.find('yeah') != -1 or res.find('ok') != -1 or res == 'k' or res == 'y'

    def introduce(self):
        self.speak("hello, i'm " + self.name + "!")
    
    def react_to_visit(self):
        self.introduce()
        if len(self.emails + self.new_emails) < 13:
            self.speak("Wahhh, I'm hungry")
        else:
            if random.random() < .5:
                yes = self.ask_yes_no("Do you want to see my writing?")
                if yes:
                    self.speak(self.generate_email())
                else:
                    yes = self.ask_yes_no("How about a poem?")
                    if yes:
                        self.speak(self.generate_poem())
            else: 
                yes = self.ask_yes_no("Do you want to see my poem?")
                if yes:
                    self.speak(self.generate_poem())
                else:
                    yes = self.ask_yes_no("How about my writing?")
                    if yes:
                        self.speak(self.generate_email())

    def build_model(self, emails):
        text_list = [email.content for email in emails]
        text =  ' '.join(text_list)
        text_model = Markov(text)
        return text_model

    def feed(self, email):
        self.new_emails.append(email)
        potential_exclamations = ["MMMMMM dat good.", "Emails are so delicious", "Nom, nom ,nom.", "Emails make me feel so good.", "Thanks for such a juicy email!"]
        self.speak(random.choice(potential_exclamations))

    def update(self):
        if len(self.new_emails) != 0:
            # Add the new emails to the markov model.
            text_list = [email.content for email in self.new_emails]
            new_email_text =  ' '.join(text_list)
            self.markov.update(new_email_text)
            # Update self.emails and clear list of unincorpoarted emails.
            self.emails = self.emails + self.new_emails
            self.new_emails = []

    def generate_email(self, length=10):
        """Return a string representing an email containing a header and a body."""
        self.update()
        # Generate the emails
        lines = []
        line_count = 0
        while line_count < length:
            sent = self.markov.make_sentence()
            if sent != None:
                lines.append(sent)
                line_count +=1
            else:
                print(sent)
        email_body = '\n'.join(lines)
        email_header = random.choice(get_best_trigrams(filter(email_body),5))
        return email_header.decode('utf-8').strip() + "\n" + email_body.decode('utf-8').strip()

    def generate_poem(self, num_lines=7):
        def get_poem_title(poem_content):
            return get_best_trigrams(poem_content, 1)[0]

        self.update()
        # Generate the emails
        lines = []
        line_count = 0
        while line_count < num_lines:
            sent = self.markov.make_sentence()
            if sent != None:
                lines.append(sent)
                line_count +=1
            else:
                print(sent)
        poem = '\n'.join(lines)
        title = get_poem_title(poem)
        return title.decode('utf-8').strip() + '\n' + poem.decode('utf-8').strip()

# Helper functions for generating emails and poems
def get_best_trigrams(text, num_best):
    tokenized_words = nltk.tokenize.word_tokenize(text.decode('utf-8').strip())
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = nltk.collocations.TrigramCollocationFinder.from_words(tokenized_words)
    best_ngrams = finder.nbest(trigram_measures.pmi, num_best)
    to_return =  [' '.join(list(best_ngram)) for best_ngram in best_ngrams]
    return to_return

def filter(poem):
    # filter out >
    p = re.compile('(>)')
    poem = p.sub('', poem)
    # strip extra spaces surrounding new lines
    return '\n'.join([line.strip() for line in poem.split('\n')])

class EmailBotsGame(Cmd, object):
    def __init__(self, jay, email_client):
        super(EmailBotsGame, self).__init__()
        self.jay = jay
        self.email_client = email_client
        self.keepbot = EmailBot('keepbot', [self.email_client.get_random_email() for i in range(10)])
        self.deletebot = EmailBot('deletebot',  [self.email_client.get_random_email() for i in range(10)])
        self.first_feed = True
    
    def do_visit(self, args):
        """Visit your emailbots"""
        if ' '.join(args).find('keepbot') != -1:
            botname = 'keepbot'
        elif ' '.join(args).find('deletebot') != -1:
            botname = 'deletebot'
        else:
            self.jay.speak("Which bot do you want to visit? keepbot or deletebot?")
            botname = raw_input('>')
            
        while botname not in set(['keepbot', 'deletebot', 'quit']):
            self.jay.speak("Sorry, I don't know that bot. You can QUIT this visit if you want.")
            botname = raw_input('>')
        if botname == 'keepbot':
            self.jay.speak("Here's keepbot!")
            self.keepbot.react_to_visit()
        elif botname == 'deletebot':
            self.jay.speak("Here's deletebot!")
            self.deletebot.react_to_visit()
        else:
            self.jay.speak("You don't have to visit your bots right now.")
            self.jay.speak("Try FEEDing them.")

    def do_listen(self, args):
        """Will listen to the emailbot's poem or writing based on what bot your mention and 
        what kind of writing you mention"""
        poem = args.contains('poem')
        deletebot = args.contains('deletebot')

        if deletebot:
            if poem:
                self.deletebot.generate_poem()
            else:
                self.deletebot.generate_email()
        else:
            if poem:
                self.keepbot.generate_poem()
            else:
                self.keepbot.generate_email()

                
    def do_feed(self, args):
        """Feed your email bots by keeping or deleting your emails."""
        if self.first_feed:
            self.jay.speak("Remember, deletebot gets to eat the emails you delete and keepbot eats the emails you don't delete!")
            self.jay.speak('Let me know when you want to STOP feeding!')
            self.first_feed = False
        delete = None
        while delete != 'stop' and delete != 'STOP':
            # pull email from database
            mail = self.email_client.get_random_email()
            self.jay.speak('Do you want to delete this email?')
            ec.preview_email(mail)
            delete = raw_input('>')
            if delete.lower().find('no') != -1:
                self.keepbot.feed(mail)
            elif delete != 'stop' and delete != 'STOP':
                self.deletebot.feed(mail)
            else:
                break
        self.jay.speak("Done feeding!")
    def do_quit(self, args):
        """Quits the program."""
        self.jay.speak("Closing your email.")
        self.jay.speak("Bye!")
        raise SystemExit

def intro(jay):
    jay.speak("Hi, I'm Jay!")
    jay.speak("I'm here to help you raise your emailbots!")
    jay.speak("What's your name?")
    name = raw_input("")
    while name == "":
        time.sleep(1)
        name = raw_input("Please, what's your name?\n")
    time.sleep(1)
    jay.speak("Great to meet you, " + name)
    jay.speak("In this game, you have two emailbots: keepbot and deletebot.")
    jay.speak("In order to feed them you will need to pull from your email. Please enter your account info below.")
    time.sleep(2)

if __name__ == '__main__':
    j = Jay()
    ec = EmailClient()
    num_emails = 100
    intro(j)
    ec.populate_basic_map(num_emails)

    j.speak("As you might think, keepbot is fed all the emails you decide to keep and deletebot gets fed all the ones you delete.")
    time.sleep(2)
    j.speak("Your bots are babies right now so you need to FEED each of them at least 3 emails before they'll stop crying and converse with you.")
    time.sleep(2)
    j.speak("You can start off by VISITing them.")

    ebots = EmailBotsGame(j, ec)
    ebots.prompt = '> '
    ebots.cmdloop('')


