pmCommand.py
==========

We recently purchased an Avocent ACS6016 and six Avocent PM3009H PDUs to be
used in a new server rack at our data center.

In comparison to the 'old' ACS16, the new ACS6016 has a quite different user
interface. Instead of being able to just edit /etc/portslave/pslave.conf and
using the pmCommand utility to manage powering on or off outlets, only a new
webGUI and a cli are available to fulfill these tasks.

Imagine you have a single device with dual PSU connected to two different
PDUs. Imagine you're at your data center location, and you're in need of a
enable or disable both of them, on different PDUs.

Using the new ACS6016 cli you have to navigate through a multi-level cli
issuing really too much commands to reach the right place where you can
actually turn on or turn off an outlet, which is just too cumbersome to
deal with.

Say hello to pmCommand.py, a replacement for the pmCommand utility that
was available on the former ACS devices of Avocent.

pmCommand.py leverages the XML RPC web interface of the ACS6k to provide
the same level of usability that the pmCommand utility on the old ACS
deviced provided.

	~/src/git/pmCommand.py/src (develop) 0-$ ./pmCommand.py admin@10.140.32.15
	Enter password for admin@10.140.32.15:
	pmCommand(10.140.32.15): help
	pmCommand strikes back!

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
	pmCommand(10.140.32.15): listipdus

	  PDU ID        Vendor   Model          Position  Status   Outlets (On/Total)  Current (A)  Power (W)  Alarm 
	  ============  =======  =============  ========  =======  ==================  ===========  =========  ======
	  20-ba-acP0_1  Avocent  PM3010/10/16A  ttyS2/3   On Line  10/10               1.5          313.0      Normal
	  power2        Avocent  PM3010/10/16A  ttyS2/1   On Line  0/10                0.0          0.0        Normal
	  power3        Avocent  PM3010/10/16A  ttyS1/1   On Line  5/10                1.4          300.0      Normal
	  power4        Avocent  PM3010/10/16A  ttyS2/2   On Line  5/10                1.5          302.0      Normal
	  power5        Avocent  PM3010/10/16A  ttyS1/2   On Line  3/10                1.5          307.0      Normal

	pmCommand(10.140.32.15): pmCommand(10.140.32.15): status all

	  Outlet            Name              Status       Current (A)
	  ================  ================  ===========  ===========
	  20-ba-acP0_1[1]   20-ba-acP0_1_1    ON           0.7        
	  20-ba-acP0_1[2]   20-ba-acP0_1_2    ON           0.4        
	  20-ba-acP0_1[3]   20-ba-acP0_1_3    ON           0.3        
	  20-ba-acP0_1[4]   20-ba-acP0_1_4    ON           0.0        
	  20-ba-acP0_1[5]   20-ba-acP0_1_5    ON           0.0        
	  20-ba-acP0_1[6]   20-ba-acP0_1_6    ON           0.0        
	  20-ba-acP0_1[7]   20-ba-acP0_1_7    ON           0.0        
	  20-ba-acP0_1[8]   20-ba-acP0_1_8    ON           0.0        
	  20-ba-acP0_1[9]   20-ba-acP0_1_9    ON           0.0        
	  20-ba-acP0_1[10]  20-ba-acP0_1_10   ON           0.0        
	  [...]

	pmCommand(10.140.32.15): off 20-ba-acP0_1[7]
	INFO: 20-ba-acP0_1[7]: status of outlet 20-ba-acP0_1_7 is now: OFF
	pmCommand(10.140.32.15): lock 20-ba-acP0_1[7]
	INFO: 20-ba-acP0_1[7]: status of outlet 20-ba-acP0_1_7 is now: OFF(locked)
	pmCommand(10.140.32.15): off 20-ba-acP0_1[8],20-ba-acP0_1[9]
	INFO: 20-ba-acP0_1[8]: status of outlet 20-ba-acP0_1_8 is now: OFF
	INFO: 20-ba-acP0_1[9]: status of outlet 20-ba-acP0_1_9 is now: OFF
	pmCommand(10.140.32.15): unlock 20-ba-acP0_1[7],20-ba-acP0_1[8],20-ba-acP0_1[9]
	INFO: 20-ba-acP0_1[7]: status of outlet 20-ba-acP0_1_7 is now: OFF
	INFO: 20-ba-acP0_1[8]: status of outlet 20-ba-acP0_1_8 is now: OFF
	INFO: 20-ba-acP0_1[9]: status of outlet 20-ba-acP0_1_9 is now: OFF
	pmCommand(10.140.32.15): on 20-ba-acP0_1[7],20-ba-acP0_1[8],20-ba-acP0_1[9]
	INFO: 20-ba-acP0_1[7]: status of outlet 20-ba-acP0_1_7 is now: ON
	INFO: 20-ba-acP0_1[8]: status of outlet 20-ba-acP0_1_8 is now: ON
	INFO: 20-ba-acP0_1[9]: status of outlet 20-ba-acP0_1_9 is now: ON

pmCommand.py tries to implement the most used (by us) commands from the old pmCommand
