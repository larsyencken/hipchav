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
from collections import namedtuple
import urllib

import requests

ApiToken = namedtuple('ApiToken', 'token version')

URL_ROOMS_V1 = 'https://api.hipchat.com/v1/rooms/list'
URL_MESSAGES_V1 = 'https://api.hipchat.com/v1/rooms/message'

URL_ROOMS_V2 = 'https://api.hipchat.com/v2/room'
URL_MESSAGES_V2 = 'https://api.hipchat.com/v2/room/{0}/message'


class HipChavError(Exception):
    pass


def _get_auth_token():
    if 'HIPCHAT_V2_TOKEN' in os.environ:
        # prefer the newer api
        return ApiToken(os.environ['HIPCHAT_V2_TOKEN'], 2)

    elif 'HIPCHAT_V1_TOKEN' in os.environ:
        return ApiToken(os.environ['HIPCHAT_V1_TOKEN'], 1)

    raise HipChavError('please set HIPCHAT_V1_TOKEN or HIPCHAT_V2_TOKEN with '
                       'your credentials')


def list_rooms_v1(token):
    resp = _safe_get(URL_ROOMS_V1, token, format='json')
    return resp['items']


def list_rooms_v2(token):
    resp = _safe_get(URL_ROOMS_V2, token)
    return resp['items']


def list_rooms():
    api_token = _get_auth_token()
    if api_token.version == 1:
        rooms = list_rooms_v1(api_token.token)
    elif api_token.version == 2:
        rooms = list_rooms_v2(api_token.token)
    else:
        raise ValueError('unknown api version {0}'.format(api_token.version))

    return rooms


def message_room(room_name, message, color=None, notify=False,
                 sender='HipChav'):
    api_token = _get_auth_token()
    if api_token.version == 1:
        message_room_v1(api_token.token, room_name, message, color=color,
                        notify=notify, sender=sender)
    elif api_token.version == 2:
        message_room_v2(api_token.token, room_name, message, color=color,
                        notify=notify)

    else:
        raise ValueError('unknown api version {0}'.format(api_token.version))


def message_room_v1(token, room_name, message, color=None, notify=False,
                    sender='HipChav'):
    data = {'room_id': room_name,
            'from': sender,
            'message': message,
            'message_format': 'text',
            'notify': notify,
            'format': 'json'}
    if color:
        data['color'] = color

    _safe_post(URL_MESSAGES_V1, token,
               urllib.urlencode(data),
               headers={'content-type': 'application/x-www-form-urlencoded'})


def message_room_v2(token, room_name, message, color=None, notify=False):
    url = URL_MESSAGES_V2.format(room_name)
    data = {'message': message}
    if color:
        data['color'] = color

    if notify:
        data['notify'] = True

    _safe_post(url, token, json.dumps(data),
               headers={'content-type': 'application/json'})


def _safe_get(url, token, **kwargs):
    params = kwargs
    params['auth_token'] = token
    resp = requests.get(url, params=params)
    if not (200 <= resp.status_code < 300):
        raise HipChavError('got HTTP response {0}: {1}'.format(
            resp.status_code,
            resp.content,
        ))

    return resp.json()


def _safe_post(url, token, data, headers=None):
    resp = requests.post(url,
                         params={'auth_token': token},
                         headers=headers,
                         data=data)
    if not (200 <= resp.status_code < 300):
        raise HipChavError('got HTTP response {0}: {1}'.format(
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
    parser.add_option('-f', '--from', action='store', dest='sender',
                      help='Who the message will appear to be from '
                      '(v1 API only)')

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    cmd = args.pop(0)
    if cmd == 'rooms' and not args:
        rooms = list_rooms()
        rooms.sort(key=lambda r: r['name'].lower())
        for r in rooms:
            print(r['name'])

    elif cmd == 'message' and len(args) == 2:
        room, message = args
        message_room(room, message, notify=options.notify,
                     color=options.color, sender=options.sender)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
