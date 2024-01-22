import os, json, requests, re, time
from pathlib import Path
from . import MMT_JSON_KEYS, LOCAL_TARGET_KEYS, isInt, isFloat
from .instruments.binospec import validate as bino_validate
from .instruments.MMTCam import validate as mmtcam_validate
from .instruments.mmirs import validate as mmirs_validate
from datetime import datetime


class api():

    def __init__(self, target=None, token=None):

        self.base = 'https://scheduler.mmto.arizona.edu/APIv2'
        self.target = target

        if token is None:
            self.token = os.getenv('MMT_API_TOKEN')
        else:
            self.token = token

        self.request = None


    def _build_url(self, params={}):
        assert self.target is not None, 'Target cannot be None'
        self.url = '{}/{}'.format(self.base, self.target)
        for p in params:
            if p in ['targetid', 'datafileid']:
                self.url = '{}/{}'.format(self.url, params[p])
            else:
                self.url = '{}/{}/{}'.format(self.url, p, params[p])


    def _post(self, r_json):
        self._build_url(r_json['urlparams'])
        data = r_json['data'] if 'data' in r_json.keys() else None
        files = r_json['files'] if 'files' in r_json.keys() else None
        d_json = r_json['d_json'] if 'd_json' in r_json.keys() else None
        self.request = requests.post(self.url, json=d_json, data=data, files=files)
        return self.request


    def _get(self, r_json):
        self._build_url(r_json['urlparams'])
        d_json = r_json['d_json'] if 'd_json' in r_json.keys() else None
        self.request = requests.get(self.url, json=d_json)
        return self.request


    def _put(self, r_json):
        self._build_url(r_json['urlparams'])
        d_json = r_json['d_json']
        self.request = requests.put(self.url, json=d_json)
        return self.request


    def _delete(self, r_json):
        self._build_url(r_json['urlparams'])
        d_json = r_json['d_json']
        self.request = requests.delete(self.url, json=d_json)
        return self.request


