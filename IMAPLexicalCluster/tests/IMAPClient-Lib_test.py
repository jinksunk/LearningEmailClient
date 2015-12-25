import unittest
import logging
import IMAPLexicalCluster
import imapclient

class TestSemanticIMAPClient(unittest.TestCase):
    HOST = 'mail.semantiknit.com'
    USER = 'cstras@semantiknit.com'
    PASS = 'VTz6tmQ4'
    BADPASS = 'goozlebomb'
    SSL = False
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        self.sic = IMAPLexicalCluster.SemanticIMAPClient.SemanticIMAPClient(
                self.HOST, self.USER, self.PASS, True)

    def tearDown(self):
        self.sic.logout()

    def test_imapconnect(self):
        '''
        First time should fail with an Authentication failed message:
        '''
        sic = None
        with self.assertRaises(imapclient.IMAPClient.Error):
            sic = IMAPLexicalCluster.SemanticIMAPClient.SemanticIMAPClient(
                    self.HOST, self.USER, self.BADPASS, True)

        ''' Todo: Add test of SSL properties '''

    def test_getFoldersWithMessages(self):
        flist = self.sic._getFoldersWithMessages()
        print (flist[0:3])

    def test_getCommonWordsInMail(self):
        flist = self.sic._getFoldersWithMessages()
        for i in range(0,3):
            print ("Getting the common words in folder %s"%flist[i][0])
            wlist = self.sic._getCommonWordsInFolder(flist[i][0], 100)
            expectedCommonWords = wlist[0]
            logging.debug(expectedCommonWords)
            print(wlist[1][0:9])
            logging.debug("Testing %d == %d..."%(len(wlist[1]),
                expectedCommonWords))
            self.assertEqual(len(wlist[1]),expectedCommonWords)

    def test_buildLexicalClusterScore(self):
        flist = self.sic._getFoldersWithMessages()
        #fscore = sic._getLexicalClusterScore('Academic.ISU.research.Positions')

