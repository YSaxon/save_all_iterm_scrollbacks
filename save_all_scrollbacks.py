#!/usr/bin/env python3.7

import iterm2
# This script was created with the "basic" environment which does not support adding dependencies
# with pip.

async def main(connection):
    # Your code goes here. Here's a bit of example code that adds a tab to the current window:
    
    print("line11")
    #print(app.terminal_windows)
    @iterm2.RPC
    async def save_all_sessions():
        app = await iterm2.async_get_app(connection)
        print("beforeapp")
        print(app)
        print("afterapp")
        print(app.terminal_windows)
        print("lin13")
        print(app.terminal_windows)
        for window in app.terminal_windows:
            print("lin15")
            for tab in window.tabs:
                for session in tab.sessions:
                    async with iterm2.Transaction(connection) as txn:
                      li = await session.async_get_line_info()
                      print("got line info\n")
                      lines = await session.async_get_contents(li.overflow, 10)
                    print(list(map(lambda line: line.string, lines)))
                      # lines = await session.async_get_contents(li.overflow, 10)
  #                   print(list(map(lambda line: line.string, lines)))
    
    # async def clear_all_sessions():
    #     code = b'\x1b' + b']1337;ClearScrollback' + b'\x07'
    #     for window in app.terminal_windows:
    #         for tab in window.tabs:
    #             for session in tab.sessions:
    #                 await session.async_inject(code)
    print("lin32")
    await save_all_sessions.async_register(connection)
    print("lin34")

iterm2.run_until_complete(main)
