import sys
from nilearn import image

def get_niimg_dim(path_to_niimg_file):
    '''
    Get dimension of Nifti image (3D or 4D)

    args:
        path_to_niimg_file (string): the file path of the 3D Nifti image to show
    
    returns:
        dim (int): the number of dimensions of the Nifti image, normally 3 or 4, 
        but returns -1 when an exception is raised
    '''
    try:
        return len(image.load_img(path_to_niimg_file).shape)
    except:
        return -1

if __name__ == '__main__':
    print(get_niimg_dim(sys.argv[1]))