class Target(api):
    def __init__(self, token=None, verbose=True, payload={}):
        self.verbose = verbose
        self.valid = False
        self.downloaded = False
        self.partial_download = False
        self.message = {
            'Errors':[],
            'Warnings':[]
        }

        assert token is not None, 'Token cannot be None'
        super().__init__('catalogTarget', token)

        allowed_keys = list(MMT_JSON_KEYS)
        self.__dict__.update((str(key).lower(), value) for key, value in payload.items() if str(key).lower() in allowed_keys)

        if 'targetid' in payload.keys():
            self.targetid = payload['targetid']
            self.id = payload['targetid']
            self.get()
            #self.database_load()

        self.validate(verbose=self.verbose)


    def validate(self, verbose=True):
        selfkeys = self.__dict__.keys()
        selfdict = self.__dict__
        errors, warnings = [], []

        if 'ra' in selfkeys:
            ra = selfdict['ra']
            r = re.compile('.{2}:.{2}:.{2}\.*')
            if not r.match(ra):
                errors.append('Invalid format for field \'ra\' ['+ra+']. Valid format is dd:dd:dd.d')
        else:
            errors.append('Field \'ra\' is required. Valid format is dd:dd:dd.d')

        if 'dec' in selfkeys:
            dec = selfdict['dec']
            r = re.compile('.{2}:.{2}:.{2}\.*')
            isNeg = dec.startswith('-')
            if '-' in dec:
                dec = dec.split('-')[1]
            if '+' in dec:
                dec = dec.split('+')[1]
            if not r.match(dec):
                errors.append('Invalid format for field \'dec\' ['+dec+']. Valid format is [+/-]dd:dd:dd.d')
            dec = '-' + dec if isNeg else '+' + dec
            self.__dict__.update({'dec':dec})

        else:
            errors.append('Field \'dec\' is required. Valid format is [+/-]dd:dd:d.d')

        if 'epoch' not in selfkeys:
            warnings.append('Field \'epoch\' default set to 2000.0')
            self.__dict__.update({'epoch':'J2000'})

        if 'exposuretime' in selfkeys:
            exposuretime = selfdict['exposuretime']
            if not isInt(exposuretime):
                errors.append('Field \'exposuretime\' valid format is integer (seconds)')
            elif not int(exposuretime) > 0:
                errors.append('Field \'exposuretime\' must be greater than zero you dingus')
        else:
            errors.append('Field \'exposuretime\' is required. Valid format is integer (seconds)')

        if 'magnitude' in selfkeys:
            magnitude = selfdict['magnitude']
            if not isFloat(magnitude):
                errors.append('Invalid format for field \'magnitude\'. Must be decimal/float')
        else:
            errors.append('Field \'magnitude\' is required for requested Target')

        if 'maskid' in selfkeys:
            maskid = selfdict['maskid']
            if not isInt(maskid):
                errors.append('Field \'maskid\' must be integer')
        else:
            errors.append('Field \'maskid\' is required \n \
                There are common mask ids for imaging/longslit slitwidths: \n \
                ----For imaging: 110 \n \
                ----Longslit0_75: 113 \n \
                ----Longslit1: 111 \n \
                ----Longslit1_25: 131 \n \
                ----Longslit1_5: 114 \n \
                ----Longslit5: 112')

        if 'numberexposures' in selfkeys:
            numberexposures = selfdict['numberexposures']
            if not isInt(numberexposures):
                errors.append('Field \'numberexposures\' must be integer')
        else:
            warnings.append('Field \'numberexposures\' is required. Setting value to 1')
            self.__dict__.update({'numberexposures':1})

        if 'objectid' in selfkeys:
            objectid = selfdict['objectid']
            if len(objectid) < 2 or len(objectid) > 50:
                errors.append('Field \'objectid\' must have a string length greater than 2 and less than 50.')
            if any(c for c in objectid if not c.isalnum() and not c.isspace()):
                errors.append('Field \'objectid\' must be alphanumeric and not contain any spaces')
        else:
            errors.append('Field \'objectid\' is required. ')

        if 'pa' in selfkeys:
            pa = selfdict['pa']
            if not isFloat(pa):
                errors.append('Field \'pa\' must be float and between -360.0 and 360.0')
            elif not (float(pa) >= -360 and float(pa) <= 360):
                errors.append('Field \'pa\' must be between -360 and 360')
        else:
            warnings.append('Field \'pa\' is set to 0.0')
            self.__dict__.update({'pa':0.0})

        if 'pm_dec' in selfkeys:
            pm_dec = selfdict['pm_dec']
            if not isFloat(pm_dec):
                errors.append('Field \'pm_dec\' must be float')
        else:
            warnings.append('Field \'pm_dec\' is set to 0')
            self.__dict__.update({'pm_dec':0.0})

        if 'pm_ra' in selfkeys:
            pm_ra = selfdict['pm_ra']
            if not isFloat(pm_ra):
                errors.append('Field \'pm_ra\' must be float')
        else:
            warnings.append('Field \'pm_ra\' is set to 0')
            self.__dict__.update({'pm_ra':0.0})

        if 'priority' in selfkeys:
            priority = selfdict['priority']
            if not isInt(priority):
                errors.append('Field \'priority\' must be an integer. Valid options are 1,2,3 where 1 is highest priority')
            elif priority not in [1, 2, 3, '1', '2', '3']:
                errors.append('Field \'priority\' valid options are 1,2,3 where 1 is highest priority')
        else:
            warnings.append('Field \'priority\' set to lowest value: 3')
            self.__dict__.update({'priority':3})

        if 'visits' in selfkeys:
            visits = selfdict['visits']
            if not isInt(visits):
                errors.append('Field \'visits\' must be an integer')
        else:
            warnings.append('Field \'visits\' is set to 1')
            self.__dict__.update({'visits':1})

        #validating nonrequired fields and default values for Binospec

        if 'photometric' in selfkeys:
            photometric = selfdict['photometric']
            if not isInt(photometric):
                errors.append('Field \'photometric\' must be integer. \n \
                    0 = photometric conditions not required. \n \
                    1 = photometric conditions required.')
        else:
            self.__dict__.update({'photometric':0})

        if 'targetofopportunity' in selfkeys:
            too = selfdict['targetofopportunity']
            if not isInt(too):
                errors.append('Field \'targetofopportunity\' must be integer. \n \
                    0 = not a target of opportunity. \n \
                    1 = target of opportunity.')
        else:
            self.__dict__.update({'targetofopportunity':0})

        #validating required keys
        if 'instrumentid' in selfkeys:
            instrumentid = selfdict['instrumentid']

            #Binospec
            if instrumentid in [16,'16']:
                inst_errors, inst_warnings, inst_dict = bino_validate(selfdict)
                errors.extend(inst_errors)
                warnings.extend(inst_warnings)
                self.__dict__.update(inst_dict)
            #MMTCAM
            if instrumentid in [6,'6']:
                inst_errors, inst_warnings, inst_dict = mmtcam_validate(selfdict)
                errors.extend(inst_errors)
                warnings.extend(inst_warnings)
                self.__dict__.update(inst_dict)

            #MMIRS...
            if instrumentid in [15,'15']:
                inst_errors, inst_warnings, inst_dict = mmirs_validate(selfdict)
                errors.extend(inst_errors)
                warnings.extend(inst_warnings)
                self.__dict__.update(inst_dict)

        else:
            errors.append('Only supported instrument right now is Binospec and MMIRS: Please choose an instrument id')
            #self.__dict__.update({'instrumentid':'16'})

        #Settings for limiting to only Binospec
        #self.__dict__.update({'dithersize':None, 'gain':None, 'grism':None, 'moon':None, 'readtab':None})

        #Validate instrument on the telescope
        #current_instruments = self.get_instruments()
        #if any(int(ci['instrumentid']) == 16 for ci in current_instruments):
        #    if 'targetofopportunity' not in selfkeys:
        #        self.__dict__.update({'targetofopportunity':1})
        #    if 'priority' not in selfkeys:
        #        self.__dict__.update({'priority':1})
        #else:
        #    self.__dict__.update({'targetofopportunity':0})
        #    self.__dict__.update({'priority':3})
        #    warnings.append('Binospec is currently not on the MMT!\n \
        #        Setting Field: \'targetofopportunity\' to 0\n \
        #        Setting Field \'priority\' to 3\n \
        #        Envoke target.api.get_instruments(instrumentid=16) to see when the next start date is for Binospec')

        #Print out Errors and Warnings
        self.valid = (len(errors) == 0)
        self.message = {
            'Errors':errors,
            'Warnings':warnings
        }

        if self.verbose:
            if not self.valid:
                print('INPUT TARGET ERRORS: ')
                for e in errors:
                    print(e)
                print()
            if len(warnings) > 0:
                print('INPUT TARGET WARNINGS: ')
                for w in warnings:
                    print(w)


    def dump(self):
        for d in self.__dict__:
            print('{}: {}'.format(d, self.__dict__[d]))
        print()


    def update(self, **kwargs):

        self.__dict__.update((key, value) for key, value in kwargs.items() if key in MMT_JSON_KEYS)
        self.validate()

        if self.valid:
            kwargs['targetid'] = self.__dict__['id']
            kwargs['token'] = self.token

            data = {
                'urlparams':{
                    'targetid':self.__dict__['id']
                },
                'd_json':kwargs
            }

            self._put(r_json=data)
            r = self.request
            print(json.loads(r.text), r.status_code)

            if r.status_code == 200:
                self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
            else:
                print('Something went wrong with the request. Envoke target.request to see request information')
        else:
            print('Invalid Target. Envoke target.validate() to see errors')


    def delete(self):
        data = {
            'urlparams':{
                'targetid':self.__dict__['id']
            },
            'd_json':{
                'token':self.token
            }
        }
        r = self._delete(r_json=data)
        if r.status_code == 200:
            print("Succesfully Deleted")
        else:
            print('Something went wrong with the request. Envoke target.request to see request information')
        if self.verbose:
            print(json.loads(r.text), r.status_code)


    def post(self):
        if self.valid:
            payload = dict((key, value) for key, value in self.__dict__.items() if key in MMT_JSON_KEYS)
            payload['token'] = self.token
            data = {
                'urlparams':{},
                'data':None,
                'files':None,
                'd_json':payload,
            }
            r = self._post(r_json=data)

            if self.verbose:
                print(json.loads(r.text), r.status_code)
            if r.status_code == 200:
                    self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
                    self.targetid = self.id
            else:
                print('Something went wrong with the request. Envoke target.request to see request information')
        else:
            print('Invalid Target parameters. Envoke target.validate() to see errors')


    def get(self):
        data = {
            'urlparams': {
                'targetid':self.__dict__['targetid']
            },
            'd_json':{
                'token':self.token
            },
        }
        request = self._get(r_json=data)
        r = json.loads(request.text)
        if request.status_code == 200:
            self.__dict__.update((key, value) for key, value in r.items())
        else:
            print('Something went wrong with the request. Envoke target.request to see request information')


    def upload_finder(self, finder_path):
        if self.valid:
            if isinstance(finder_path, str):
                finder_file = open(finder_path, 'rb')
            else:  # if it's already a file object (e.g., from Django)
                finder_file = finder_path.open('rb')
            data = {
                'urlparams': {
                    'targetid':self.__dict__['targetid']
                },
                'data':{
                    'type':'finding_chart',
                    'token':self.token,
                    'target_id':str(self.__dict__['id']),
                },
                'files':{
                    'finding_chart_file': finder_file
                },
                'd_json':None
            }
            r = self._post(r_json=data)
            if r.status_code == 200:
                self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
            else:
                print('Something went wrong with the request. Envoke target.request to see request information')
            if self.verbose:
                print(json.loads(r.text), r.status_code)


    def download_exposures(self, force=False):
        # also check the headers for the individual exposure times adding up to the total requested from api.get(targetid) method
        # to decide if it is done
        if (self.valid and self.iscomplete != 1) or force:
            self.datalist = Datalist(token=self.token)
            self.datalist.get(targetid=self.__dict__['id'])

            parentdir = self.parentdir if 'parentdir' in self.__dict__.keys() else os.getcwd()
            print('Length of datalist {}'.format(len(self.datalist.data)))
            if len(self.datalist.data):
                for d in self.datalist.data:
                    name = d['name']
                    datafiles = d['datafiles']
                    for df in datafiles:
                        ftype = df['type']
                        filepath = '{}/data/{}/{}/{}'.format(parentdir, self.objectid, name, ftype)
                        Path(filepath).mkdir(parents=True, exist_ok=True)
                        datafileid = df['id']
                        filename = df['filename']
                        download_file = '{}/{}'.format(filepath, filename)

                        if not os.path.exists(download_file):
                            if self.verbose:
                                print('Downloading: {}'.format(download_file))
                            im = Image(token=self.token)
                            im.get(datafileid=datafileid, filepath=download_file)
                            self.partial_download = True

                        else:
                            if self.verbose:
                                print('File \'{}\' already exists'.format(download_file))
                                self.partial_download = True

                self.downloaded = True
                self.partial_download = False

            #else:
            #    if self.verbose:
            #        print('Exposures have been take, but are not ready for download')

            else:
                if self.verbose:
                    print('Exposures not taken yet.')
        else:
            if self.verbose:
                print('Exposure is completed')


