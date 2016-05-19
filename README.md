# Kidprint

--------------------------------------------------------------------------------

### Overview

One of the challenges that doctors in developing countries face is
identification - namely, how to keep track of patients that they have treated
and how to store their information. This becomes even more of a problem when
the patient does not understand or remember their medical information - when
they are infants, for example. This makes even the most basic treatments, such
as vaccinations, very difficult - and a mistake is potentially fatal.

Project Kidprint aims to solve that problem by going back to one of the 
earliest, but most reliable forms of identification - fingerprints. In
conjunction with researchers and graduate students at the Qualcomm Institute at
U.C. San Diego, our goal is to create a modular, intuitive, and cheap way of
reliably reading the fingerprints of infants. While other attempts have been
made, the results have either been unsuccessful, or far too expensive and
inaccessible. We hope to succeed where others have failed by taking a different
approach to solving this problem - rather than take a specific technology and
mold it to our needs, we are choosing to experiment with multiple technologies
and picking the ones that are best suited to the task.

The core steps of the identification process are these:

1. Use a camera to take an image of the fingerprint
  * Automatically adjust the settings of the camera to have optimal clarity
  * Prepare the image to be pipelined
2. Pass the image to a processing device
3. Run the image through an image processing algorithm
4. Use the metadata from the algorithm to search through a database
5. Allow the user to view and modify the information of the infant

### Repository Information
This repository contains the code for the first step - interfacing with the
embedded devices that are used for the project. These include, but are not
limited to, various cameras, an Arduino compatible microprocessor, and an
Arduino compatible Bluetooth module. The camera will be used to take the
pictures of the fingerprints, and the Arduino modules will be used to implement
an autofocus algorithm, that we hope to later adapt to automatically change
light levels. We are rapidly cycling through prototypes, so the specific
technologies are likely to change, but by using OpenCV and Arduino, both widely
accepted standards, we guarantee that this code will be modular across a
multitude of devices.

### Device Information
**Current Camera:**
[See3CAM_CU51](http://www.e-consystems.com/Monochrome-USB-Camera-board.asp)

**Current Arduino board:**
[SparkFun Pro Micro - 5V/16MHz](https://www.sparkfun.com/products/12640)

**Current Arduino Bluetooth module:**
[SparkFun Bluetooth Modem - BlueSMiRF Silver](https://www.sparkfun.com/products/12577)
