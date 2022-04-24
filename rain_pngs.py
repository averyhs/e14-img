from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from scipy import ndimage

# Get subdir as input and put all nii files in a list
subdir = input('subdir: ')
nii_files = list(Path('Datasets/Original/'+subdir).glob('*.nii*'))

# Show sample image to set planes and rotations
# by visual inspection:
# ---
# Load the nifti image data
niimg_array = nib.load(nii_files[0]).get_fdata()

# If the image is 4D, i.e. a time series, only take the first volume
# (balances the amount of high and low detail images 
# and is simpler to implement)
if len(niimg_array.shape) == 4:
    niimg_array = niimg_array[:,:,:,0]

# Show one slice for visual inspection
fig, axs = plt.subplots(1,3)
axs[0].imshow(niimg_array[100,:,:], cmap='gray')
axs[0].set_title('0')
axs[1].imshow(niimg_array[:,100,:], cmap='gray')
axs[1].set_title('1')
axs[2].imshow(niimg_array[:,:,100], cmap='gray')
axs[2].set_title('2')
plt.show()

# After inspection of x,y,z images, enter which corresponds to each axis
# and how much to roate each
axs_dict = {
    'ax':eval(input('Axial axis (0,1,2): ')),
    'cr':eval(input('Coronal axis (0,1,2): ')),
    'sg':eval(input('Sagittal axis (0,1,2): '))
}
rot_dict = {
    'ax':eval(input('Rotate axial images ccw by [deg]: ')),
    'cr':eval(input('Rotate coronal images ccw by [deg]: ')),
    'sg':eval(input('Rotate sagittal images ccw by [deg]: '))
}

# Generate pngs for each file
for cnt, nii_f in enumerate(nii_files, start=1):
    # Load the nifti image data
    niimg_array = nib.load(nii_f).get_fdata()

    # Dimensions of array (num of axial, coronal, sagittal slices)
    dims = niimg_array.shape
    ax_len = dims[axs_dict['ax']]
    cr_len = dims[axs_dict['cr']]
    sg_len = dims[axs_dict['sg']]

    def cut_in_plane(axis, cut, arr):
        '''
        Cut a nifti image array along a specified axis (x, y, z, corresponding in any order to axial, coronal, sagittal planes). Can cut a single slice, or a section. The array must be 3 dimensional.

        args:
            axis (int):
            cut (int or tuple of int):
            arr (list of float):
        
        returns:
            cut_arr (list of float):
        '''
        cut_arr = np.array([])
        if axis==0:
            cut_arr = arr[cut[0]:cut[1],:,:] if type(cut) is tuple else arr[cut,:,:]
        if axis==1:
            cut_arr = arr[:,cut[0]:cut[1],:] if type(cut) is tuple else arr[:,cut,:]
        if axis==2:
            cut_arr = arr[:,:,cut[0]:cut[1]] if type(cut) is tuple else arr[:,:,cut]
        return cut_arr

    # Select a part in the middle in each direction
    # (which part determined visually on one example, hardcoded)
    ax_arr = cut_in_plane(axs_dict['ax'], (ax_len//2, ax_len-ax_len//6), 
        niimg_array)
    cr_arr = cut_in_plane(axs_dict['cr'], (cr_len//4, cr_len-cr_len//5), 
        niimg_array)
    sg_arr = cut_in_plane(axs_dict['sg'], (sg_len//4, sg_len-sg_len//4), 
        niimg_array)

    # Rotate images as required
    ax_arr = ndimage.rotate(ax_arr, rot_dict['ax'], (axs_dict['cr'],axs_dict['sg']))
    cr_arr = ndimage.rotate(cr_arr, rot_dict['cr'], (axs_dict['ax'],axs_dict['sg']))
    sg_arr = ndimage.rotate(sg_arr, rot_dict['sg'], (axs_dict['ax'],axs_dict['cr']))

    # Console update
    print('File {} of {}'.format(cnt, len(nii_files)))

    # TODO: Put this in a function for readability
    # Slice em and save em
    for slice in np.linspace(0, min(ax_arr.shape), num=10, dtype=np.uint16, endpoint=False):
        plt.imsave('Datasets/Axial/ax_{}_{}_{}.png'.format(subdir,cnt,slice), 
            cut_in_plane(axs_dict['ax'], slice, ax_arr), cmap='gray')                    # axial

    for slice in np.linspace(0, min(cr_arr.shape), num=10, dtype=np.uint16, endpoint=False):
        plt.imsave('Datasets/Coronal/cr_{}_{}_{}.png'.format(subdir,cnt,slice), 
            cut_in_plane(axs_dict['cr'], slice, cr_arr), cmap='gray')                  # coronal

    for slice in np.linspace(0, min(sg_arr.shape), num=10, dtype=np.uint16, endpoint=False):
        plt.imsave('Datasets/Sagittal/sg_{}_{}_{}.png'.format(subdir,cnt,slice), 
            cut_in_plane(axs_dict['sg'], slice, sg_arr), cmap='gray')                 # sagittal