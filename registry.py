#! /usr/bin/python
# -*- coding: utf-8-

import urllib2
import json


def register(server_url, index):
    response = urllib2.urlopen(
            'http://%s/robo/register?index=%s' % (server_url, index))
    obj = json.loads(response.read())
    if 'succeeded' in obj:
        return obj['succeeded']
    return False

def delete(server_url, index):
    response = urllib2.urlopen(
            'http://%s/robo/delete?index=%s' % (server_url, index))
    obj = json.loads(response.read())
    if 'succeeded' in obj:
        return obj['succeeded']
    return False


if __name__ == '__main__':
    import sys
    index = "252"
    if len(sys.argv) == 2:
        index = sys.argv[1]
    server_url = "localhost:5000"
    print 'Registering...'
    if register(server_url, index):
        print "Success:)"
        """
        print 'Deleting...'
        if delete(server_url, index):
            print "Success:)"
        else:
            print "Failure:("
        """
    else:
        print "Failure:("
