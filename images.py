#!/usr/bin/env python

import sys
import os
from tqdm import tqdm
import time
import glob
from astropy.io import fits
import numpy as np

def download():
    result=os.system('wget https://lofar-surveys.org/public/uksrc-test-data/lofar_images.tar')
    if result!=0:
        raise RuntimeError('Download failed!')
    result=os.system('tar xvf lofar_images.tar')
    if result!=0:
        raise RuntimeError('Untar failed!')

if __name__=='__main__':
    print('Running toy FITS image processing benchmark')
    try:
        wd=sys.argv[1]
    except IndexError:
        print('A working directory must be supplied')
        raise

    os.chdir(wd)

    try:
        operation=sys.argv[2]
    except IndexError:
        operation='benchmark'

    if operation not in ['download','benchmark']:
        raise RuntimeError('Unknown operation %s specified' % operation)

    print('Running operation',operation)
    
    if operation=='download':
        download()
    elif operation=='benchmark':
        files=glob.glob('*-mosaic.fits')
        if len(files)==0:
            download()
            files=glob.glob('*-mosaic.fits')

        times=[]
        count=5
        outfile='output.fits'
        for i in tqdm(range(count)):
            if os.path.isfile(outfile):
                os.unlink(outfile)
            st=time.time()
            for i,f in enumerate(files):
                hdu=fits.open(f)
                if not i:
                    isum=np.where(np.isnan(hdu[0].data),0,hdu[0].data)
                    count=np.where(np.isnan(hdu[0].data),0,1)
                else:
                    isum+=np.where(np.isnan(hdu[0].data),0,hdu[0].data)
                    count+=np.where(np.isnan(hdu[0].data),0,1)
            isum/=count
            hdu[0].data=isum
            hdu[0].header['OBJECT']='STACK'
            hdu.writeto(outfile)
            et=time.time()
            times.append(et-st)
        print('Average execution time %f seconds' % np.mean(times))
        print('Max execution time %f seconds' % np.max(times))
        print('Std dev of execution time %f seconds' % np.std(times))
