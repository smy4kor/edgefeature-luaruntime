#!/usr/bin/python3

import os
import urllib.request


class DownloadManager:

    def download(self, artifact):
        path = os.getcwd() + "/downloads"
        print ("Desired download directory is %s" % path)
        if  not os.path.isdir(path):
            print("Download directory must be created")
            try:
                os.mkdir(path)
                print ("Successfully created the directory %s " % path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
    
        urllib.request.urlretrieve(artifact.url, path + "/" + artifact.name)
        print('downloaded ' + artifact.name)
