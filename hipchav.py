#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hipchav.py
#  hipchav
#

"""
A command-line hipchat client.
"""

from __future__ import absolute_import, print_function, division

import os
import sys
import optparse
import json

import requests

URL_ROOMS = 'https://api.hipchat.com/v2/room'
URL_MESSAGES = 'https://api.hipchat.com/v2/room/{0}/message'


def _get_auth_token():
    if 'HIPCHAT_AUTH_TOKEN' not in os.environ:
        raise Exception('please set HIPCHAT_AUTH_TOKEN with your token')

    return os.environ['HIPCHAT_AUTH_TOKEN']


def list_rooms(token=None):
    token = token or _get_auth_token()
    resp = _safe_get(URL_ROOMS, token)
    return resp['items']


def cmd_list_rooms():
    rooms = list_rooms()
    rooms.sort(key=lambda r: r['name'].lower())
    for r in rooms:
        print(r['name'])


def cmd_message_room(room_name, message, color=None, notify=False):
    message_room(room_name, message, color=color, notify=notify)


def message_room(room_name, message, color=None, notify=False, token=None):
    token = token or _get_auth_token()
    url = URL_MESSAGES.format(room_name)
    data = {'message': message}
    if color:
        data['color'] = color

    if notify:
        data['notify'] = True

    _safe_post(url, token, **data)


def _safe_get(url, token, **kwargs):
    params = kwargs
    params['auth_token'] = token
    resp = requests.get(url, params=params)
    if not (200 <= resp.status_code < 300):
        raise IOError('got HTTP response {0}: {1}'.format(
            resp.status_code,
            resp.content,
        ))

    return resp.json()


def _safe_post(url, token, **kwargs):
    data = json.dumps(kwargs)
    resp = requests.post(url,
                         params={'auth_token': token},
                         headers={'content-type': 'application/json'},
                         data=data)
    if not (200 <= resp.status_code < 300):
        raise IOError('got HTTP response {0}: {1}'.format(
            resp.status_code,
            resp.content,
        ))

    if resp.content:
        return resp.json()


def _create_option_parser():
    usage = \
"""%prog rooms
       %prog message [-c color] <room> <message>

Send notifications to HipChat rooms on the command-line. Use the rooms command
to list the available rooms, and the message command to send a message to one."""  # nopep8

    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--color', action='store', type='choice',
                      dest='color', choices=['yellow', 'red', 'green',
                                             'purple', 'gray', 'random'],
                      default='yellow',
                      help='Color the message [yellow]')
    parser.add_option('-n', '--notify', action='store_true', dest='notify',
                      help='Notify the people in the room [false]')

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    cmd = args.pop(0)
    if cmd == 'rooms' and not args:
        cmd_list_rooms()

    elif cmd == 'message' and len(args) == 2:
        room, message = args
        cmd_message_room(room, message, notify=options.notify,
                         color=options.color)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
