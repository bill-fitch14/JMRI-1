import java
import jmri

# This produces a user interface to Dispatcher to speedily set it up.

# Starting from a system with

# 1) a layout panel setup with track, blocks and signals,
# 2) certain blocks marked as stations, and
# 3) some engines set up with speed profiles

# it creates a system in three easy stages (three button presses) with

# 1) a set of transits and train info files enabling trains to run anywhere on the layout using dispatcher
# 2) A set of station buttons inserted on the panel which allow trains to run station to station under dispatcher
# 3) Provision is made to set up routes so that trains can be sent along these routes
# 4) A scheduler enables trains to run at preset times
# 5) A set of buttons are provided on the panel which enable you to setup and run the system easily

# The system is stored in the Dispatcher System folder, but you can run it using this file

# Procedure
# 1) Run the Toplevel DispatcherSystem.py (this file)
# 2) Read the help accessed from the menu to get detailed instructions on how to run the system

# Note
#the Dispatcher system is stored in folder jython/DispatcherSystem

# Author:  Bill Fitch copyright (c) 2020

RunDispatcherSystem = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/DispatcherSystem.py')
execfile(RunDispatcherSystem)
