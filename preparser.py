#!/usr/bin/python

import os
import sys
import time

# set django environment
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.template import Template, Context
from django.template.loader import *


def print_usage():
    """
    display the help message to the user
    """
    if len(sys.argv) >= 3 and sys.argv[1].lower() == 'help' and commands.has_key(sys.argv[2]):
        # print doc string for method
        args = {
            'doc': commands[sys.argv[2]].__doc__,
            'program': sys.argv[0],
            'key': sys.argv[2],
        }
        print("""
Usage for %(key)s:

%(program)s %(key)s

%(doc)s
""" % args)
    else:
        sorted_keys = commands.keys()
        sorted_keys.sort()
        args = {
            'program': sys.argv[0],
            'commands': "\n".join(sorted_keys),
        }

        print("""Usage:

%(program)s <command>

Where <command> is:
%(commands)s

For extra help, type:
%(program)s help <command>
""" % args)

def is_hidden(path):
    """
    Check if a file or folder is hidden.
    """
    title = file_title(path)
    return title[-1] == '~' or title[0] == '.'

def file_title(path):
    """
    Get only the title of a path.
    """
    names = path.split(os.sep)
    if len(names) == 0:
        return path
    else:
        return names[-1]

def walk(compile_func):
    """
    for each source file, call compile_func with these arguments:
        source file absolute path
        dest file absolute path
    """
    force = examine_watchlist()
    for root, dirs, files in os.walk(settings.PREPARSE_DIR, followlinks=True):
        relative = root.replace(settings.PREPARSE_DIR, "")
        if len(relative) > 0 and relative[0] == os.sep:
            relative = relative[1:]

        for file in files:
            in_file = os.path.join(root, file)
            if not is_hidden(in_file):
                out_file = os.path.join(settings.PREPARSE_OUTPUT, relative, file)
                compile_func(in_file, out_file, force)

def compare_file_date(in_file, out_file):
    """
    standard file compare: if in_file is newer, return true
    """
    in_file_modified = os.path.getmtime(in_file)
    out_file_modified = -1
    if os.path.exists(out_file):
        out_file_modified = os.path.getmtime(out_file)
    return in_file_modified > out_file_modified

watchlist = {}
def examine_watchlist():
    """
    if any template files have changed since this function was last called,
    return True and update the list
    """
    new_item = False
    for template_dir in settings.TEMPLATE_DIRS:
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                full_path = os.path.join(root, file)
                file_modified = os.path.getmtime(full_path)
                if watchlist.has_key(full_path):
                    if file_modified > watchlist[full_path]:
                        new_item = True
                else:
                    new_item = True
                watchlist[full_path] = file_modified

    return new_item

def compile_file(source, dest, force):
    """
    parse source and write to dest, only if source is newer
    force will make it definitely compile
    """
    if force or compare_file_date(source, dest):
        print("Parsing %s." % file_title(source))
        file = open(dest, 'w')
        in_text = open(source, 'r').read().decode()
        template = Template(in_text)

        # manually add settings from settings.py :(
        hash = settings.PREPARSE_CONTEXT
        hash.update({
            'MEDIA_URL': settings.MEDIA_URL,
        })
        
        context = Context(hash)
        file.write(template.render(context))
        file.close()

def clean_file(source, dest, force):
    if os.path.exists(dest):
        os.remove(dest)
        print("removing %s" % dest)

def compile():
    """
    compile every file, mirroring directory structure
    """
    walk(compile_file)

def clean():
    """
    delete auto-generated files
    """
    walk(clean_file)

def monitor():
    """
    Watches for new or changed files that are candidates for being preparsed,
    and automatically re-parses them.
    """
    while True:
        compile()
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            sys.exit(0)


commands = {
    'help': print_usage,
    'parse': compile,
    'clean': clean,
    'monitor': monitor,
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or not commands.has_key(sys.argv[1]):
        print_usage();
        sys.exit(1)
    else:
        commands[sys.argv[1]]()


