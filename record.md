
>the file **opencv_test** is used to test how rotate the image and place to right position. The idea to code the fish position is
making the all angles of rotating image and save those image.
>
>The file **moving_fish** is the main code. And it load the file /data/test.npy.


##using package(install by pip):
* opencv-python(4.1.0.25) :
	using the threading to make console panel and image work independently
* numpy
* pygame

##useful reference:
* [save ndarray](https://stackoverflow.com/questions/28439701/how-to-save-and-load-numpy-array-data-properly)
* [merge image](https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv)
* [package data](https://stackoverflow.com/questions/779495/python-access-data-in-package-subdirectory)
* [multiprocess varible](https://blog.51cto.com/11026142/1874807)

#schedule
10/25:

it can rotating and move the fish well. Next step is tring to reduce (or stableize) the frame time step.

10/28:

using the manager of multiprocessing to approach the goal of 10/25. And redesign the veriable transfer and structure. 