class Instruments(api):
    def __init__(self, token=None, verbose=True, payload={}):
        self. verbose = verbose
        super().__init__('trimester//schedule/all/', token)

    def get_instruments(self, date=None, instrumentid=None, getAll=False):
        if date is None and instrumentid is None:
            date = datetime.now()

        r_json = {
            'urlparams':{},
            'd_json':{
                'token':self.token
            }
        }

        self._get(r_json=r_json)

        schedule = json.loads(self.request.text)
        published_queues = schedule['published']['queues']
        ret = []

        for pq in published_queues:
            start = datetime.strptime(pq['queueruns'][0]['startdate'], '%Y-%m-%d %H:%M:%S-%f')
            end = datetime.strptime(pq['queueruns'][0]['enddate'], '%Y-%m-%d %H:%M:%S-%f')
            instid = pq['instrumentid']
            queuename = pq['name']
            for qr in pq['queueruns']:
                start = datetime.strptime(qr['startdate'], '%Y-%m-%d %H:%M:%S-%f')
                end = datetime.strptime(qr['enddate'], '%Y-%m-%d %H:%M:%S-%f')
                if getAll:
                    ret.append({'instrumentid':instid, 'name':queuename, 'start': start, 'end': end})
                else:
                    if instrumentid is None and (date > start and date < end):
                        ret.append({'instrumentid':instid, 'name':queuename, 'start': start, 'end': end})
                    if date is None and (instrumentid == int(instid)):
                        ret.append({'instrumentid':instid, 'name':queuename, 'start': start, 'end': end})

        ret = sorted(ret, key=lambda i: i['start'])
        if self.verbose:
            for r in ret:
                print(r)
        return ret


