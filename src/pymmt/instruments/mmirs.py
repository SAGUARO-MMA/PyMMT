
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
            if 'gain' in selfkeys:
                gain = selfdict['gain']
                if gain not in ['low']:
                    errors.append('Field \'gain\' is required. Valid options is: low')
            else:
                errors.append('For observationtype:longlist, field \'gain\' is required. Valid options is: low')

            if 'readtab' in selfkeys:
                readtab = selfdict['readtab']
                if readtab not in ['ramp_4.426']:
                    errors.append('Field \'readtab\' is required. Valid options is:ramp_4.426')
            else: 
                errors.append('For observationtype:longlist, field \'readtab\' is required. Valid options is: ramp_4.426')

            if 'grism' in selfkeys:
                grism = selfdict['grism']
                if grism not in ['J','HK', 'HK3']:
                    errors.append('Field \'grism\' is required. Valid options are: J, HK, HK3')
            else:
                errors.append('For observationtype:longlist, field \'grism\' is required. Valid options are: J, HK, HK3 ')
            

            if 'slitwidth' in selfkeys:
                slitwidth = selfdict['slitwidth']
                if slitwidth not in ['1pixel', '2pixel', '3pixel', '4pixel', '5pixel','6pixel','12pixel']:
                    errors.append('Field \'slitwidth\' valid options are: 1pixel, 2pixel, 3pixel, 4pixel, 5pixel,6pixel,12pixel')
            else:
                errors.append('For observationtype: longslit, field \'slitwidth\' is required. Valid options are: 1pixel, 2pixel, 3pixel, 4pixel, 5pixel,6pixel,12pixel')
            
            if 'slitwidthproperty' in selfkeys:
                slitwidthproperty = selfdict['slitwidthproperty']
                if slitwidthproperty not in ['long', 'short']:
                    errors.append('Field \'slitwidthproperties\' valid options are: long, short')
            else:
                errors.append('For observationtype: longlist, slitwidthproperty is required. Valid options are: long, short') 



        if observationtype == 'imaging':
            # self.__dict__.update({'centralwavelength':None})
            # self.__dict__.update({'grating':None})
            if 'gain' in selfkeys:
                gain = selfdict['gain']
                if gain not in ['high']:
                    errors.append('Field \'gain\' is required. Valid options is: high')
            else:
                errors.append('For observationtype:imagin, field \'gain\' is required. Valid options is: high')

            if 'dithersize' in selfkeys:
                dithersize = selfdict['dithersize']
                if dithersize not in ['5', '7','10','15','20','30','60','120','210']:
                    warnings.append('For observationtype: imaging, valid options for field \'dithersize\' are: \'5\', \'7\',\'10\',\'15\',\'20\',\'30\',\'60\',\'120\',\'210\' \n \
                                Default setting \'dithersize\' to \'7\'')
            
            if 'readtab' in selfkeys:
                readtab = selfdict['readtab']
                if readtab not in ['ramp_4.426','ramp_1.475']:
                    errors.append('Field \'readtab\' is required. Valid options is:ramp_4.426, ramp_1.475')
            else: errors.append('For observationtype:longlist, field \'readtab\' is required. Valid options is: 4.426, 1.475')


        if 'filter' in selfkeys:
            filt = selfdict['filter']
            if observationtype == 'imaging' and filt not in ['J', 'H', 'K', 'Ks']:
                errors.append('For observationtype: imaging, valid options for field \'filter\' are: \'J\', \'H\', \'K\', and \'Ks\'.')
            if observationtype == 'longslit' and filt not in ['HK', 'zJ']:
                warnings.append('For observationtype: longslit, valid options for field \'filter\' are: \'HK\' and \'zJ\' \n ')
        else:
            if observationtype == 'longslit':
                update_dict['filter'] ='HK'
            errors.append('Field \'filter\' is required for observation types \'imaging\' and \'longslit\' \n \
                        For imaging: valid options are \'J\', \'H\', \'K\', and \'Ks\'. \n \
                        For longslit: valid options are \'HK\' (default) and \'zJ\'')

        if 'onevisitpernight' not in selfkeys:
            if observationtype == 'imaging':
                update_dict['onevisitpernight']=0
            if observationtype == 'longslit':
                update_dict['onevisitpernight']=1
        else:
            onevisitpernight = selfdict['onevisitpernight']
            if onevisitpernight not in [0, 1]:
                errors.append('Field \'onevisitpernight\' must be either 0 or 1')

    else:
        errors.append('Field \'observationtype\' is required. Valid values are \'longslit\', \'imaging\', and \'mask\'')

    return errors, warnings, update_dict
