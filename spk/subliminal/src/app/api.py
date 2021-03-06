from pyextdirect.configuration import create_configuration, expose, LOAD, STORE_READ, STORE_CUD, SUBMIT
from pyextdirect.router import Router
import subliminal
import os
import datetime
import subprocess
from configobj import ConfigObj
from validate import Validator
from db import *


__all__ = ['Base', 'Directories', 'Subliminal']


Base = create_configuration()


class Directories(Base):
    def __init__(self):
        self.session = Session()

    @expose(kind=STORE_CUD)
    def create(self, data):
        results = []
        for record in data:
            directory = Directory(name=record['name'], path=record['path'])
            self.session.add(directory)
            self.session.commit()
            results.append({'id': directory.id, 'name': directory.name, 'path': directory.path})
        return results

    @expose(kind=STORE_READ)
    def read(self):
        results = []
        for directory in self.session.query(Directory).all():
            results.append({'id': directory.id, 'name': directory.name, 'path': directory.path})
        return results

    @expose(kind=STORE_CUD)
    def update(self, data):
        results = []
        for record in data:
            directory = self.session.query(Directory).get(record['id'])
            directory.name = record['name']
            directory.path = record['path']
            results.append({'id': directory.id, 'name': directory.name, 'path': directory.path})
        self.session.commit()
        return results

    @expose(kind=STORE_CUD)
    def destroy(self, data):
        results = []
        for directory_id in data:
            directory = self.session.query(Directory).get(directory_id)
            self.session.delete(directory)
            results.append(directory.id)
        self.session.commit()
        return results

    @expose
    def scan(self, directory_id):
        path = self.session.query(Directory).get(directory_id).path
        if not os.path.exists(path):
            return 0
        s = Subliminal()
        with subliminal.Pool(2) as p:
            subtitles = p.download_subtitles(path, languages=s.config['General']['languages'], services=s.config['General']['services'], force=False, multi=s.config['General']['multi'],
                                             cache_dir='/usr/local/subliminal/cache', max_depth=s.config['General']['max_depth'])
        return len(subtitles)


class Subliminal(Base):
    config_path = '/usr/local/subliminal/var/config.ini'

    def __init__(self):
        self.session = Session()
        self.config = ConfigObj(self.config_path, configspec='/usr/local/subliminal/app/config.spec', encoding='utf-8')
        self.config_validator = Validator()
        self.config.validate(self.config_validator)

    def setup(self):
        self.config.validate(self.config_validator, copy=True)
        self.config.write()

    @expose(kind=LOAD)
    def load(self):
        result = {'languages': self.config['General']['languages'], 'services': self.config['General']['services'],
                  'multi': self.config['General']['multi'], 'max_depth': self.config['General']['max_depth'],
                  'task': self.config['Task']['enable'], 'age': self.config['Task']['age'],
                  'hour': self.config['Task']['hour'], 'minute': self.config['Task']['minute']}
        return result

    @expose(kind=SUBMIT)
    def save(self, languages=None, services=None, multi=None, max_depth=None, task=None, age=None, hour=None, minute=None):
        self.config['General']['languages'] = languages
        self.config['General']['services'] = services
        self.config['General']['multi'] = multi
        self.config['General']['max_depth'] = max_depth
        self.config['Task']['enable'] = task
        self.config['Task']['age'] = age
        self.config['Task']['hour'] = hour
        self.config['Task']['minute'] = minute
        if not self.config.validate(self.config_validator):
            return
        self.config.write()

    def scan(self):
        paths = [directory.path for directory in self.session.query(Directory).all() if os.path.exists(directory.path)]
        if not paths:
            return
        scan_filter = lambda x: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(x)) > datetime.timedelta(days=self.config['Task']['age'])
        with subliminal.Pool(2) as p:
            subtitles = p.download_subtitles(paths, languages=self.config['General']['languages'], services=s.config['General']['services'], force=False, multi=self.config['General']['multi'],
                                             cache_dir='/usr/local/subliminal/cache', max_depth=self.config['General']['max_depth'], scan_filter=scan_filter)
        return len(subtitles)
