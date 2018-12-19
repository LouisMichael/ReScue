# -*- coding: utf-8 -*-
import os
import sys
import re

from os import makedirs
from os.path import exists, join

from scripts.utils.webutils import *
from scripts.utils.extractutils import *

def analyzeGitUrl(url, storeDir):
    res = re.search('.*github.com/(.*)/(.*)\.git', url)
    print(res.groups())
    developer = res.group(1)
    project = res.group(2)
    print(developer, project)

    repo_page = 'https://github.com/' + developer + '/' + project
    resp = requestPage(repo_page)

    res = re.findall('<span class="lang">(.*?)</span>\s*<span class="percent">(.*%)</span>', resp)

    lang = None
    if len(res) > 0:
        lang = res[0][0]

    if lang is not None:
        placeDir = join(storeDir, lang)
        if not exists(placeDir):
            makedirs(placeDir)
        return (lang, project, placeDir)
    else:
        print('Error: cannot extract language from its project page')
        return (None, project, None)

def getGitProject(url, dir):
    cwd = os.getcwd()
    os.chdir(dir)
    os.system('git clone ' + url)
    os.chdir(cwd)

def isProjectExist(url):
    db = connectDB()
    cs = db.cursor()
    sql = 'SELECT DISTINCT repo FROM regs'
    cs.execute(sql)

    res = cs.fetchall()
    for r in res:
        if url == r[0]:
            return True

    return False