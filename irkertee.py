#!/usr/bin/env python
"""
irkertee - tee data to an irker relay agent

Copyright (c) 2012 William Pitcock <nenolod@dereferenced.org>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

This software is provided 'as is' and without any warranty, express or
implied. In no event shall the authors be liable for any damages arising
from the use of this software.
"""

import json, socket, sys

class IrkerRelayer:
    "A relayer which relays messages to irker server."
    def __init__(self, dest, to):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = dest
        self.to = to
    def __del__(self):
        self.sock.close()
    def write(self, line):
        envelope = {'to': self.to, 'privmsg': line}
        message = json.dumps(envelope)
        self.sock.sendto(message + "\n", (self.dest, 6659))
    def relay(self, inbuf=sys.stdin, outbuf=sys.stdout):
        while True:
            try:
                line = inbuf.readline()
            except:
                exit(-1)
            if not line: break
            self.write(line)
            outbuf.write(line)

if len(sys.argv) < 3:
    print "usage: irkertee destination irc://... [irc://...]"
    exit(-1)

dest = sys.argv[1]
to = []
for i in sys.argv[2:]:
    to.append(i)

IrkerRelayer(dest, to).relay()
