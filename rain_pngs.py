import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from scipy import ndimage

# Get all the paths to the image directories (dirs should contain only niftis)
# TODO: get them all
file_path = 'Datasets/GAZE_PRF/sub-001_ses-03_anat_sub-001_ses-03_acq-ADNI_run-2_T1w.nii.gz'

# Load the nifti image data
niimg_array = nib.load(file_path).get_fdata()

# Dimensions of array (num of coronal, axial, sagittal slices)
cr_dim, ax_dim, sg_dim = niimg_array.shape

# Select a part in the middle in each direction
# (which part determined visually on one example)
ax_arr = niimg_array[:, ax_dim//2 : ax_dim-ax_dim//6, :]
cr_arr = niimg_array[cr_dim//4 : cr_dim-cr_dim//5, :, :]
sg_arr = niimg_array[:, :, sg_dim//4 : sg_dim-sg_dim//4]

# Coronal and sagittal images must be rotated
sg_arr = ndimage.rotate(sg_arr, 90)
cr_arr = ndimage.rotate(cr_arr, 180)

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