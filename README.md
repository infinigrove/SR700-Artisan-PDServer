# SR700-Artisan-PDServer
Python Pyro PID Daemon server for Fresh Roast SR700 for use with Artisan roasting software.

This allows for connection of Fresh Roast SR700 coffee roaster with Artisan roasting software.

# Drivers

Please refer to OpenRoast wiki page on [installing drivers](https://github.com/Roastero/Openroast/wiki/Installing-Drivers) to ensure you have the appropriate drivers installed.

# Setting Up A Development Environment

Requirements are Python3, [Artisan](https://github.com/artisan-roaster-scope/artisan/releases) (tested with v0.9.9)

Ubuntu Linux

    sudo apt-get install git python3 python3-pip
    git clone https://github.com/infinigrove/SR700-Artisan-PDServer.git
    cd SR700-Artisan-PDServer
    pip3 install -r requirements.txt
    sudo ./Install.linux.sh
    
The Install.linux.sh will install the commands in the Artisan directory /usr/share/artisan/SR700/  if your commands are not installed there then alter your Artisan configuration accordingly.

Make sure the Fresh Roast SR700 roaster is connected before starting the server.

    ./StartSAPDServer.sh

# Configure Artisan BT bean temperature

Start Artisan, click Config->Device from the drop-down menu.  In the Device Assignment dialog box select "Program" and replace "test.py" with "/usr/share/artisan/SR700/Get_Artisan_Temp.py" and click "OK"

# Configure Artisan Sliders

Click Config->Events from the drop-down menu.  In the "Event Types" row change the following

    1 "Speed" to "Timer"
    2 "Power" to "Temperature"
    
Click the "Sliders" tab and check the box for "Timer", "Temperature",  and "Fan" and select an Action of "Call Program" for each.  Then set them up as follows:

    Timer Command = "/usr/share/artisan/SR700/Roaster_Set_Time.py {}", Offset = 1, Factor = 6.00
    Temperature Command = "/usr/share/artisan/SR700/Roaster_Set_Temp.py {}", Offset = 50, Factor = 5.00
    Fan Command = "/usr/share/artisan/SR700/Roaster_Set_Fan.py {}", Offset = 0, Factor = 0.10
    
**Note:** Artisan Sliders range from 0-100 so all controls are based on that scale.  Temperature scale is 20 = 150, 40 = 250, 60 = 350, 80 = 450, 100 = 550.  Also, setting the temp below/lower 20 = 150 will cause the roaster to go into colling cycle.

# Configue Artisan Alarms

(see samples in alarms dir)