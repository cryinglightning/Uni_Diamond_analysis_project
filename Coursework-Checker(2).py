"""A script to test PHYS2320 Computing 2 Submissions.

This does NOT check whether your code correctly finds peaks - it checks
whether your code can be called by the program used to mark it and whether
yoy are returning results in the correct format.

Save this script into the same folder as your Python code and run it to check your code's operation

Version 1.1: Put back a missing import of getsourcelines
"""

import os.path as path
from inspect import isfunction,getargs,getmembers,getsourcelines
import traceback
import importlib
import re
import sys
from numpy import ndarray,all

def get_user_id():
    try:
        user_id=str(raw_input("Enter your issid (e.g. py11spqr :"))
        user_id=user_id.strip()
        assert path.exists(user_id+".py"),"Unable to find Python code module {}.py".format("user-id")
    except Exception as err:
        print """Failed to find your code. I looked for a file called {} in the current directory, but
        it doesn't exist ! Please move your code to the same directory and checking script and make sure
        that it is called <issid>.py where <issid> is your University of Leeds logon id.""".format(user_id+".py")
        user_id=None
    return user_id

def get_data_file():
    try:
        filename=str(raw_input("Enter the name of the data file :"))
        assert path.exists(filename),"Unable to locate your data file :".format(filename)
        with open(filename,"r") as data:
            for line in data:
                if "&END" in line:
                    break
                elif "mode" in line and line.split("=")[1].strip()!="assessment":
                    print "Your data file appears to be a practice data set. Make sure you submit the assessment data."
            else:
                print "Failed to find the start of data marker - are you sure this is a file downloaded from the coursework website?"
    except AssertionError as err:
        print """Failed to find your data file. I looked for a file called {} in the same directory as the checking
        script but it doesn't seem to be there. Please either move the file to this directory or enter the correct file name.""".format(filename)
        filename=None
    except IOError as err:
        print "Something went wrong with reading your data file {}".filename
        print err
        filename=None
    return filename

def scan_for_raw_input(filename):
    ok=re.compile(r"[^#]*#.*raw_input.*")
    with open(filename,"r") as code:
        for line in code:
            if "raw_input" in line and not ok.match(line):
                print """Found a raw_input statement that is not in a comment. This is potentially a problem as it might mean your
                code is asking me to type something in when I import it. Because the marking program can't type things in at a keyboard,
                it will refuse to try and mark code that has raw_input in it. Please either delete the line with the raw_input or comment
                it out by putting a # mark at the start of the line."""
                return False
    return True



def do_import(user_id):
    try:
        print """Ok, now I'm going to try and import your module. This should not result in any output....."""
        module=importlib.import_module(user_id)
        print """Finished importing your module. If you saw any lines of output then it means that your code is running something when
        I'm trying to import it. This is probably not the right thing. !"""
        assert "ProcessData" in dir(module),"Your module should contain a ProcessData function"
        assert isfunction(module.ProcessData),"ProcessData should be a function"
        args,vargs,vkwargs=getargs(module.ProcessData.__code__)
        assert len(args)==1 and args[0]=="filename" and vargs is None and vkwargs is None,"ProcessData should take just one argument called 'filename'"
    except ImportError as err:
        print "Failed to inmport your module correctly\nmessage was:\n{}".format(err.message)
        module=None
    except AssertionError as err:
        print "Something is wrong with your module\nMessage was\n{}".format(err.message)
        #module=None
    else:
        return module

def get_module_funcs(module):
    print "Now trying to list all the functions defined in your module."
    ix=0
    for name, member in getmembers(module):
        if not isfunction(member):
            continue
        elif name=="ProcessData":
            print "Got Process Data"
        else:
            print getsourcelines(member)[0][0]
            ix+=1
    if ix==0:
        print """Couldn't find any functions other than ProcessData in the module code.
 If you have think you should have more functions than this, then perhaps
 you have nested your function definitions inside the ProcessData ? Whilst
 this isn't an error, it is not very good style of efficient and you might
 want to move them into the main module code."""
    return True

def inspect_results(results):
    try:
        assert isinstance(results,dict),"Your code should return a dictionary not a {}. Please look at the template code on the VLE.".format(type(results))
        expected_results={"10keV_B":None, #this would be the magnetic field for 10keV data (T)
             "10keV_B_error":None, # the error in the magnetic field (T)
             "beta": None, #Detector angle in radians
             "beta_error": None, #uncertainity in detector angle (rad)
             "10keV_tau_damp": None, #Dampoing time for 10keV (s)
             "10keV_tau_damp_error": None, #and error (s)
             "B(Energy)_coeffs":(None,None,None), #tuple of a,b,c for quadratic,linear and constant terms
                                                  #for fitting B dependence on energy
                                                  #(T/keV^2,T/keV,T)
             "B(Energy)_coeffs_errors":(None,None,None), # Errors in above in same order.
             }
        
        for k in expected_results:
            print "Checking if your code returns a value for {}".format(k)
            if k not in results:
                print "....No - your code should return a dictionary of results with a key {}. If your code doesn't find a number for this then it should return None.".format(k)
            elif k.startswith("B(Energy)_coeffs"):
                if not (isinstance(results[k],(tuple,list,ndarray)) and len(results[k])==3 and all([isinstance(v,float) for v in results[k]])):
                    print "....No, the qudratic coefficients (and errors) for the multiple energies task should be a tuple of 3 floating point numbers."
                else:
                    print ".... Seems to return three floating point numbers ok. I haven't checked if it is correct though !"

            elif results[k] is not None and not isinstance(results[k],float):
                print "....No, your code returned a value for {}, but it was a {} not a floating point number".format(k,type(k))
            elif results[k] is None:
                print "....Your code doesn't find an answer for {}, but does correctly return None. IF this is what you expected, this is ok.".format(k)
            else:
                print ".... Seems to return a floating point number ok. I haven't checked if it is correct though !"
    except AssertionError as err:
        print "There was a problem with the results your code returned. Ther error message was\n{}".format(err.message)
        return False
    else:
        return True

if __name__=="__main__":
    user_id=get_user_id()
    if user_id is None:
        sys.exit()
    if not scan_for_raw_input(user_id+".py"):
        sys.exit()
    module=do_import(user_id)
    if module is None:
        sys.exit()
    if not get_module_funcs(module):
        sys.exit()
    filename=get_data_file()
    if filename is None:
        sys.exit()
    try:
        results=module.ProcessData(filename)
    except Warning as err:
        print "Your code generated some warnings, but continued anyway - the error message was:\n{}".format(err)        
    except Exception as err:
        print "Oh dear, there was a {} problem runnign your code. There error message was\n{}".format(type(err),err)
        traceback.print_exc()
    if results is not None and inspect_results(results):
        print "Congratulations, your code passed all the tests. We should be able to mark it."

