#!/usr/bin/env python
#
# Author: Chema Garcia (aka sch3m4)
# Homepage: http://safetybits.net
# Contact: chema@safetybits.net || @sch3m4
#

import os
import sys
import httplib

RESOLUTIONS=['240','360','720','1080']

def get_video_preffix(host,path):
    # obtenemos la url del video
    conn = httplib.HTTPConnection(host)
    conn.request("GET", path )
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    
    try:
        host = data.split('video_host')[1].split("'")[1]
        uid = data.split('video_uid')[1].split("'")[1]
        vtag = data.split('video_vtag')[1].split("'")[1]
        ret = host + 'u' + uid + '/video/' + vtag
    except:
        host = None
        ret = None
    
    return (ret,host)
    
def check_resolutions(host,url,res):
        conn = httplib.HTTPConnection(host.split("/")[2])
        conn.request("GET", url + '.' + res + '.mp4' )
        resp = conn.getresponse()
        conn.close()
        
        if resp.status == 404:
            return (False,0)
        return (True,resp.length)

def main(host,path,destination):
    
    videos = {}
    
    print "\n[+] Getting video URL..."
    preffix,host = get_video_preffix(host,path)
    if preffix is None:
        print "Error: No video found!\n"
        sys.exit(-2)
    
    print "\t+ URL: %s\n" % preffix
    
    print "[+] Checking resolutions..."
    
    for res in RESOLUTIONS:
        valido,bytes = check_resolutions(host,preffix,res)
        if valido is True:
            print "\t+ %s (%d MBytes): %s" % (res, bytes/1024/1024 , preffix + '.' + res + '.mp4')
            videos[res] = preffix + '.' + res + '.mp4'
            resol = res
    
    if len(videos) > 1:
        resol = 0
        while resol not in videos.keys():
            print "\n[+] Select resolution: ",
            resol = sys.stdin.readline().strip()
    
    resp = 'a'
    while resp != 'y' and resp != 'n' and resp != '':
        print "\n[+] Do you want to launch WGet and download the file? (y/n)[y]: ",
        resp = str(sys.stdin.readline().strip()).lower()
    
    print ""
    if resp == 'y' or resp == '':
        os.system("wget '%s' -O '%s'" % (videos[resol],destination))

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "\n[+] Usage: %s <VK.Url> <destination>\n"
        sys.exit(-1)
        
    # creates the directory if it does not exists
    if os.path.dirname(sys.argv[2]) != "" and not os.path.isdir(os.path.dirname(sys.argv[2])):
        os.mkdir(os.path.dirname(sys.argv[2]))

    try:
        if sys.argv[1][:7] == 'http://':
            sys.argv[1] = sys.argv[1][7:]
        elif sys.argv[1][:8] == 'https://':
            sys.argv[1] = sys.argv[1][8:]
        host = sys.argv[1].split("/")[0]
        path = "/" + sys.argv[1].split("/")[1]
    except:
        print "[e] Invalid URL!\n"
        sys.exit(-2)
    
    main(host,path,sys.argv[2])
