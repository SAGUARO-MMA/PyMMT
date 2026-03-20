[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8322354.svg)](https://doi.org/10.5281/zenodo.8322354)
# PyMMT

This repository is designed to facilitate rapid Target of Opportunity (ToO) observations to Binospec or MMIRS at the [MMT](https://www.mmto.org/) to enable same-night spectroscopy of interesting transients. Here we will provide examples to install and upload targets.

## Install
To get the repository (in a bash/unix terminal)
```bash
git-clone repository
python -m pip install -e .
#or
python -m pip install pymmt
```

## Using the API Wrapper

Here we describe the process to POST, GET, UPDATE, and DELETE a MMT Target. The `Target` class also contains an `api` class that calls each of the API methods. This class contains the request information for each request method so that it can debugged in the command line. 

```python
import pymmt

target = pymmt.Target(token=API_TOKEN, ...)
#once a request is made

target.**action() #post, delete, update... etc

#the request response can be viewed by
target.request

#which contains all of the expected request response information:
#   target.request.content
#   target.request.text
#   target.request.status_code
#   etc
```

### Creating a Target

To create a target there are a lot of required fields and conditional parameters based on the observation type. To begin with the metadata for the target itself:

* `objectid`: This is the name of the target. The requirements for this field is that it contains no special characters and spaces. It must also be greater than 2 characters and less than 50 characters.
* `ra`: Right Ascension of the target. Required format to be: `dd:dd:dd.d`
* `dec`: Declination of the target. Required format to be: `[+/-]dd:dd:dd.d`
* `magnitude`: Magnitude of the target. Must be a `float`
* `epoch`: The epoch of the target. Defaults to 2000.0

The target exposure information is based on the the field `observationtype`:

For Binospec `observationtype:imaging`:
* `filter`: Must be `g`, `r`, `i`, or `z`
* `maskid`: can be `110` or a predefined mask set up prior to target request
* `exposuretime`: The observation exposure time in seconds

For MMIRS `observationtype:imaging`:
* `filter`: Must be `J`, `H`, `K`, or `Ks`
* `dithersize`: Must be `5`, `7`, `10`, `15`, `20`, `30`, `60`, `120`, or `210`
* `readtab`: Must be `ramp_4.426` or ramp_1.475`
* `maskid`: can be `110` or a predefined mask set up prior to target request
* `exposuretime`: The observation exposure time in seconds

For Binospec `observationtype:longslit`:
* `grating`: Valid options are `270`, `600`, and `1000`
* `centralwavelength`: Depending on the chosen `grating`:
  * For `grating=270`, valid options are between `5501-7838`
  * For `grating=600`, valid options are between `5146-8783`
  * For `grating=1000`, valid options are between `4108-4683`, `5181-7273`, `7363-7967`, `8153-8772` or `8897-9279`
* `slitwidth`: valid options are `Longslit0_75`, `Longslit1`, `Longslit1_25`, `Longslit1_5`, `Longslit5`
* `filter`: valid options are `LP3800` or `LP3500`. Defaults to `LP3800`
* `maskid`: Can be a predefined mask, or there are common `maskid`s depending on the chosen slitwidth:
  * For `Longslit0_75`: id `113`
  * For `Longslit1`: id `111`
  * For `Longslit1_25`: id `131`
  * For `Longslit1_5`: id `114`
  * For `Longslit5`: id `112`
* `exposuretime`: The observation exposure time in seconds

For MMIRS `observationtype:longslit`:
* `grism`: Valid options are `J`, `HK`, and `HK3`
* `filter`: valid options are `Y`, `J`, `H`, `Ks`, `zJ`, `HK`, `HK3`, `Kspec`
* `readtab`: Valid options are `ramp_4.426`
* `slitwidth`: valid options are `1pixel`, `2pixel`, `3pixel`, `4pixel`, `5pixel`, `6pixel`, `12pixel`
* `slitwidthproperty`: valid options are 'long', 'short'
* `maskid`: Can be a predefined machined mask, or a preset for imaging or spectroscopy:
  * For imaging: id `110`
  * For spectroscopy: id `111`
* `exposuretime`: The observation exposure time in seconds

Other observation metadata:

* `pa`: The parralactic angle. Defaults to 0
* `pm_ra` and `pm_dec`: Proper motion of of the RA and DEC parameters. Defaults to 0.0 respectively
* `numberexposures`: Number of exposures. Defaults to 1
* `visits`: Visits. Defaults to 1
* `priority`: Ranks for all targets in the users catalog. Valid options are 1,2,3 where 1 is the highest priority. Defaults to 3
* `photometric`: Valid options are 0 for non-photometric conditions or 1 for photometric conditions. Defaults to 0
* `targetofopportunity`: Valid options are 0 for non ToO or 1 for requesting a ToO.

All metadata will be validated upon initialization. Once the target object has been validated as True, it can be posted to the MMT schedule.

```python
import pymmt

#example for Binospec imaging target payload:
payload = {
  'objectid':'TARGETNAME',
  'ra':'12:34:56.78',
  'dec':'+87:65:43:21',
  'magnitude':21,
  'epoch':2000,
  'filter':g,
  'maskid':110,
  'exposuretime':400,
  'visits':1,
  'numberexposures':2,
  'priority':1
}


#example payload for Binospec longslit target payload
payload = {
  'objectid':'Targetname',
  'ra':'12:34:56.78',
  'dec':'+87:65:43:21',
  'magnitude':21,
  'epoch':2000,
  'grating':1000,
  'centralwavelength':7380,
  'slitwidth':'Longslit1_25',
  `maskid`:131,
  `filter`:'LP380'
  'visits':1,
  'exposuretime':900,
  'numberexposures':2,
  'priority':1,
  'targetofopportunity':1
}

#example payload for MMIRS longslit target payload
payload = {
  'objectid': 'AT2021fxy',
  'ra': '13:13:01.560',
  'dec': '-19:30:45.100',
  'epoch': 'J2000',
  'exposuretime': 450.0,
  'filter': 'zJ',
  'grism': 'J',
  'magnitude': 16.9,
  'maskid': 111,
  'notes': 'Demo observation request. Please do not observe this.',
  'numberexposures': 3,
  'observationtype': 'longslit',
  'priority': 3,
  'slitwidth': '1pixel',
  'targetofopportunity': 0,
  'visits': 1,
  'instrumentid':15,
  'gain':'low',
  'readtab': 'ramp_4.426',
  'slitwidthproperty':'long',
  'dithersize':'5'
  }

#this will create the target along with validating the payload information. It will inform the user of any errors or warnings associated with the metadata
target = pymmt.Target(token=API_TOKEN, 
                      verbose=True, 
                      payload=payload)
#this will send the information to the scheduler if it is a valid target
target.post()

#this will create the target along with validating the payload information. It will inform the user of any errors or warnings associated with the metadata
target = pymmt.Target(token=API_TOKEN, 
                      verbose=True, 
                      payload=payload)
#this will send the information to the scheduler if it is a valid target
target.post()
```

### Getting Target Information

To get Target Information the only parameters to be passed into the Target class initation are the `token` and `targetid`. This will populate the Target with all of the MMT Target's keywords. If the request is successful, print out all of the target information with the `.dump()` method.

```python
import pymmt

target = pymmt.Target(token=API_TOKEN,
                      verbose=True,
                      payload={'targetid':TARGETID})
target.dump()
```

### Uploading a Finder Image

Once a target is either created, or retrieved with the API GET method, a finder image can be uploaded. If an finder image already exists, this will overwrite it. All that is needed the pathway to the finder image.

```python
target.upload_finder(finder_path=PATH_TO_IMAGE)
```

### Downloading a completed observation

```python
target.download_exposures()
```

### Updating Target Information

Once a target is created, or retrieved with the API GET method, its meta-data can be updated. All that is required is passing in the valid keyword arguments and their respective values. The updated information will be validated before being submitted to the API.

```python
#the kwargs can be defined as: KEY_WORD1=VAlUE1, KEY_WORD2=VALUE2... etc 
target.update(KEY_WORD1=VAlUE1, KEY_WORD2=VALUE2... etc)
```

Valid MMT Target `KEY_WORD`'s:

```python
[
  'id', 'ra', 'objectid', 'observationtype', 'moon', 'seeing', 'photometric', 'priority', 'dec', 'ra_decimal', 
  'dec_decimal', 'pm_ra', 'pm_dec', 'magnitude', 'exposuretime', 'numberexposures', 'visits', 
  'onevisitpernight', 'filter', 'grism', 'grating', 'centralwavelength', 'readtab', 'gain', 'dithersize', 
  'epoch', 'submitted', 'modified', 'notes', 'pa', 'maskid', 'slitwidth', 'slitwidthproperty', 'iscomplete',
  'disabled', 'notify', 'locked', 'findingchartfilename', 'instrumentid', 'targetofopportunity', 'reduced',
  'exposuretimeremaining', 'totallength', 'totallengthformatted', 'exposuretimeremainingformatted', 
  'exposuretimecompleted', 'percentcompleted', 'offsetstars', 'details', 'mask'
]
```

### Deleting a Target

Once a target is created or retireved with the API GET method, it can be deleted from the Observatory scheduler.

```python
target.delete()
```

## Other API Endpoints

### MMT Instrument

Here we describe the API endpoint to get the current instruments in the most recent published schedule. When instantiating a Target through this API it will validate whether or not the Binospec instrument is on the telescope. It can also be used to see what instruments are currently on, or when an instrument will be on the telescope.

This function takes can take in two parameters:
* `date` 
* `instrumentid`

if you don't pass any params into the function it will just find the current instruments on the telescope using `datetime.datetime.now()`

```python
from datetime import datetime, timedelta
insts = pymmt.Instruments()
current_instruments = insts.get_instruments()

#you can look into the future to see what instruments will be available:
future_instruments = insts.get_instruments(date=datetime.datetime.now()+timedelta(months=1))

#you can look through the entire published schedule to see when a certain instrument will be on the telescope (Binospec = 16, MMIRS = 15)
my_instrument = insts.get_instruments(instrumentid=16)
```

This function returns a list of dictionary elements with the values for: 
* `instrumentid` - ID for the instrument
* `name` -  the name of the queue run
* `start` - start date
* `end` - end date
