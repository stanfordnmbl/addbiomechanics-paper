# Data specific trial and file labels. These dictionaries areused to handle filename
# convention inconsistencies specific to the Hamner running dataset.
trial_dict = {'run200': 'Run_200',
              'run300': 'Run_300',
              'run400': 'Run_400',
              'run500': 'Run_500'}
subject_dict = {'subject02': [('run400', '05')],
                'subject03': [('run500', '03')],
                'subject04': [('run500', '04')],
                'subject08': [('run300', '01'), ('run500', '03')],
                'subject17': [('run300', '01'), ('run400', '01'), ('run500', '01')],
                'subject19': [('run200', '01'), ('run300', '01'), ('run400', '01'), ('run500', '01')],
                'subject20': [('run200', '01'), ('run300', '01'), ('run400', '01')]}
init_cycle_dict = {'subject02': [('run300', 2)],
                   'subject10': [('run200', 2), ('run500', 4)],
                   'subject11': [('run200', 2)]}
second_cycle_dict = {'subject02': [('run300', 3), ('run400', 3)],
                     'subject10': [('run200', 5), ('run500', 5)],
                     'subject11': [('run200', 3)]}
final_cycle_dict = {'subject02': [('run300', 4), ('run400', 4)],
                    'subject10': [('run200', 6), ('run500', 7)],
                    'subject11': [('run200', 4)]}