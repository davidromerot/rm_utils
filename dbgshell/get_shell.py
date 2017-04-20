# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 13:23:23 2017

@author: dromero
"""

def get_shell():
    """
    Returns a callable object that opens an interactive IPython shell.
    This code is taken directly from the IPython documentation.
    http://ipython.org/ipython-doc/dev/interactive/reference.html#embedding-ipython
    To use it, create the embedded shell object
        my_new_shell = get_shell.get_shell()
    and then call it, whenever you want to have an interactive shell
        my_new_shell()
    Note that, within this shell, you can modify variables, but the changes will
    not be propagated to the calling environment.
    """
    try:
        get_ipython
    except NameError:
        banner=exit_msg=''
    else:
        banner = '*** Nested interpreter ***'
        exit_msg = '*** Back in main IPython ***'

    # First import the embed function
    from IPython.frontend.terminal.embed import InteractiveShellEmbed
    # Now create the IPython shell instance. Put ipshell() anywhere in your code
    # where you want it to open.
    return InteractiveShellEmbed(banner1=banner,exit_msg=exit_msg)

