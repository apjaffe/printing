from subprocess import Popen, PIPE

def send_email(text, subj, to, frm):
  proc = Popen(["mailx","-s",subj,to, "-r", frm], stdin=PIPE)
  proc.stdin.write(text)
  proc.stdin.close()
  proc.wait()
