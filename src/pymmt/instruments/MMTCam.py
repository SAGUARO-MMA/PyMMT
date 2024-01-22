from .. import isFloat, isInt

def validate(payload={}):
    selfkeys = payload.keys()
    selfdict = payload
    errors, warnings = [], []
    update_dict = {}

    if 'observationtype' in selfkeys:
        observationtype = selfdict['observationtype']

        if observationtype not in ['imaging']:
            errors.append('Field \' observationtype\' must be \'imaging\'')


        if observationtype == 'imaging':
            update_dict['centralwavelength'] = None
            update_dict['grating'] =  None

        if 'filter' in selfkeys:
            filt = selfdict['filter']
            if observationtype == 'imaging' and filt not in ['u','g', 'r', 'i', 'z']:
                errors.append('For observationtype: imaging, valid options for field \'filter\' are:\'u\', \'g\', \'r\', \'i\', and \'z\'.')
       
        if 'onevisitpernight' not in selfkeys:
            if observationtype == 'imaging':
                update_dict['onevisitpernight'] = 0


            
           

    return errors, warnings, update_dict
