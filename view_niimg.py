import sys
import matplotlib.pyplot as plt
from nilearn import plotting
from nilearn import image

def view_niimg(path_to_niimg_file):
    '''
    Show a 3D Nifti image at default slice values using NiLearn plotting

    args:
        path_to_niimg_file (string): the file path of the 3D Nifti image to show
    '''
    plotting.plot_anat(path_to_niimg_file)
    plotting.show()

if __name__ == '__main__':
    view_niimg(sys.argv[1])
