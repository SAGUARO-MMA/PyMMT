import pymmt

#example for Binospec imaging target payload:

payload = {
  'objectid':'TARGETNAME',
  'ra':'12:34:56.78',
  'dec':'+87:65:43:21',
  'magnitude':21,
  'epoch':2000,
  'filter':'g',
  'maskid':110,
  'exposuretime':400,
  'visits':1,
  'numberexposures':2,
  'priority':1,
  'instrumentid':6,
  'observationtype': 'imaging',
}

mmtcam_token=''
target = pymmt.Target(token=mmtcam_token, 
                      verbose=True, 
                      payload=payload)
target.dump()
print(target.message)
target.post()
