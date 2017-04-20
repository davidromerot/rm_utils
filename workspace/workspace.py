# -*- coding: utf-8 -*-
"""
Saves all user-created variables in the current environment into a file.
This function aims to provide functionality similar to Matlab's "save"
function.

Version 1 created on Tue Apr 04 14:53:19 2017

@author: dromero
"""

def load_workspace(filename, overwrite = True, debug = False):
    """
    Load all user-defined variables from a file into the caller's namespace
    """
    
    import sys
    import pickle

    # TODO: Implement functionality to read the last (most recent) file.
    
    # Load file
    try:
        d = pickle.load(open(filename,'rb'))
    except Exception as e:
        print("\nsave_workspace: \tError reading the file {}.\n"\
              .format(filename))
        raise
        return
    
    # Get access to the caller's namespace (just one level up in the stack)
    calling_namespace = sys._getframe(1).f_locals
    
    # Process dictionary to create the variables in the caller's workspace
    for name,value in d.iteritems():
        # TODO: Implement functionality to avoid overwriting existing variables
        calling_namespace[name] = value
    
    return



def save_workspace(filename = None, type_list = '', debug = False):
    """
    Save all user-defined variables in the current namespace into a file
    """
    
    import os
    import sys
    import types
    import collections
    import datetime as dt
    import pickle
    
    # Create filename based on time and date if it was not provided
    if not filename:
        name_part = dt.datetime.now().__str__()
        name_part = name_part[:-4]
        name_part = name_part.replace('-','_')
        name_part = name_part.replace(':','_')
        name_part = name_part.replace('.','_')
        filename = 'workspace_' + name_part + '.pkl'

    # Get access to the caller's namespace (just one level up in the stack)
    # I saw this functionality here:
    # http://stackoverflow.com/questions/3114015/call-python-function-as-if-it-were-inline
    calling_namespace = sys._getframe(1).f_locals
    
    # get list of variables in user namespace (this is a list of strings)
    user_ns = get_ipython().user_ns
    hidden_ns = get_ipython().user_ns_hidden
    
    # this part is an idea from a StackOverflow answer
    nonmatching = object()
    # list of variables that are not built-in or hidden
    out = [ i for i in user_ns
                if not i.startswith('_') \
                and (user_ns[i] is not hidden_ns.get(i, nonmatching)) ]
    out.sort()
    
    # total number of names in the calling's namespace
    ntotal = len(out)
    
    # debug help    
    if debug:
        print("\nList of available variables in the namespace:\n")
        print(out)
    
    # filter to include only variables of types requested by the user
    typelist = type_list.split()
    if typelist:
        typeset = set(typelist)
        out = [i for i in out if type(user_ns[i]).__name__ in typeset]

    # remove specific object types
    exclusion_list = [types.ModuleType, types.FrameType, \
         collections.Callable, types.FileType, types.TypeType, \
         types.GeneratorType]
    #
    out = [ i for i in out \
            if not any([isinstance(calling_namespace[i],objtypes) \
            for objtypes in exclusion_list]) ]
    
    # debug help    
    if debug:
        print("\nList of variables to try to save:\n")
        print(out)
    
    # Exclude other unpickable objects.
    # This follows the duck-test philosophy: Try, and handle errors if any
    
    # iterate over the variables, remove those that raise errors PickleError
    removed_vars = list()
    for var_name in out:
        try:
            # Check is done with pickle.dump because pickle.dumps works even for
            # non-pickleable types
            #dummy = pickle.dumps(calling_namespace[var_name])
            blackhole = open(os.devnull,'wb')
            dummy = pickle.dump(calling_namespace[var_name],blackhole)
                
        except Exception as e:
            # no error handling here, 'var_name' is guaranteed to be in 'out'
            out.remove(var_name)
            removed_vars.append(var_name)
            
            # debug help    
            if debug:
                print("\n The variable {} gave a {} during pickling: {}\n"\
                      .format(var_name,e.__class__,e.message))
            pass
        
    # Notify the user if any names in the namespace will not be pickled
    if removed_vars:
        print("\nsave_workspace - Warning: \tThe following objects will not be saved:\n")
        print(removed_vars)
    
    # sort the list of variables to be saved
    out.sort()
    
    # debug help
    if debug:
        print("\nList of picklable objects that will be saved:\n")
        print(out)

    # final number of variables to save
    nsaved = len(out)

    # loop over list to build the output dictionary
    outdict = dict()
    if debug:
        print("\nBuilding output dictionary:\n")
    
    for name in out:
           outdict[name] = calling_namespace[name]
           if debug:
              print("Name: {} \t --> \t Content: {}"\
                    .format(name,calling_namespace[name].__class__))
              
    # save the dictionary into a pickle (in a pickle?)
    try:
        fp = open(filename,'wb')
        pickle.dump(outdict, fp)
        fp.flush()
        fp.close()
    except Exception as e:
        print("\nsave_workspace - Error: \tThere was an error saving to the file.\n")
        raise

    # If we are here, no exceptions were raised, saving was successful
    print("\nsave_workspace: \tWorkspace saved successfully as {}."\
          .format(filename))
    print("save_workspace: \t{} out of {} variables saved.\n\n"\
          .format(nsaved,ntotal))    
    return
