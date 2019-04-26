# CSCI5448-OOAD-IPA

**Name:** Timothy Mason

University of Colorado at Boulder

CSCI 5448 - Object Oriented Design and Analysis

**Project Name:** Image Processing App - Final project for CSCI 5448 Object Oriented Analysis and Design

This is an application to display and edit images.  By running the app, you can open multiple image files, make edits to those images, then save the edited image.  Users have the option to selected different image file formats on saving, and the app could therefore also be used for filetype conversion by opening a file then saving it unedited to a different image filetype.

# Files
```
IPA/ImageVitals.py      Implementation of the ImageVitals class
IPA/IPAModel.py         Implementation of the IPAModel class
IPA/IPAView.py          Implementation of the IPAView class
IPA/rotContrast.png     Image of the word "Contrast" rotated 90 degrees
IPA/ScrolledCanvas.py   Implementation of the ScrolledCanvas class
IPA/IPA.py              Implementation of the IPA class (main entry point for the application)
IPA/rotSaturation.png   Image of the word "Saturation" rotated 90 degrees
IPA/IPAController.py    Implementation of the IPAController class
IPA/rotBrightness.png   Image of the word "Brightness" rotated 90 degrees
README.md               this readme file
IPA.sublime-workspace   workspace file for my programming editor
IPA.sublime-project     project file for my programming editor
```

# Execution

Assumes you have Python 3 installed as the "first hit" in your path (tested with Python 3.6 and 3.7).  Also
assumes you have installed Pillow (https://pillow.readthedocs.io/en/stable/installation.html):

```
pip install Pillow
```

Once the prerequisites are satisfied, launch the application from a terminal / command window.  From within the IPA directory:

Mac / Unix:
```
$ python IPA.py
```

Windows:
```
C:> python IPA.py
```
