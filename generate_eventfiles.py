""" Generates some fake event files for testing. """

import datetime

import numpy as np

import eventfile
import fakedata


def main():
    eventcount = 10000

    thresholds = [0.0099, 0.0095, 0.0090]
    for i, threshold in enumerate(thresholds):
        runnumber = 10000+i
        recorded = datetime.datetime.now().isoformat()+'Z'
        header = {
            'runnumber': runnumber,
            'eventcount': eventcount,
            'threshold': threshold,
            'recorded': recorded
        }
        with open('run%d.run' % runnumber, 'wb') as f:
            eventfile.write_header(f, header)

            for evtno in range(eventcount):
                eventdata = fakedata.create_binary_map(threshold)
                bits = np.packbits(eventdata)
                thebytes = bits.tobytes()
                f.write(thebytes)
        

if __name__ == '__main__':
    main()
