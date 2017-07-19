""" An example "analysis". """

import eventfile
import numpy as np
import matplotlib.pyplot as plt

# this line allows us to access the Django database:
from modulejournal import wsgi
from journal import models

from django.core.files import File


def main():
    module = models.Module.objects.get(pk=2)
    runs = models.RunEntry.objects.filter(module=module)
    for inputrun in runs:
        perform_analysis(inputrun)
    

def perform_analysis(inputrun: models.RunEntry):
    filename = inputrun.data.path

    with open(filename, 'rb') as f:
        header, data = eventfile.read_event_file(f)

    eventsize = 96
    length = len(data)
    summed = None
    nevents = int(length/eventsize)
    print(nevents)
    summed = np.zeros((48,16))
    for i in range(nevents):
        thebytes = data[i*eventsize:i*eventsize+eventsize]
        frame = np.frombuffer(thebytes, dtype=np.uint8)
        hits = np.reshape(np.unpackbits(frame), newshape=(48, 16))

        summed += hits

    
    plt.imshow(summed)
    plt.savefig("temp.png")
    # plt.show()

    with open("temp.png", 'rb') as f:
        df = File(f)
    
        tool = models.AnalysisTool.objects.get(name="SimpleAnalysis")

        toolrun = models.ToolRun(tool=tool)
        toolrun.save()
        toolrun.inputRuns=[inputrun]
        toolrun.save()
        outputimage = models.OutputImage(image=df, toolrun=toolrun)
        outputimage.save()
    

if __name__ == '__main__':
    main()
