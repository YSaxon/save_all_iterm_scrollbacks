#!/usr/bin/env python3.7

import iterm2
import pprint
import os
import shlex
import urllib
import gzip


path=os.path.expanduser("~")+'/Documents/iterm_screen_buffers'
if not os.path.exists(path):
    os.makedirs(path)
# This script was created with the "basic" environment which does not support adding dependencies
# with pip.

async def main(connection):
    app = await iterm2.async_get_app(connection)
    print(app)
    for window in app.terminal_windows:
        print("window: "+window.pretty_str()+"\n")
        pretty_window_safe=urllib.parse.quote(window.pretty_str().partition('\n')[0],safe='=[](){} ,+;:|?<>!@#$^&* ').replace(" ","_")
        window_path=f"{path}/{pretty_window_safe}"
        if not os.path.exists(window_path):
            os.makedirs(window_path)
        for tab in window.tabs:
            for session in tab.sessions:
                print(session.pretty_str())
                pretty_session_safe=urllib.parse.quote(session.pretty_str(),safe='=[](){} ,+;:|?<>!@#$^&* ').replace(" ","_")
                session_file_path=f"{window_path}/{pretty_session_safe}.txt"
                gzip_path=f"{window_path}/{pretty_session_safe}.txt.gz"
                print(session_file_path)
                lines_offset=0
                lines_per_read=100000
                async with iterm2.Transaction(connection) as txn:
                    with open(session_file_path, "w") as f, gzip.open(gzip_path,"wt") as gf:
                        try_reading_more_lines=True
                        while try_reading_more_lines:
                            li = await session.async_get_line_info()
                            lines = await session.async_get_contents(li.overflow+lines_offset, lines_per_read)
                            f.writelines("{}\n".format(line.string) for line in lines)        
                            gf.writelines("{}\n".format(line.string) for line in lines)
                            lines_offset+=lines_per_read
                            try_reading_more_lines=lines
                os.chmod(session_file_path, 0o200);
                os.chmod(gzip_path, 0o200);

iterm2.run_until_complete(main)
