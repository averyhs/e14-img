# -----------------------------------------------
# Remove all Nifti images files that have 4D data
# because idk how to plot it
# Each subdir in Datasets contains only Niftis
# -----------------------------------------------

#!/bin/bash

for D in Datasets/*
do
    if [ -d "${D}" ] # if D is a directory
    then
        for niimg in $D/*
        do
            dim=`python get_niimg_dim.py $niimg`
            echo $dim
            echo $niimg
            if [ $dim != "3" ]
            then
                rm $niimg
            fi
            echo "  "
        done
    fi
done