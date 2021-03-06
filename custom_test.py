import numpy as np
import keras, os, pickle, scipy, rawpy, scipy.stats
from model2 import *
import tensorflow as tf
from PIL import Image
#from model import *
from multiprocessing import Pool
import subprocess
from Traditional import *
from time import time

def run_bash_command(filename):
    subprocess.Popen("shotwell "+filename, shell = True)

start = 0.0
def custom_test(filename):
    global start
    start = time()
    print("Started clock:\n")
    mod = model()
    rows = {0: (0, 512), 1:(512, 1024), 2:(912, 1424)}
    cols = {0: (0, 512), 1:(512, 1024), 2:(1024, 1536), 3: (1536, 2048), 4:(1616, 2128)}
    mod.load_weights("./weights/weights.166.hdf5")
    traditional_approach(filename)
    image = pre_process(filename)*100.0
    image_outs = np.empty(0)
    for i, r in rows.items():
        temp = np.empty(0)
        for j, c in cols.items():
            img = image[:,r[0]:r[1], c[0]:c[1], :]
            out_img = mod.predict(img)
            out_img = np.squeeze(out_img, axis=0)
            out_img = np.minimum(np.maximum(out_img, 0), 1)
            out_img = out_img * 255
            if(j == 0):
                temp = out_img
            elif(j == 4):
                temp = np.concatenate([temp, out_img[:,864:,:]], axis = 1)
            else:
                temp = np.concatenate([temp, out_img], axis = 1)
        if(i == 0):
            image_outs = temp
        elif(i == 1):
            image_outs = np.concatenate([image_outs, temp], axis = 0)
        else:
            image_outs = np.concatenate([image_outs, temp[224:,:,:]], axis = 0)
    #print(image_outs.shape)
    img = scipy.misc.toimage(image_outs, high=255, low=0, cmin=0, cmax=255)
    img.save('Outputs/'+filename.split('/')[3][:5]+'_fin_v3.png')
    #print(image_outs.shape)
    #pool = Pool()
    #pool.map(run_bash_command, [filename, filename.split('/')[3][:5]+'_fin.png', filename.split('/')[3][:5]+'_trad.png'])


if __name__ == "__main__":
    object_focused_images = ['00224_00_0.1s.ARW', '00202_00_0.033s.ARW', '00204_00_0.1s.ARW', '00205_00_0.1s.ARW', '00189_00_0.1s.ARW']
    outside_images = ['00113_00_0.1s.ARW', '00114_00_0.1s.ARW', '00119_00_0.1s.ARW', '00121_00_0.1s.ARW', '00122_00_0.1s.ARW']
  #  for img in outside_images:
  #      custom_test('./Sony/short/'+img)
    #for img in object_focused_images:
  #      custom_test('./Sony/short/'+img)
    global start
    custom_test(input("Enter image location:\n"))
    print('\nTime taken is %s '% (time()-start))
