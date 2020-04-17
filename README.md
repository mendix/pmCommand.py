pmCommand.py
==========

We recently purchased an Avocent ACS6016 and six Avocent PM3009H PDUs to be
used in a new server rack at our data center.

In comparison to the 'old' ACS16, the new ACS6016 has a quite different user
interface. Instead of being able to just edit `/etc/portslave/pslave.conf` and
using the pmCommand utility to manage powering on or off outlets, only a new
webGUI and a horrible cli are available to fulfill these tasks.

Imagine you have a single device with dual PSU connected to two different
PDUs. Imagine you're at your data center location, and you're in need of a
enable or disable both of them, on different PDUs.

Using the new ACS6016 cli you have to navigate through a multi-level cli
issuing really too much commands to reach the right place where you can
actually turn on or turn off an outlet, which is just too cumbersome to
deal with.

Say hello to pmCommand.py, a replacement for the pmCommand utility that
was available on the former ACS devices of Avocent.

pmCommand.py leverages the XML web interface of the ACS or PM to provide the
same level of usability that the pmCommand utility on the old ACS deviced
provided.

    ~/s/pmCommand.py/src (master) 0-$ ./pmCommand.py https://10.140.32.15
    Enter password for admin:
    INFO - Cyclades ACS6000 - console-zork - Welcome admin!
    pmCommand# help

    Available commands:
     login              Provide password to get a new session at the appliance.
     logout             Logout from the appliance.
     sort               Toggle sorted output for pdu and outlet list
     exit               Exits from the application.
     help               Displays the list of commands.
     listipdus          Lists the IPDUs connected to the appliance.
     on                 Turns on outlets defined in <outlet list>.
     off                Turns off outlets defined in <outlet list>.
     cycle              Power cycles outlets defined in <outlet list>.
     lock               Locks outlets defined in <outlet list> in current state.
     unlock             Unlocks outlets define in <outlet list>.
     status             Displays status of outlets defined in <outlet list>.
     save               Saves configuration to flash.

    Hint: use tab autocompletion for commands!
    pmCommand# listipdus

      PDU ID        Vendor   Model          Position  Status   Outlets (On/Total)  Current (A)  Power (W)  Alarm
      ============  =======  =============  ========  =======  ==================  ===========  =========  ======
      power1        Avocent  PM3010/10/16A  ttyS2/3   On Line  10/10               1.5          313.0      Normal
      power2        Avocent  PM3010/10/16A  ttyS2/1   On Line  0/10                0.0          0.0        Normal
      power3        Avocent  PM3010/10/16A  ttyS1/1   On Line  5/10                1.4          300.0      Normal
      power4        Avocent  PM3010/10/16A  ttyS2/2   On Line  5/10                1.5          302.0      Normal
      power5        Avocent  PM3010/10/16A  ttyS1/2   On Line  3/10                1.5          307.0      Normal

    pmCommand# status all

      Outlet          Name             Status       Bank  Current (A)  Power (W)
      ==============  ===============  ===========  ====  ===========  =========
      power1[1]       foo-L            ON(locked)   N/A   0.4          105.0
      power1[2]       bar-L            ON(locked)   N/A   0.5          121.0
      power1[3]       baz-L            ON(locked)   N/A   0.0          0.0
      power1[4]       quux-L           ON(locked)   N/A   0.5          127.0
      power1[5]       lorem-L          ON(locked)   N/A   0.4          112.0
      power1[6]       ipsum-L          ON(locked)   N/A   0.5          119.0
      power1[7]       quia-L           ON(locked)   N/A   0.3          83.0
      power1[8]       dolor-L          ON(locked)   N/A   0.0          0.0
      power1[9]       sit-L            ON(locked)   N/A   0.3          76.0
      power1[10]      power1-10        OFF(locked)  N/A   0.0          0.0
      power2[1]       foo-R            ON(locked)   N/A   0.5          131.0
      power2[2]       bar-R            ON(locked)   N/A   0.5          124.0
      [...]

    pmCommand# off power1[7]
    INFO: power1[7]: status of outlet quia-L is now: OFF
    pmCommand# lock power1[7]
    INFO: power1[7]: status of outlet quia-L is now: OFF(locked)
    pmCommand# off power1[8],power1[9]
    INFO: power1[8]: status of outlet dolor-L is now: OFF
    INFO: power1[9]: status of outlet sit-L is now: OFF
    pmCommand# unlock power1[7],power1[8],power1[9]
    INFO: power1[7]: status of outlet quia-L is now: OFF
    INFO: power1[8]: status of outlet dolor-L is now: OFF
    INFO: power1[9]: status of outlet sit-L is now: OFF
    pmCommand# on power1[7],power1[8],power1[9]
    INFO: power1[7]: status of outlet quia-L is now: ON
    INFO: power1[8]: status of outlet dolor-L is now: ON
    INFO: power1[9]: status of outlet sit-L is now: ON

pmCommand.py tries to implement the most commonly used commands from the old pmCommand program.
