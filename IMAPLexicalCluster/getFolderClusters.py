#!/usr/local/bin/python3

''' A test driver for the various imap clustering utilities included in 
    this project.

    TODO:
    12/4/2014 - The first aspect is to read a set of imap folders and
    perform lexical analysis on the messages contained within to determine
    a folder 'profile'.  If many messages are present, 100 will be selected at
    random.
'''

import imaplib
import getpass

def getImapObject(imapserver='', imapuser='', imappass=''):
    '''
    Return a ready-to-use imap connection object.
    '''
    imapcon = imaplib.IMAP4_SSL(imapserver)
    imapcon.login(imapuser, imappass)
    return imapcon

def getImapFolderList(icon, Parent=None):
    '''
    Return a list of all imap folders on the server.
    '''
    fList = icon.list()
    return fList

def processMailbox(icon, mailbox):
    '''
    Return a dict of lexical strings and word counts for the given mailbox.
    '''
    mcount = icon.select(mailbox)
    print("{0}\t{1}".format(mailbox,mcount))

    if mcount[0] == "OK":
        ''' Is the number of messages > 100?  If so pick some at random. '''
        count = int(mcount[1][0].decode("utf-8"))
        if count > 2:
            count = 2 
        ''' Get text for the first 100 messages '''
        for i in range(0,count):
            curMess = icon.fetch(i, "(UID BODY[TEXT])")
            print ("Message: {0}".format(curMess))


if __name__ == '__main__':
    '''
    Run simple test code to start with.
    '''
    imapserver = "mail.semantiknit.com"
    imapuser = "cstras@semantiknit.com"
    imappass = getpass.getpass(prompt='IMAP Password: ')

    icon = getImapObject(imapserver, imapuser, imappass)
    folders = getImapFolderList(icon)

    sflist = list()
    if folders[0] == "OK":
        for li in folders[1]:
            sflist.append(li.decode("utf-8").split('"')[3])

    print ("Folder list: " )
    print ("\n\t".join([x for x in sflist]))

    processMailbox(icon, sflist[18])

    print("Done.")


