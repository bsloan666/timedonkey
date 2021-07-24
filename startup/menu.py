import os
import datetime
import nuke


def save_record(app, action):
    current = datetime.datetime.now()
    timestr = current.strftime("%Y-%m-%d %H:%M:%S")
    if nuke.root().name() == 'Root' or action == 'save':
        with open('{0}/.activitylog'.format(os.getenv('HOME')), 'a') as handle:
            handle.write(timestr + ',' + app + ',' + action + ',' + os.path.basename(nuke.root().name()) + '\n')
        


save_record('nuke', 'open')
nuke.addOnScriptSave(save_record, args=('nuke', 'save'))
nuke.addOnScriptClose(save_record, args=('nuke', 'close'))
