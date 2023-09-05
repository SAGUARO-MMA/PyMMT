MMT_JSON_KEYS = ("id", "ra", "objectid", "observationtype", "moon", "seeing", "photometric", "priority", "dec",
                 "ra_decimal", "dec_decimal", "pm_ra", "pm_dec", "magnitude", "exposuretime", "numberexposures",
                 "visits", "onevisitpernight", "filter", "grism", "grating", "centralwavelength", "readtab",
                 "gain", "dithersize", "epoch", "submitted", "modified", "notes", "pa", "maskid", "slitwidth",
                 "slitwidthproperty", "iscomplete", "disabled", "notify", "locked", "findingchartfilename",
                 "instrumentid", "targetofopportunity", "reduced", "exposuretimeremaining", "totallength",
                 "totallengthformatted", "exposuretimeremainingformatted", "exposuretimecompleted",
                 "percentcompleted", "offsetstars", "details", "mask")

LOCAL_TARGET_KEYS = ("partial_download", "downloaded", "local_save", "_id", "delete_date")

MMT_MMIRS_REQUIRED_KEYS = ['ra', 'dec', 'epoch', 'exposuretime', 'observationtype', 'numberexposures', 'filter','grating' \
    ,'instrumentid','magnitude','maskid','objectid','onevisitpernight','pa','pm_dec','pm_ra','priority','slitwidth','slitwidthproperty','visits']
MMT_REQUIRED_KEYS = ['ra', 'dec', 'epoch', 'exposuretime', 'observationtype', 'numberexposures', 'observationtype']

def isInt(i):
    try:
        ret = int(i)
        return True
    except:
        return False


def isFloat(i):
    try:
        ret = float(i)
        return True
    except:
        return False


from .pymmt import (
    api,
    Target,
    Instruments,
    Datalist,
    Image,
    Listener
)
