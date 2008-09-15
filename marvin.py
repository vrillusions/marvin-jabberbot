#!/usr/bin/env python
# vim:ts=4:sw=4:expandtab:ft=python:fileencoding=utf-8
"""Marvin jabber bot.

A jabber bot made to play with jabber, python, etc and hopefully still be
useful.

"""

# $Id$
__version__ = "$Rev$"

import datetime
import hashlib
import os
import string
from random import choice
from ConfigParser import ConfigParser

from jabberbot import JabberBot

import botcommands


class MarvinJabberBot(JabberBot):
    """Incredible... It's even worse than I thought it would be."""
    def connectCallback(self):
        """Called after successful connection but before processing"""
        # would have like to add the RegisterHandlers here but it doesn't appear to work
        pass
    
    def subscribe_handler(self, conn, pres):
        """Handles requests from users to subscribe to bot"""
        # for some reason this HAS to be set before the initial connection. Place the
        # following in the connect() function of main file
        #   conn.RegisterHandler('presence', self.subscribe_handler, 'subscribe')
        jid = pres.getFrom().getStripped()
        self.conn.Roster.Authorize(jid)
        self.conn.Roster.Subscribe(jid)
    
    def unsubscribed_handler(self, conn, pres):
        """Handles notifications that the user has unsubscribed (removed) the bot"""
        # place follwoing in connect() function of main file
        #   conn.RegisterHandler('presence', self.unsubscribed_handler, 'unsubscribed')
        jid = pres.getFrom().getStripped()
        self.conn.Roster.delItem(jid)
    
    def bot_serverinfo(self, mess, args):
        """HIDDEN Displays information about the server."""
        #version = open('/proc/version').read().strip()
        #loadavg = open('/proc/loadavg').read().strip()
        #return '%s\n\n%s' % ( version, loadavg, )
        return botcommands.getServerInfo()

    def bot_url(self, mess, args):
        """Returns a shorten form of url."""
        # only process the first "word"
        if args == '':
            return "Syntax: url http://google.com"
        argList = []
        argList = args.split()
        return botcommands.getShortUrl(argList[0])
    
    def bot_length(self, mess, args):
        """Returns how long the specified message is."""
        return len(args)

    def bot_md5(self, mess, args):
        """Returns MD5 hash in hexadecimal format."""
        return hashlib.md5(args).hexdigest()
    
    def bot_lookupmd5(self, mess, args):
        """Attempts to lookup the value of an MD5 hash."""
        return botcommands.lookupMd5(args)

    def bot_sha1(self, mess, args):
        """Returns SHA1 hash in hexadecimal format."""
        return hashlib.sha1(args).hexdigest()

    def bot_reload(self, mess, args):
        """HIDDEN Reloads the bot."""
        self.quit()
        return None

    def bot_time(self, mess, args):
        """Displays current server time."""
        return str(datetime.datetime.now()) + " EST/EDT"

    def bot_rot13(self, mess, args):
        """Returns passed arguments rot13'ed."""
        return args.encode('rot13')

    def bot_whoami(self, mess, args):
        """Tells you your username."""
        return mess.getFrom()

    def bot_fortune(self, mess, args):
        """Get a random quote."""
        # taken from snakebot jabber bot
        fortune = os.popen('/usr/games/fortune').read()
        return fortune

    def bot_spell(self, mess, args):
        """Checks the spelling of a word"""
        return botcommands.spellCheck(args)
    
    def bot_random(self, mess, args):
        """Returns a random 32 character string useful for passwords"""
        chars = string.letters + string.digits
        randomOutput = ''
        for i in range(32):
            randomOutput = randomOutput + choice(chars)
        return randomOutput

    def bot_password(self, mess, args):
        """Similar to random command but tries to produce a pronounceable password"""
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        numbers = string.digits
        randomPassword = ( choice(consonants) + choice(vowels) + choice(consonants) + 
            choice(vowels) + choice(consonants) + choice(vowels) + choice(consonants) + 
            choice(numbers) )
        return randomPassword
    
    def bot_ascii2hex(self, mess, args):
        """Takes an ascii string and converts it to hexadecimal."""
        return args.encode('hex')
    
    def bot_hex2ascii(self, mess, args):
        """Takes a hex string and converts it to ascii."""
        return args.decode('hex')
    
    def bot_dbg(self, mess, args):
        """HIDDEN used for debugging"""
        jid = mess.getFrom().getStripped()
        jidobj = mess.getFrom()
        #jid = 'vrillusions@gmail.com'
        subscribe = self.conn.Roster.getSubscription( jid)
        ask = self.conn.Roster.getAsk(jid)
        show = self.conn.Roster.getShow(jidobj)
        group = self.conn.Roster.getGroups(jid)
        result = 'sub:%s ask:%s show:%s group:%s' % (subscribe, ask, show, group)
        #result = self.conn.Roster.getRawItem(jid)
        #result = self.conn.Roster.getItems()
        return result


if __name__ == '__main__':
    Config = ConfigParser()
    Config.read('config.ini')
    username = Config.get('jabberbot', 'username')
    password = Config.get('jabberbot', 'password')
    adminJid = Config.get('jabberbot', 'adminjid')
    
    bot = MarvinJabberBot(username,password)
    bot.serve_forever(bot.connectCallback())
    # error handling is handled in serve_forever, don't think it is needed
    # here.  At least it's not as important

