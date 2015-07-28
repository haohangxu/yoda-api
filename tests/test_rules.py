import logging
import unittest

from google.appengine.api import urlfetch
from google.appengine.ext import testbed

from language import tagger
from language.sentence import Sentence
from rules.yodish import *

class E2eTestCase(unittest.TestCase):
    """ Guide rule development with tests, we must. """
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()
        self.tagger = tagger.PartOfSpeechTagger(
            'http://text-processing.com/api/tag/', 
            'text'
        )

    def tearDown(self):
        self.testbed.deactivate()

    def test_conflicted_you_are(self):
        sut = Sentence(
            self.tagger.tag("You are conflicted.")
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Conflicted, you are.",
            sut.render()
        )

    def test_uppercase_i(self):
        sut = Sentence(
            self.tagger.tag("ii i i")
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Ii I I.",
            sut.render()
        )

    def test_much_anger(self):
        sut = Sentence(
            self.tagger.tag("I sense much anger in him.")
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Much anger in him, I sense.",
            sut.render() 
        )

    def test_away_put_weapons(self):
        sut = Sentence(
            self.tagger.tag("Put your weapons away.")
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Away put your weapons.",
            sut.render()
        )

    def test_multiple_sentences(self):
        source = "You are conflicted. Put your weapons away."
        sentences = self.tagger.tag(source).split('\n')
        actual = ""
        expected = "Conflicted, you are. Away put your weapons."
        for pos_tagged in sentences:
            s = Sentence(pos_tagged)
            apply_yodish_grammar(s)
            actual += s.render() + ' '
        actual = actual.strip()
        self.assertEqual(
            expected,
            actual
        )
