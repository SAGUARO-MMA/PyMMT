from .. import isFloat, isInt

def validate(payload={}):
    selfkeys = payload.keys()
    selfdict = payload
    errors, warnings = [], []
    update_dict = {}

    if 'observationtype' in selfkeys:
        observationtype = selfdict['observationtype']

        if observationtype not in ['longslit', 'imaging', 'mask']:
            errors.append('Field \' observationtype\' must be either \'imaging\', \'longslit\', or \'mask\'')

        if observationtype == 'longslit':
            if 'grating' in selfkeys:
                grating = selfdict['grating']

                if grating not in ['270', 270, '600', 600, '1000', 1000]:
                    errors.append('For observationtype longslit, valid options for field \'grating\' are \'270\', \'600\', and \'1000\'')

                if 'centralwavelength' in selfkeys:
                    centralwavelength = selfdict['centralwavelength']

                    if isFloat(centralwavelength):
                        cw = float(centralwavelength)
                        if grating in ['270', 270] and not (cw >= 5501 and cw <= 7838):
                            errors.append('For \'grating\' = 270: valid centralwavelength ['+str(centralwavelength)+'] must be between 5501-7838 Angstroms')
                        if grating in ['600', 600] and not (cw >= 5146 and cw <= 8783):
                            errors.append('For \'grating\' = 600: valid centralwavelength ['+str(centralwavelength)+'] must be between 5501-7838 Angstroms')
                        if grating in ['1000', 1000] and not ((cw >= 4108 and cw <= 4683) or (cw >= 5181 and cw <= 7273) or (cw >= 7363 and cw <= 7967) or (cw >= 8153 and cw <= 8772) or (cw >= 8897 and cw <= 9279)):
                            errors.append('For \'grating\' = 1000: valid centralwavelength must be between 4108-4683, 5181-7273, 7363-7967, 8153-8772 or 8897-9279')
                    else:
                        errors.append('Field \'centralwavelength\' must be float')
                else:
                    errors.append('For observationtype: longslit, field \'centralwavelength\' is required \n \
                        Valid options are dependent on the field \'grating\' \n \
                        \'grating\' = 270: valid centralwavelength must be between 5501-7838 Angstroms \n \
                        \'grating\' = 600: valid centralwavelength must be between 5146-8783 Angstroms \n \
                        \'grating\' = 1000: valid centralwavelength must be between 4108-4683, 5181-7273, 7363-7967, 8153-8772 or 8897-9279')

            else:
                errors.append('Field \'grating\' is required for observationtype: longslit \n \
                    Valid options are \'270\', \'600\', and \'1000\'')

            if 'slitwidth' in selfkeys:
                slitwidth = selfdict['slitwidth']
                if slitwidth not in ['Longslit0_75', 'Longslit1', 'Longslit1_25', 'Longslit1_5', 'Longslit5']:
                    errors.append('Field \'slitwidth\' valid options are: Longslit0_75, Longslit1, Longslit1_25, Longslit1_5, and Longslit5')
            else:
                errors.append('For observationtype: longslit, field \'slitwidth\' is required. Valid options are: Longslit0_75, Longslit1, Longslit1_25, Longslit1_5, and Longslit5')


        if observationtype == 'imaging':
            update_dict['centralwavelength'] = None
            update_dict['grating'] =  None

        if 'filter' in selfkeys:
            filt = selfdict['filter']
            if observationtype == 'imaging' and filt not in ['g', 'r', 'i', 'z']:
                errors.append('For observationtype: imaging, valid options for field \'filter\' are: \'g\', \'r\', \'i\', and \'z\'.')
            if observationtype == 'longslit' and filt not in ['LP3800', 'LP3500']:
                warnings.append('For observationtype: longslit, valid options for field \'filter\' are: \'LP3800\' and \'LP3500\' \n \
                                Default setting \'filter\' to \'LP3800\'')
        else:
            if observationtype == 'longslit':
                update_dict['filter'] = 'LP3800'
            errors.append('Field \'filter\' is required for observation types \'imaging\' and \'longslit\' \n \
                        For imaging: valid options are \'g\', \'r\', \'i\', and \'z\'. \n \
                        For longslit: valid options are \'LP3800\' (default) and \'LP3500\'')

        if 'onevisitpernight' not in selfkeys:
            if observationtype == 'imaging':
                update_dict['onevisitpernight'] = 0
            if observationtype == 'longslit':
                update_dict['onevisitpernight'] = 1
        else:
            onevisitpernight = selfdict['onevisitpernight']
            if onevisitpernight not in [0, 1]:
                errors.append('Field \'onevisitpernight\' must be either 0 or 1')

    else:
        errors.append('Field \'observationtype\' is required. Valid values are \'longslit\', \'imaging\', and \'mask\'')

    return errors, warnings, update_dict