class Datalist(api):
    def __init__(self, token=None, verbose=True, payload={}):
        self.verbose = verbose
        self.data = []
        super().__init__('data/list/catalogtarget', token)


    def get(self, targetid, data_type='raw'):
        assert data_type in ['raw', 'reduced'], 'data_type must either be raw or reduced'
        r_json = {
            'urlparams':{
                'targetid':targetid,
                'token':self.token,
                'type':data_type
            }
        }

        self._get(r_json=r_json)

        if self.request.status_code == 200:
            self.data = self.request.json()
        else:
            print('Datalist request error')


class Image(api):
    def __init__(self, token=None, verbose=True, payload={}):
        self. verbose = verbose
        super().__init__('data/download/datafile', token)


    def get(self, datafileid=None, filepath=os.getcwd()):

        assert datafileid is not None, 'datafileid cannot be None'
        r_json = {
            'urlparams':{
                'datafileid':datafileid,
                'token':self.token
            }
        }

        self._get(r_json=r_json)

        if self.request.status_code == 200:
            if self.verbose:
                print('Writing file.')
            open(filepath, 'wb').write(self.request.content)
            self.request = None
        else:
            print('Image download request error')


class Listener():
    def __init__(self, token=None, targetid=None):
        assert token is not None, 'token cannot be None'
        assert targetid is not None, 'targetid cannot be None'
        self.token = token
        self.targets = []
        self.targets.append(Target(token=self.token, payload={'targetid':targetid})) 
        #self.listener_log = payload['logpath'] if 'logpath' in payload.keys() else os.getcwd()

    def listen(self, Force=True):

        start_time = datetime.now()
        all_downloaded = all([x.downloaded for x in self.targets])

        run_listener = not all_downloaded or Force

        while run_listener:

            for t in self.targets:
                t.get()
                print(t.objectid)
                t.download_exposures(force=Force)

            run_listener = not all([x.downloaded for x in self.targets])

            if run_listener:
                print("Sleeping for 60s")
                time.sleep(60)
            else:
                print('Download finished :)')

        pass
