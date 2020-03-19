# api/git.py

import os
import config
import subprocess as sp
from git import Repo
from App.models import *

class Repository():
    def __init__(self, path=config.REPOSITORY_FOLDER):
        self.path = path

    def fill_database(self):
        self.repos = os.listdir(self.path)
        self.paths = [ os.path.join(self.path, repo) for repo in self.repos ]
        self.repositories = [ Repo(repo) for repo in self.paths ]
        for i in self.repositories:
            branches = []

    def get_repos(self):
        repos = Repositories.query.all()
        database = []
        for i,repo in enumerate(repos):
            database.append({})
            database[i]["repo"] = repo
            database[i]["branches"] = []
            iid = 0
            for j, branch in enumerate(eval(repo.branches)):
                database[i]["branches"].append({})
                database[i]["branches"][j]["id"] = iid
                iid += 1
                database[i]["branches"][j]["name"] = branch
                database[i]["branches"][j]["commits"] = Commits.query.filter(Commits.repository==repo.id).all()
        return database

    def create_repo(self,title, desc, targz):
        os.mkdir(title+".git")

    def check_folder(self):
        pass

    def git(self,*command):
        pass
