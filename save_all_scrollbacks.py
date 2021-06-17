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
        for tab in window.tabs:
            for session in tab.sessions:
                print(session.pretty_str())
                pretty_session_safe=urllib.parse.quote(session.pretty_str(),safe='=[](){} ,+;:|?<>!@#$^&* ').replace(" ","_")
                session_file_path=f"{path}/{pretty_session_safe}.txt"
                print(session_file_path)
                async with iterm2.Transaction(connection) as txn:
                  li = await session.async_get_line_info()
                  lines = await session.async_get_contents(li.overflow, 100000000)
                with open(session_file_path, "w") as f:
                    f.writelines("{}\n".format(line.string) for line in lines)
                os.chmod(session_file_path, 0o200);
                gzip_path=session_file_path+".gzip"
                with gzip.open(gzip_path,"wt") as gf:
                    gf.writelines("{}\n".format(line.string) for line in lines)
                os.chmod(gzip_path, 0o200);

iterm2.run_until_complete(main)
