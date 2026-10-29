"""Put back the dates the list's archive lost when it moved to OSGeo.

usage: fix-rebuilt-dates.py FILE.mbox [...]

grass-stats came to lists.osgeo.org in November 2007, and the import wrote
that moment (14 November 2007, 16:58) into the Date line of almost every
message from May 2001 on. The envelope line above each message ("From user
at domain  date") kept the day the message arrived, and pipermail filed each
message in the month of that day. Where the Date line is more than a day
from the envelope, or empty, this writes the envelope's date in its place, in
the same form. It was run once, on the files up to November 2007.

The text archive also leaves a line of a message's text that starts with
"From " as it is, and the parser takes it for the start of a new message, so
the rest of that message is lost. Such a line is written ">From ", as an
mbox file keeps it.

Adapted from r-mailing-lists/statnet-help's tools/fix-rebuilt-dates.py.
"""
import re
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

START = re.compile(r"(?m)^(?=From \S+(?: at \S+)?  \w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4}$)")
ENVELOPE = re.compile(r"From \S+(?: at \S+)?  (\w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4})\n")
DATE = re.compile(r"(?m)^Date:[ \t]*(.*)$")
CTIME = "%a %b %d %H:%M:%S %Y"


def when(text):
    """The Date line's moment, written as pipermail does or as the message did."""
    try:
        return datetime.strptime(" ".join(text.split()), CTIME)
    except ValueError:
        pass
    try:
        moment = parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError):
        return None
    return moment.astimezone(timezone.utc).replace(tzinfo=None) if moment.tzinfo else moment


BODY_FROM = re.compile(r"(?m)^From ")


def fix(message):
    env = ENVELOPE.match(message)
    if not env:
        return message, False
    head, sep, body = message.partition("\n\n")
    body = BODY_FROM.sub(">From ", body)
    date = DATE.search(head)
    stamp = when(env.group(1))
    current = when(date.group(1)) if date else None
    if current is not None and abs((current - stamp).total_seconds()) <= 86400:
        return head + sep + body, False
    line = "Date: " + env.group(1)
    head = DATE.sub(lambda _: line, head, count=1) if date else head + "\n" + line
    return head + sep + body, True


def main(paths):
    for path in paths:
        raw = open(path, "rb").read().decode("latin-1")
        parts = START.split(raw)
        fixed = [fix(p) if p.startswith("From ") else (p, False) for p in parts]
        changed = sum(c for _, c in fixed)
        open(path, "wb").write("".join(p for p, _ in fixed).encode("latin-1"))
        print(f"{path}: {changed} of {sum(p.startswith('From ') for p in parts)} dates put back")


if __name__ == "__main__":
    main(sys.argv[1:])
