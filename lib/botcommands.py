#!/usr/bin/env python
# vim:ts=4:sw=4:expandtab:ft=python:fileencoding=utf-8
"""Various Bot functions

"""

import urllib2
from xml.dom import minidom
import enchant

def getServerInfo():
    """Get's various server information"""
    version = open('/proc/version').read().strip()
    loadavg = open('/proc/loadavg').read().strip()
    return '%s\n\n%s' % ( version, loadavg, )

def getShortUrl( longUrl):
    """Uses the http://is.gd/ service to shorten a url"""
    basePath = 'http://is.gd/api.php?longurl='
    try:
        fh = urllib2.urlopen(basePath + longUrl)
    except urllib2.HTTPError, inst:
        # is.gd probably gave us a reason why it didn't work
        return inst.fp.readline()
    except urllib2.URLError, inst:
        # a non http error, may be a typo
        return "Error: %s" % inst.reason
    else:
        shortUrl = fh.readline()
        fh.close()
        return shortUrl

def lookupMd5( hash):
    """Uses http://md5.rednoize.com to lookup md5 hashes"""
    if len(hash) <> 32:
        return "Error: invalid md5 hash"
    try:
        fh = urllib2.urlopen('http://md5.rednoize.com/?q=' + hash + '&xml')
    except urllib2.HTTPError, inst:
        # maybe we got a reason why it didn't work
        return inst.fp.readline()
    except urllib2.URLError, inst:
        # a non http error, may be a typo
        return "Error: %s" % inst.reason
    else:
        doc = minidom.parse(fh)
        fh.close()
    result = doc.getElementsByTagName('ResultString')
    return result.item(0).firstChild.data

def spellCheck( word):
	"""Uses python-enchant to check spelling."""
	if len(word) <= 0:
		return "Error: no word specified"
	d = enchant.Dict("en_US")
	if d.check(word) == True:
		return "'" + word + "' is spelled correctly."
	else:
		# only showing up to the first 4 possibilites
		return "Possible spellings for '" + word + "': " + ', '.join(d.suggest(word)[:4])
