import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from scipy import ndimage

# Get all the paths to the image directories (dirs should contain only niftis)
# TODO: get them all
file_path = ''

# Load the nifti image data
niimg_array = nib.load(file_path).get_fdata()

# If the image is 4D, i.e. a time series, only take the first volume (- this balances the amount of high and low detail images and is simpler to implement)
if len(niimg_array.shape) == 4:
    niimg_array = niimg_array[:,:,:,0]

# Dimensions of array (num of coronal, axial, sagittal slices)
cr_dim, ax_dim, sg_dim = niimg_array.shape

def cut_in_plane(plane, cut, arr):
    '''
    Cut a nifti image array along a specified plane (axial, coronal, sagittal). Can cut a single slice, or a section. The array must be 3 dimensional.

    args:
        plane (string): Plane to cut along, must be one of 'ax', 'cr', 'sg'
        cut (int or tuple of int): index at which to cut or (start, stop) indexes of cut
        arr (list of float): Niimg array (3D) to be cut
    
    returns:
        cut_arr (list of float): Niimg array cut as specified. Empty array if input is invalid
    '''
    cut_arr = np.array([])
    if plane=='ax':
        cut_arr = arr[:,cut[0]:cut[1],:] if type(cut) is tuple else arr[:,cut,:]
    if plane=='cr':
        cut_arr = arr[cut[0]:cut[1],:,:] if type(cut) is tuple else arr[cut,:,:]
    if plane=='sg':
        cut_arr = arr[:,:,cut[0]:cut[1]] if type(cut) is tuple else arr[:,:,cut]
    return cut_arr

# Select a part in the middle in each direction
# (which part determined visually on one example)
ax_arr = cut_in_plane('ax', (ax_dim//2, ax_dim-ax_dim//6), niimg_array)
cr_arr = cut_in_plane('cr', (cr_dim//4, cr_dim-cr_dim//5), niimg_array)
sg_arr = cut_in_plane('sg', (sg_dim//4, sg_dim-sg_dim//4), niimg_array)

# Coronal and sagittal images must be rotated
sg_arr = ndimage.rotate(sg_arr, 90)
cr_arr = ndimage.rotate(cr_arr, 180)

# TODO: Put this in a function for readability
# Slice em and save em
print('axial')
for slice in np.linspace(0, ax_arr.shape[1], num=10, dtype=np.uint16, endpoint=False):
    plt.imsave('Images/ax_{}_someid.png'.format(slice), 
        ax_arr[:,slice,:], cmap='gray')                    # axial

print('coronal')
for slice in np.linspace(0, cr_arr.shape[0], num=10, dtype=np.uint16, endpoint=False):
    plt.imsave('Images/cr_{}_someid.png'.format(slice), 
        cr_arr[slice,:,:], cmap='gray')                  # coronal

print('sagittal')
for slice in np.linspace(0, sg_arr.shape[2], num=10, dtype=np.uint16, endpoint=False):
    plt.imsave('Images/sg_{}_someid.png'.format(slice), 
        sg_arr[:,:,slice], cmap='gray')                 # sagittal