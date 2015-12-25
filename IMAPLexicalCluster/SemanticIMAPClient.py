"""
Author: Chris Strasburg

The purpose of this class is to provide an interface to an IMAP account which
facilitates the learning and suggestions of mail folder recommendations
based on lexical clustering of existing messages.

This class contains methods which:
    * Construct and maintain an IMAP connection
    * List all folders in an IMAP account
    * Retrieve attributes of all messages in a particular IMAP folder
    * Return a list of suggested folders with confidence scores for a 
      particular IMAP message.
"""

import imapclient
import logging
import nltk
from nltk.corpus import PlaintextCorpusReader


class SemanticIMAPClient():
    """
    This class represents an interface to an imap mailbox which
    includes suggestions for semantic tagging of messages based on
    existing folders' message contents.
    """

    def __init__(self, host, username, password, ssl):
        """ Perform initialization: 
            * host = The hostname to connect to
            * username = The username to connect with
            * password = The password to connect with
            * ssl = Whether to use SSL or not (True or False)
        """
        self.username = username
        self.hostname = host
        self.server = imapclient.IMAPClient(host, use_uid=True, ssl=ssl)
        self.server.login(username, password)

    def _getFoldersWithMessages(self):
        """
        Return a list of all of the folders on the server which contain 
        messages, along with message counts and status.
        """
        flist = [x[2] for x in self.server.list_folders()]
        retlist = [[x,
                    self.server.folder_status(
                      x,
                      ('MESSAGES'))['MESSAGES'.encode('ascii')
                  ]] for x in flist]
        return retlist

    ''' TODO: Define a decorator for getFoldersWithMessages which implements a
        cache / checks modified date.  We don't want to have to rebuild
        corpi if we don't need to.'''

    def _getCommonWordsInFolder(self, folder, numWords):
        """
        Given a folder to process and a limit on the number of words to
        include, return a list of '[numWords, [(Word, frequency), ...]]'.
        """
        utf8text = self._buildTextFromFolder(folder)
        tokenizer = nltk.tokenize.RegexpTokenizer(r'[\w\'\-]{3,}')
        tokens = tokenizer.tokenize(utf8text)
        nutext = nltk.Text(tokens)
        fdist = nltk.FreqDist(nutext)
        logging.debug("Length of frequency list: %d"%len(fdist))
        return [len(fdist), fdist.most_common(numWords)]

    def _buildLexicalClusterScore(self, folder):
        """
        Given a folder, evaluate it for its lexical content
        """

    def _buildTextFromFolder(self, folderName):
        """
        Given a folder name on the server, build an NLTK corpus from it.
        This method is READ ONLY.
        """
        ''' Get all messages in the folder, or maybe randomly sample some of
            them.  We probably only want the plain text part, skpping 
            attachments, binary data, etc...
            For now, let's just skip multipart messages entirely
        '''
        mparts = 0 # Track the number of multipart messages we see

        # Switch to the folder?
        folderStatus = self.server.select_folder(folderName, readonly=True)

        # Get a list of messages in the folder to determine how many there are:
        uidList = self.server.search()
        messageStructs = self.server.fetch(uidList, 'BODYSTRUCTURE')
        fullMlist = list()

        # For each message, fetch the BODYSTRUCTURE to see if it is multipart
        for m in messageStructs:
            if messageStructs[m][b'BODYSTRUCTURE'].is_multipart:
                mparts = mparts + 1
            else:
                # If it is not multipart, fetch the full BODY
                fullMlist.append(m)
        messageBodies = self.server.fetch(fullMlist, 'BODY[TEXT]')

        utf8String = ''.join([messageBodies[b][b'BODY[TEXT]'].decode() \
                for b in messageBodies])

        # Switch back *from* the folder?
        logging.info("Found %d multipart messages in %s".format(mparts,
            folderName))

        return utf8String

    def logout(self):
        """
        Just close the IMAP connection.
        """
        self.server.logout()
