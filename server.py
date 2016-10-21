import os
import sys
import email
import errno
import mimetypes
from inbox import Inbox
import random
import email_util

#https://github.com/kennethreitz/inbox.py/blob/master/inbox.py
inbox = Inbox()
directory = "/tmp"

#https://docs.python.org/3/library/email-examples.html
def unpack(body):
    msg = email.message_from_tsring(body)
    filenames = []
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        # Applications should really sanitize the given filename so that an
        # email message can't be used to overwrite important files
        filename = "print-%d.pdf" % random.randint(10000000)
        with open(os.path.join(directory, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))
        filenames.append(filename)
    return filenames

@inbox.collate
def handle(to, sender, body, **kwargs):
  filenames = unpack(body)
  email_util.send_email("Received",kwargs.get(subject,"Print Submission"),sender,to)
  
inbox.serve(address='0.0.0.0', port=25)
