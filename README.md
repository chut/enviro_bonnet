#Setting up Enviro Bonnet with AIY Image

##Setup the Pi and AIY Software
###Get the AIY image
The AIY image already has most of the dependencies installed. This is an easy place to start. However, the image is also configured for many other AIY projects and has a lot of baggage.

1. Download the AIY Image available from (here)[https://drive.google.com/corp/drive/u/0/folders/1u66FKftzIi0d3KTf-cfEc7Ybu51N8-o3].
2. Flash this to your SD Card (8gb or larger). A good tool for this is (Etcher)[https://etcher.io/] on Mac or just dd on Linux. 
3. Boot up your Raspberry Pi and either SSH in or use a keyboard, monitor, and mouse. The AIY image does provide a GUI interface but you won’t need it to get this working. The AIY image use the default login credentials.
..* Username: pi
..* Password: raspberry


###Setup the libraries
Most of the libraries are installed with the AIY image. But we will run pip install anyway.

1. Navigate to the AIY projects directoory.
`cd /home/pi/AIY-projects-python/src`
2. Run `sudo pip3 install .`

##Configure the Enviro Bonnet Examples
There is a sample script for printing sensor data on the OLED and connecting the IoT Core using the crypto chip. There are also some sample helper scripts for setting up your system.

### Get the Code
1. Download or clone the sample code and helper scripts from (Github)[https://github.com/chut/enviro_bonnet] to your home folder (`/home/pi`). *Note: You can clone it other places, but you will have to account for that in other places in the tutorial and modify the later scirpts.*

###Configure for IoT Core
This tutorial assumes you are familiar with the basics of IoT Core. If you need help setting up a project and registry, see the IoT Core docs.

1. Open the `enviro_bonnet/enviro/my_config.ini` file in an editor and put in your corresponding, `ProjectID`, `CloudRegion`, and `RegistryID`.
2. Choose an ID for your device or enter one you have already setup as `DeviceID`. If you are using an already created device, you will still have to add the public key in the next step.
3. Leave `RSACertFile` blank, where we're going, we don’t need certs!

###Setup IoT Core
Lets configure your crypto chip to talk to IoT Core!

####Get your public key
1. You should be working in the `enviro_bonnet/enviro` folder now. If your not run `cd ~/enviro_bonnet/enviro`
2. Run `python3 get_pubkey.py`
3. You should see output similar to:
```
Serial number: 0123...

-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAEYIKoZIzj0DAQcDQgAENvRyrDgkwx7KbcM5Q9OP3vYPc9cp2fCdfil9r5pnXZgirRBu9mcxBEAvmDkP7g4u0BHNADx8hiM62Da2uBLBiA==
-----END PUBLIC KEY-----
```
4. Just copy the key, starting with `-----BEGIN PUBLIC KEY-----` and ending with `-----END PUBLIC KEY-----`
5. Keep it in clipboard or copy it somewhere, you will need it in the next step.


####Create your device in IoT Core
1. Go to (IoT Core)[https://pantheon.corp.google.com/iot] and select the respective project and registry you selected earlier.
2. Hit add device, under Device ID, use the same value you put as `DeviceID` in `my_config.ini` or make something up and put that value in `my_config.ini` as described in "Configure for IoT Core"
3. Select `ES256` as the "Public key format". (Note: Do NOT select `ES256_X509`)
4. Now copy and paste the public key from the previous step into the "Public key value" box. Including the lines at the beginning and end.

##Try it out
You should now be able to run the example code from the Github repo you cloned earlier!

###Start the script
For testing, we want to pass a few extra options to the script, to see if its all working.

1. If not already, `cd /home/pi/enviro_bonnet/enviro`
2. Run `python3 envirobonnet2.py --print-output --upload_delay 10`
.. These extra options will show the output on the terminal, in addition to the OLED as well as configure the data to be sent to IoT Core every 10 seconds (default is every 5min).
3. You should see the OLED come to life on the device. You should see IP, temp, light, and pressure data scrolling by.
4. Your terminal should be displaying similar data
5. You should also see `Message sent Cloud {EXAMPLE}` every 10 seconds.


###See Data in Pub/Sub
The data is being past to whatever topic you specified for events during your registry setup.

####Create a Pub/Sub Subscription
1. Go to Pub/Sub in Pantheon
2. Click the topic you created for your Enviro Hat registry
3. Click "Create Subscription"
4. Enter `enviro_bonnet` for "Subscription name"
5. Select "Pull"
6. Click Create

####View the data from Pub/Sub

1. Click the Cloud Console button in the top right of Pantheon
2. Run `gcloud pubsub subscription enviro_bonnet`
3. You should see data coming in 
4. Keep running the same command to see more data. 


##Start script at boot
If you want the Enviro Bonnet to be used all the time, you can configure the script to start at boot with the inlcuded Systemd Unit script.


1. Copy the enviro.service from `/home/pi/enviro_bonnet/enviro/` to the systemd foler. Run `sudo cp enviro.service /etc/systemd/system/enviro.service`
2. Reload systemd. Run `sudo systemctl daemon-reload`
3. Enable the script to start at boot. Run `sudo systemctl enable enviro.service`
4. Run `sudo reboot` you should see the OLED screen turn on and data start appearing in GCP without doing anything else. 
5. Now as long as your device has power and internet you get secure connectivity. 


