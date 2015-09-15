#frist python program
#!/usr/bin/env python
import os
import webbrowser
import subprocess
import re
import string
import datetime
from itertools import izip

def openURL (url_path):
    url = url_path
    # Open URL in a new tab, if a browser window is already open.
    try:
        webbrowser.open_new_tab(url)
    except:
        print("do it    ")
    return 0


def gitcommand ():
    os.chdir("./repository")
    cmd1 = "git tag | grep 'hotfix'"
    list_hf = subprocess.check_output(cmd1, shell=True)
    f = open('./hotfix', 'w')
    f.write(list_hf)
    f.close()
    cmd2 = "git show --tags | grep 'INC'"
    list_in = subprocess.check_output(cmd2, shell=True)
    f = open('./incident', 'w')
    f.write(list_in)
    f.close()
    return list_hf


def html_maker():
    #print "_ html maker is working"
    filenames = ['head', 'json', 'tail']
    htmlfile = 'HotFixes_Charges_' + get_datetime() + '.html'
    print htmlfile
    #with open('test.html', 'w') as outfile:
    with open(htmlfile, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())


def head_json():
    #print "Creating json"
    vtree_head ='<script>var treeData = [ { "name": "Hotfixes","parent": "null", "children": ['
    vtree_tail = "] } ];"
    vname = '{"name":'
    vparent_top_level = '"parent": "Top Level"'
    vchildren = '"children": ['
    vparent = '"parent":'
    vparent_close = '}]}'
    #others vars
    v_comma = ","
    v_dquotes = '"'
    v_list_inc = ''
    fjson = open('./json', 'w')
    fjson.write(vtree_head)
    v_parent = "Top Level"
    #fjson.write(vname)
    fjson.close()

def add_json(hf,incid,charges):
    #print "%s" % hf
    #print "%s" % incid
    #print "%s" % charges
    fjson = open('./json', 'a')
    v_name = '{"name": " ' + hf + ' " , '
    fjson.write(v_name)
    v_name = """ "parent": "Top Level" , "children": [ """
    fjson.write(v_name)
    v_name = """ {"name": " """ + incid + """ " , "parent": " """ + hf + """ " , "children": [ """
    fjson.write(v_name)
    # charges 1 or n
    #v_name = """ {"name": " """ + charges + """ ", "parent": " """ + incid + """ "}, ]} ] }, """
    v_name = grep_charges(incid)
    fjson.write(v_name)
    v_name = """ ]} ] }, """
    fjson.write(v_name)
    fjson.close()

def closed_json():
    fjson = open('./json', 'a')
    fjson.write('] } ];')
    fjson.close()

def create_nodes():
    file_hotfix = open("./hotfix")
    file_inicident = open("./incident")
    #create dictionary with charges file content
    d = {}
    with open("./charges") as f:
        for line in f:
            (key, val) = line.split()
            d[str(key)] = val



    #loop hotfix and incidente file. Get incident value from dictionary
    for file_hotfix, file_inicident in izip(file_hotfix, file_inicident):
        #print "%s\t%s" % (file_hotfix.rstrip(), file_inicident.rstrip())
        #print "Value : %s" %  d.get(file_inicident.rstrip())
        add_json(file_hotfix.rstrip(),file_inicident.rstrip(),d.get(file_inicident.rstrip()))

    return 0

def grep_charges(incid):
    #os.chdir("./repository")
    charges_list = ''
    charge_node = ''
    for line in open('./charges'):
        if incid in line:
            charges_list = line
            #print "En el if"
            charges_list = charges_list.replace(incid,'')
            charges_list = charges_list.strip()
            #print charges_list
            charge_node += """ {"name": " """ + charges_list      + """ ", "parent": " """ + incid + """ "}, """
    return charge_node

def clean():
    #print "Deleting temp files"
    #Delete incident, hotfix and json file
    os.remove('./hotfix')
    os.remove('./incident')
    os.remove('./json')


def get_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")



#call first function
gitcommand()
head_json()
create_nodes()
closed_json()
html_maker()
grep_charges('INC_001')
#openURL("./test.html")
get_datetime()
clean()
