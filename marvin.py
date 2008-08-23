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
from ConfigParser import ConfigParser

from jabberbot import JabberBot

import botcommands


class MarvinJabberBot(JabberBot):
    """Incredible... It's even worse than I thought it would be.
    
    I don't authorize connections by default, use the 'authorize' command
    
    Available commands:"""
    def bot_serverinfo( self, mess, args):
        """Displays information about the server."""
        #version = open('/proc/version').read().strip()
        #loadavg = open('/proc/loadavg').read().strip()
        #return '%s\n\n%s' % ( version, loadavg, )
        return botcommands.getServerInfo()

    def bot_url( self, mess, args):
        """Returns a shorten form of url."""
        # only process the first "word"
        if args == '':
            return "Syntax: url http://google.com"
        argList = []
        argList = args.split()
        return botcommands.getShortUrl(argList[0])
    
    def bot_length( self, mess, args):
        """Returns how long the specified message is."""
        return len(args)

    def bot_md5( self, mess, args):
        """Returns MD5 hash in hexadecimal format."""
        return hashlib.md5(args).hexdigest()
    
    def bot_lookupmd5( self, mess, args):
        """Attempts to lookup the value of an MD5 hash."""
        return botcommands.lookupMd5(args)

    def bot_sha1( self, mess, args):
        """Returns SHA1 hash in hexadecimal format."""
        return hashlib.sha1(args).hexdigest()

    def bot_authorize( self, mess, args):
        """Have me authorize your subscription to my presence."""
        # also sends a subscribe request
        # you authorize the stripped version of JID object
        f = mess.getFrom().getStripped()
        self.conn.Roster.Authorize( f)
        self.conn.Roster.Subscribe( f)
        return "Authorized."

    def bot_deauthorize( self, mess, args):
        """Remove yourself from my roster."""
        f = mess.getFrom().getStripped()
        self.conn.Roster.Unsubscribe( f)
        # we'll keep them authorized though
        #self.conn.Roster.Unauthorize( f)
        return "Sorry to see you go"

    #def bot_sendsubscribe( self, mess, args):
    #    f = mess.getFrom().getStripped()
    #    self.conn.Roster.Subscribe( f)
    #    return 'Subscription Sent.'

    #def bot_getsubscribe( self, mess, args):
    #    jid = mess.getFrom().getStripped()
    #    subscribe = self.conn.Roster.getSubscription( jid)
    #    return subscribe
    
    #def bot_showroster( self, mess, args):
    #    """show everyone I know"""
    #    roster = self.conn.Roster.getItems()
    #    return '\n'.join(roster)

    def bot_reload( self, mess, args):
        """Reloads the bot."""
        self.quit()
        return None

    def bot_time( self, mess, args):
        """Displays current server time."""
        return str(datetime.datetime.now())

    def bot_rot13( self, mess, args):
        """Returns passed arguments rot13'ed."""
        return args.encode('rot13')

    def bot_whoami( self, mess, args):
        """Tells you your username."""
        return mess.getFrom()

    def bot_fortune( self, mess, args):
        """Get a random quote."""
        # taken from snakebot jabber bot
        fortune = os.popen('/usr/games/fortune').read()
        return fortune

    def bot_spell( self, mess, args):
        """Checks the spelling of a word"""
        return botcommands.spellCheck(args)


if __name__ == '__main__':
    Config = ConfigParser()
    Config.read('config.ini')
    username = Config.get('jabberbot', 'username')
    password = Config.get('jabberbot', 'password')
    
    bot = MarvinJabberBot(username,password)
    bot.serve_forever()
    # error handling is handled in serve_forever, don't think it is needed
    # here.  At least it's not as important

