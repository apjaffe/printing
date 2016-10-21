import os
import sys
import email
import errno
import mimetypes
from inbox import Inbox

#https://github.com/kennethreitz/inbox.py/blob/master/inbox.py
inbox = Inbox()
directory = "/tmp"

#https://docs.python.org/3/library/email-examples.html
def unpack(body):
    msg = email.message_from_tsring(body)
    counter = 1
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        # Applications should really sanitize the given filename so that an
        # email message can't be used to overwrite important files
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = '.pdf'
            filename = 'part-%03d%s' % (counter, ext)
        counter += 1
        with open(os.path.join(directory, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))

@inbox.collate
def handle(to, sender, body):
  unpack(body)
  
inbox.serve(address='0.0.0.0', port=4467)
