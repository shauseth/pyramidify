# pyramidify
 Plot camera poses in 3D for creating NeRFs.

### Step 1
* Take some images of a scene using any camera.
* Try to revolve around an origin rather than making panoramas.
* Make sure the images aren't blurry.
* Around 30-50 images should be enough.

### Step 2
* Run COLMAP Automatic Reconstruction on the images. ![](https://colmap.github.io)
* Export your model as text files.
* This should give you the following:
```
  camera.txt
  images.txt
  points3D.txt
```
<img src="images/colmap.png" height="342"/>

### Step 2
<img src="images/poses.png" height="342"/>

### Step 3
<img src="images/room.gif" height="342" width="342"/>
