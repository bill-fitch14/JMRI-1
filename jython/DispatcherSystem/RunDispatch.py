###############################################################################
#
# class OptionDialog
# Some Swing dialogs
# 
# class NewTrainMaster *
# Sets up a tran in a section
#
# class StopMaster *
# Turns the dispatch system off
#
# class OffActionMaster *
# allows actions when buttons are turned off
# a) toggles the Setupdispatch SetupRoute buttons
#
# class ResetButtonMaster *
# if a button is turned on, this class turns off all the others.  
# allows only one station button to be active at a time
#
# class MoveTrain
# Calls dispatcher to move train from one station to another
# diven engine and start and end positions
#
# class DispatchMaster *
# monitors the station buttons, and dependent on the mode one is in
# Setup dispatch, setup route, run route
# calls the appropriate action
#
# class RunDispatchMaster
# starts the classes marked with * above in threads so they can do their work
# also starts class scheduler and class simulation which are in different files
# 
###############################################################################
import java
import jmri
import re
from javax.swing import JOptionPane
import os
import imp
import copy
import org 

from javax.swing import JOptionPane, JFrame, JLabel, JButton, JTextField, JFileChooser, JMenu, JMenuItem, JMenuBar,JComboBox,JDialog,JList

import sys

# include the graphcs library
my_path_to_jars = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/jars/jgrapht.jar')
sys.path.append(my_path_to_jars) # add the jar to your path
from org.jgrapht.alg import DijkstraShortestPath
from org.jgrapht.graph import DefaultEdge
from org.jgrapht.graph import DirectedMultigraph

#############################################################################################
#
# Set some global variables
#

logLevel = 0          # for debugging
trains = {}           # dictionary of trains shared over classes
instanceList=[]       # instance list of threads shared over classes
g = None              # graph shared over classes

time_to_stop_in_station = 10000   # time to stop in station in stopping mode(msec)

#############################################################################################
# the file was split up to avoid errors
# so now include the split files

# FileMoveTrain has to go before CreateScheduler
FileMoveTrain = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/MoveTrain.py')
execfile(FileMoveTrain) 

CreateScheduler = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/Scheduler.py')
execfile(CreateScheduler)

CreateSimulation = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/Simulation.py')
execfile(CreateSimulation)

#############################################################################################

#class OptionDialog( java.lang.Runnable ) :
class OptionDialog( jmri.jmrit.automat.AbstractAutomaton ) :
    #
    
    def List(self, title, list_items):
        list = JList(list_items)
        list.setSelectedIndex(0)
        i = []
        print "len i", len(i)
        while len(i) == 0:
            JOptionPane.showMessageDialog(None, list, title, JOptionPane.PLAIN_MESSAGE)
            i = list.getSelectedIndices()
        index = i[0]
        return list_items[index]
    #called  
        # list_items = ("Bruce", "Darrell", "Tony", "Debbie", "Karen")
        # ans = OptionDialog().List(list_items)
        # print ans
        
    #list and option buttons
    def ListOptions(self, list_items, title, options):
        list = JList(list_items)
        list.setSelectedIndex(0)
        s = JOptionPane.showOptionDialog(None,
        list,
        title,
        JOptionPane.YES_NO_OPTION,
        JOptionPane.PLAIN_MESSAGE,
        None,
        options,
        options[1])
        index = list.getSelectedIndices()[0]
        return [list_items[index], options[s]]
        
        # call using
        # list_items = ["list1","list2"]
        # options = ["opt1", "opt2", "opt3"]
        # title = "title"
        # result = OptionDialog().ListOptions(list_items, title, options) 
        # print "result= " ,result[0], "list = ",result[1]
        # result = opt2 list = list1   
    
    def variable_combo_box(self, options, default, msg, title = None, type = JOptionPane.QUESTION_MESSAGE):
    
    
        result = JOptionPane.showInputDialog(
            None,                                   # parentComponent
            msg,                                    # message text
            title,                                  # title
            type,                                   # messageType
            None,                                   # icon
            options,                                # selectionValues
            default                                 # initialSelectionValue
            )
        
        return result  
        
    def displayMessage(self, msg):
        JOptionPane.showMessageDialog(None, msg, 'Message', JOptionPane.WARNING_MESSAGE)
        
    def customQuestionMessage(self, msg, title, opt1, opt2, opt3):
        options = [opt1, opt2, opt3]
        s = JOptionPane.showOptionDialog(None,
        msg,
        title,
        JOptionPane.YES_NO_CANCEL_OPTION,
        JOptionPane.QUESTION_MESSAGE,
        None,
        options,
        options[2])
        return s
        
    def customQuestionMessage2(self, msg, title, opt1, opt2):
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
        msg,
        title,
        JOptionPane.YES_NO_OPTION,
        JOptionPane.QUESTION_MESSAGE,
        None,
        options,
        options[1])
        return s 
        
    def customQuestionMessage2str(self, msg, title, opt1, opt2):
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
        msg,
        title,
        JOptionPane.YES_NO_OPTION,
        JOptionPane.QUESTION_MESSAGE,
        None,
        options,
        options[1])
        if s == JOptionPane.YES_OPTION:
            s1 = opt1
        else:
            s1 = opt2
        return s1 

    def customMessage(self, msg, title, opt1):
        options = [opt1]
        s = JOptionPane.showOptionDialog(None,
        msg,
        title,
        JOptionPane.YES_OPTION,
        JOptionPane.PLAIN_MESSAGE,
        None,
        options,
        options[0])
        return s 
        
    def timedMessage(self, msg):
        
        pane = JOptionPane(msg,  JOptionPane.PLAIN_MESSAGE, JOptionPane.PLAIN_MESSAGE);
        pane.setOptions([])
        pane.showMessageDialog(None, msg, 'Message', JOptionPane.WARNING_MESSAGE)
        # # myDialog=  pane.createDialog(None, "New Topic");
        # # myDialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        # # myDialog.setLocation(1000, 500)
        # # myDialog.setLocationRelativeTo(None)
        # # myDialog.setVisible(True)
        self.waitMsec(1000)
        pane.setVisible(False)


        
        
        
    def input(self,msg):
        x = JOptionPane.showInputDialog(None,msg)
        return x
        
    #def JOptionPane.showConfirmDialog(None, msg, title, JOptionPane.YES_NO_OPTION)

        
    # def bell(self, bell_on = "True"):
        # if bell_on == "True":
            # snd = jmri.jmrit.Sound("resources/sounds/Bell.wav")
            # snd.play() 
            
class modifiableJComboBox:

    def __init__(self,list, msg):
        #list = self.get_all_roster_entries_with_speed_profile()
        jcb = JComboBox(list)
        jcb.setEditable(True)
        JOptionPane.showMessageDialog( None, jcb, msg, JOptionPane.QUESTION_MESSAGE)
        self.ans = str(jcb.getSelectedItem())
         
    def return_val(self):
        return self.ans
        
           
            
#        
# instanceList.append(RunDispatch())        
# instanceList[0].start() 
class NewTrainMaster(jmri.jmrit.automat.AbstractAutomaton):

    # responds to the newTrainSensor, and allocates trains available for dispatching
    # we make the allocated flag global as we will use it in DispatchMaster when we dispatch a train
    
    global trains_allocated
    
    #instanceList = []   # List of file based instances
    
    def init(self):
        self.logLevel = 0
        if self.logLevel > 0: print 'Create Stop Thread'

    def setup(self):
        global trains_allocated
        #self.initialise_train()
        newTrainSensor = "newTrainSensor"
        self.new_train_sensor = sensors.getSensor(newTrainSensor)
        if self.new_train_sensor is None:
            return False
        self.new_train_sensor.setKnownState(INACTIVE)
        trains_allocated = []
        return True
        
    def handle(self):
    
        global trains_allocated
        
        #this repeats
        # wait for a sensor requesting to check for new train
        if self.logLevel > 0: print ("wait for a sensor requesting to check for new train")
        
        self.waitSensorActive(self.new_train_sensor)
        self.new_train_sensor.setKnownState(INACTIVE)
        
        #display the allocated trains

        
        station_block_name, new_train_name = self.check_new_train_in_siding()
        if self.logLevel > 0: print "station_block_name",station_block_name, "existing train name", new_train_name
        if station_block_name != None:
            # take actions for new train
            if new_train_name == None:
                # roster_entries_with_speed_profile = self.get_all_roster_entries_with_speed_profile()  
                # if self.logLevel > 0: print roster_entries_with_speed_profile
                # new_train_name = JOptionPane.showInputDialog(None,"Enter engine name", "diesel")
                all_trains = self.get_all_roster_entries_with_speed_profile()
                if all_trains == []:
                    msg = "There are no engines with speed profiles, cannot operate without any"
                    JOptionPane.showMessageDialog(None,msg)
                else:    
       
                    msg = self.get_all_trains_msg()
                    title = None
                    opt1 = "Select train on next optionbox1"
                    
                    OptionDialog().customMessage(msg, title, opt1)
                    msg = "Select the train in " + station_block_name
                    trains_to_choose = self.get_non_allocated_trains() 
                    if trains_to_choose == []:
                        OptionDialog().displayMessage("no more trains with speed profiles \nto select")
                    else:
                        new_train_name = OptionDialog().List(msg, trains_to_choose)
                        #new_train_name = modifiableJComboBox(trains_to_choose,msg).return_val()
                        if new_train_name not in trains_allocated:
                            trains_allocated.append(new_train_name)
                        self.add_to_train_list_and_set_new_train_location(new_train_name, station_block_name)
                        self.set_blockcontents(station_block_name, new_train_name)
            else:
                #allow operator to verify the train
                # all_trains = self.get_all_roster_entries_with_speed_profile()
                # trains_to_choose = copy.copy(all_trains)
                # for train in trains_allocated:
                    # if self.logLevel > 0: print str(trains_to_choose)
                    # if train in trains_to_choose:
                        # trains_to_choose.remove(train)
                trains_to_choose = self.get_non_allocated_trains() 
                
                
                
                msg = "In " + station_block_name + " Select train roster"
                new_train_name = modifiableJComboBox(trains_to_choose,msg).return_val()
                if new_train_name not in trains_allocated:
                    trains_allocated.append(new_train_name)
                self.add_to_train_list_and_set_new_train_location(new_train_name, station_block_name)
                self.set_blockcontents(station_block_name, new_train_name)
                
        else:
            if self.logLevel > 0: print "about to show message no new train in siding"
            msg = self.get_all_trains_msg() 
            msg +=  "\nPut a train in a section so it can be allocated!\n"
            title = "All trains allocated"
            opt1 = "Continue"
            opt2 = "Delete the trains already set up and start again"
            ans = OptionDialog().customQuestionMessage2(msg, title, opt1, opt2)
            if ans == JOptionPane.NO_OPTION:
                self.reset_allocation()
                

            # # if trains_allocated[1:-1] == []:
                # # trains_allocated_msg = "None"
            # # else:
            # trains_allocated_msg = str(trains_allocated)[1:-1]
            # if trains_allocated_msg == "": trains_allocated_msg = "None setup yet"
            # title = "Oh Oh"
            # msg = "Trains set up:\n"+ trains_allocated_msg + "\n\nPut a train in a section so it can be allocated!\n\nContinue(yes) or If you want to delete the trains already set up press (no)"
            # #JOptionPane.showOptionDialog(None,msg)
            # result = JOptionPane.showConfirmDialog(None, msg, title, JOptionPane.YES_NO_OPTION)
            # if result ==  JOptionPane.NO_OPTION:
                # print ("no option")
                # # trains_allocated = []
                # # OptionDialog().displayMessage("try again")
                # self.reset_allocation()
                
                
        return True

    def get_allocated_trains_msg(self):
        allocated_trains =[ str(train) + " in block " + str(trains[train]["edge"].getTarget()) for train in trains_allocated]
        if allocated_trains ==[]:
            msg = "There are no allocated trains \n"
        else:
            msg = "The Allocated trains are: \n" +'\n'.join(allocated_trains)
        return msg
        
        
    def get_non_allocated_trains(self):
        all_trains = self.get_all_roster_entries_with_speed_profile()
        non_allocated_trains = copy.copy(all_trains)
        for train in trains_allocated:
            if train in non_allocated_trains:
                non_allocated_trains.remove(train)
        return non_allocated_trains
        
    def get_non_allocated_trains_msg(self):
        #non_allocated_trains = self.get_non_allocated_trains()
        #return "the non-allocated trains are: \n" +'\n'.join([ str(train)   for train in non_allocated_trains]) 
        trains_in_sections_allocated1 = self.trains_in_sections_allocated()
        msg = "the non-allocated trains are in sections: \n" + "\n".join([ str(train[0]) for train in trains_in_sections_allocated1 if train[2] == "non-allocated"])
        return msg
        
    def get_all_trains_msg(self):
        return self.get_allocated_trains_msg() + "\n" + self.get_non_allocated_trains_msg()
        
    def reset_allocation(self):
        global trains_allocated
        if trains_allocated == []:
            if self.logLevel > 0: print ("a")
            msg = "Nothing to reset"
            OptionDialog().displayMessage(msg)
        else:
            if self.logLevel > 0: print ("b")
            msg = "Select train to modify"
            train_name_to_remove = modifiableJComboBox(trains_allocated,msg).return_val()
            trains_allocated.remove(train_name_to_remove)
            self.new_train_sensor.setKnownState(ACTIVE)
        
    
    def get_all_roster_entries_with_speed_profile(self):
        roster_entries_with_speed_profile = []
        r = jmri.jmrit.roster.Roster.getDefault()
        for roster_entry in jmri.jmrit.roster.Roster.getAllEntries(r):
            if self.logLevel > 0: print "roster_entry.getSpeedProfile()",roster_entry,roster_entry.getSpeedProfile()
            if roster_entry.getSpeedProfile() != None:
                roster_entries_with_speed_profile.append(roster_entry.getId())
                if self.logLevel > 0: print "roster_entry.getId()",roster_entry.getId()
        return roster_entries_with_speed_profile
                
                       
    def add_to_train_list_and_set_new_train_location(self, train_name, station_block_name):
        # trains is a dictionary, with keys of the train_name
        # each value is itself a dictioary with 3 items
        # edge
        # penultimate_block_name
        # direction
        global train
        global trains_allocated
        if train_name not in trains:
            trains[train_name] = {}
            train = trains[train_name]
            train["train_name"] = train_name
        else:
            #train_name = self.get_train_name()
            self.set_train_in_block(station_block_name, train_name)
            
        # 2) set the last traversed edge to the edge going into the siding
        edge = None
        for e in g.g_stopping.edgeSet():
            #if self.logLevel > 0: print "************************"
            #if self.logLevel > 0: print e, "Target", e.getTarget()
            #if self.logLevel > 0: print e, "Source", e.getSource()
            LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
            station_block = LayoutBlockManager.getLayoutBlock(station_block_name)
            number_neighbors = station_block.getNumberOfNeighbours()
            in_siding = (number_neighbors == 1)
            for i in range(station_block.getNumberOfNeighbours()):
                neighbor_name = station_block.getNeighbourAtIndex(i).getDisplayName()
                if self.logLevel > 0: print e.getItem("penultimate_block_name"), "station_block_name",station_block_name,"neighbor_name",neighbor_name
                if e.getItem("penultimate_block_name") == neighbor_name:
                    edge = e
                    break
        train["edge"] = edge
        train["penultimate_block_name"] = edge.getItem("penultimate_block_name")
        if self.logLevel > 0: print 
        
        # 3) set direction so can check direction of transit
        
        penultimate_block_name = edge.getItem("penultimate_block_name")
        penultimate_layout_block = LayoutBlockManager.getLayoutBlock(penultimate_block_name)
        saved_state = penultimate_layout_block.getUseExtraColor()
        if not in_siding:
            # highlight the penultimate block
            penultimate_layout_block.setUseExtraColor(True)  
        train["direction"] = self.set_train_direction(station_block_name, in_siding)
        penultimate_layout_block.setUseExtraColor(saved_state)
        
        # 4) add to allocated train list
        if str(train_name) not in trains_allocated:
            trains_allocated.append(str(train_name))
            
    def set_train_direction(self, block_name, in_siding):
    
        options = ["forward", "reverse"]
        default = "forward"
        if in_siding:
            msg = "In block: " + block_name + "\n" +'What way is train facing\nout of junction?'
            #msg = 'What way is train facing\nout of junction?'
        else:
            msg = "In block: " + block_name + "\n" +'What way is train facing\ntowards highlighted block?'
            #msg = 'What way is train facing\ntowards highlighted block?'
        title = "Set Train Facing Direction"
        type = JOptionPane.QUESTION_MESSAGE
        result = OptionDialog().customQuestionMessage2str(msg, title, "forward", "reverse")

        #result = OptionDialog().variable_combo_box(options, default, msg, title, type)
        #new_train_name = OptionDialog().List(msg, options)
        
        if result == "forward":
            train_direction = "reverse"
        else:
            train_direction = "forward"
        return train_direction
        
    def set_train_in_block(self, block_name, train_name):
        mem_val = train_name
        self.set_blockcontents(block_name, mem_val)
        
    def trains_in_sections_allocated(self):
        trains_in_sections_allocated = []
        #trains_in_sections_nonallocated = []
        for station_block_name in g.station_block_list:
            block_value = self.get_blockcontents(station_block_name)
            block_occupied_state = self.check_sensor_state_given_block_name(station_block_name)
            if block_occupied_state == True:
                if block_value not in trains_allocated:
                    trains_in_sections_allocated.append([station_block_name, block_value, "non-allocated"])
                elif (block_value != None and block_value != "" and block_value != "none"):
                    trains_in_sections_allocated.append([station_block_name, block_value, "allocated"])
                else:
                    trains_in_sections_allocated.append([station_block_name, block_value, "other"])
        if self.logLevel > 0: print str(trains_in_sections_allocated)
        return trains_in_sections_allocated
                
        
    def check_new_train_in_siding(self):

        # go through all station
        global trains_allocated
        
        for station_block_name in g.station_block_list:
        
            #get a True if the block block_value has the train name in it
            block_value = self.get_blockcontents(station_block_name)
            if self.logLevel > 0: print " a trains_allocated:", trains_allocated, ": block_value", block_value
            
               
            # if block_value != None:
                # if self.is_roster_entry(block_value):
                    # if self.logLevel > 0: print block_value.getId()
                    # block_value = block_value.getId()
            #get a True if the block is occupied
            block_occupied_state = self.check_sensor_state_given_block_name(station_block_name)
            
            if self.logLevel > 0: print ("station block name {} : block_value {}". format(station_block_name, str(block_value)))
            
            #check if the block is occupied and has the required train in it  
            if (block_value == None or block_value == "" or block_value == "none") and block_occupied_state == True:
                return [station_block_name, None]
            elif block_occupied_state == True and (block_value != None and block_value != "" and block_value != "none"):
                #check if there is already a thread for the train
                #check if the train has already been allocated
                #if self.new_train_thread_required(block_value):
                if block_value not in trains_allocated:
                    return [station_block_name, block_value]
                else:
                    if self.logLevel > 0: print "block_value in trains_allocated"
                    if self.logLevel > 0: print "b trains_allocated:", trains_allocated, ": block_value", block_value
                    pass
            else:
                pass
        return [None, None]

    def is_roster_entry(self, v):
        return type(v) is jmri.jmrit.roster.RosterEntry

    # def new_train_thread_required(self, train_name):
        # for thread in instanceList:
                # if thread is not None:
                    # if thread.isRunning():
                        # existing_train_name = thread.getName() 
                        # if existing_train_name == train_name:
                            # return False
        # return True
        
    def train_thread_exists(self, train_name):
        for thread in instanceList:
                if thread is not None:
                    if thread.isRunning():
                        existing_train_name = thread.getName() 
                        if existing_train_name == train_name:
                            return True
        return False
        
    def create_new_train_thread(self, train_name):
        idx = len(instanceList)
        instanceList.append(RunDispatch())          # Add a new instance
        instanceList[idx].setName(train_name)        # Set the instance name
        #if instanceList[idx].setup():               # Compile the train actions
        instanceList[idx].start()               # Compile was successful
        
        
    def get_blockcontents(self, block_name):
        block = blocks.getBlock(block_name)
        value =  block.getValue()
        return value
        
        
    def set_blockcontents(self, block_name, value):
        block = blocks.getBlock(block_name)
        value =  block.setValue(value)
        

    def check_sensor_state_given_block_name(self, station_block_name):
        #if self.logLevel > 0: print("station block name {}".format(station_block_name))
        layoutBlock = layoutblocks.getLayoutBlock(station_block_name)
        station_sensor = layoutBlock.getOccupancySensor() 
        if station_sensor is None:
            OptionDialog().displayMessage(' Sensor in block {} not found'.format(station_block_name))
            return
        currentState = True if station_sensor.getKnownState() == ACTIVE else False
        return currentState 

       
            
class StopMaster(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        self.logLevel = 0
        if self.logLevel > 0: print 'Create Stop Thread'

    def setup(self):
        self.stop_master_sensor = sensors.getSensor("stopMasterSensor")
        if self.stop_master_sensor is None:
            return False
        self.stop_master_sensor.setKnownState(INACTIVE)
        
        self.start_scheduler = sensors.getSensor("startSchedulerSensor")
        self.start_scheduler.setKnownState(INACTIVE)
        return True

    def handle(self):
        global timebase
        self.waitSensorActive(self.stop_master_sensor)
        #stop all threads
        if self.logLevel > 0: print "instancelist", instanceList
        for thread in instanceList:
            if thread is not None:
                if thread.isRunning():
                    if self.logLevel > 0: print 'Stop "{}" thread'.format(thread.getName())
                    thread.stop()
                else:
                    #need this for scheduler in wait state
                    thread.stop()
        self.new_train_sensor = sensors.getSensor("startDispatcherSensor")
        self.new_train_sensor.setKnownState(INACTIVE)
        try:
            #stop the scheduler timebase listener
            if self.logLevel > 0: print "removing listener"
            timebase.removeMinuteChangeListener(TimeListener())
            return False
        except NameError:
            if self.logLevel > 0: print "Name error"
            return False
        else:
            return False
        

# End of class StopMaster

class OffActionMaster(jmri.jmrit.automat.AbstractAutomaton):

    button_sensors_to_watch = []
    def __init__(self):
        self.logLevel = 0
        
    def init(self):
        if self.logLevel > 0: print 'Create OffActionMaster Thread'
        self.get_run_buttons()
        self.get_route_dispatch_buttons()
        
        self.button_sensors_to_watch = self.run_stop_sensors 
        if self.logLevel > 0: print "button to watch" , str(self.button_sensors_to_watch)
        #wait for one to go inactive
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)      
        self.waitSensorState(button_sensors_to_watch_JavaList, INACTIVE)
        
        if self.logLevel > 0: print "button went inactive"
        sensor_that_went_inactive = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == INACTIVE][0]
        if self.logLevel > 0: print "sensor_that_went_inactive" , sensor_that_went_inactive
        start_sensor = sensors.getSensor("startDispatcherSensor")
        #start_sensor = sensors.getSensor("IS96004")
        stop_sensor =  sensors.getSensor("stopMasterSensor")
        if self.logLevel > 0: print "start_sensor" , start_sensor
        if self.logLevel > 0: print "stop_sensor" , stop_sensor
        if sensor_that_went_inactive in self.run_stop_sensors:
            if self.logLevel > 0: print "run stop sensor went inactive"

            if sensor_that_went_inactive == start_sensor:
                self.sensor_to_look_for = stop_sensor
                if self.logLevel > 0: print "start sensor went inactive"
                if self.logLevel > 0: print "setting stop sensor active"
                stop_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # if self.logLevel > 0: print "setting start sensor active"
                # start_sensor.setKnownState(ACTICE)
            elif sensor_that_went_inactive == stop_sensor:
                self.sensor_to_look_for = start_sensor
                if self.logLevel > 0: print "stop sensor went inactive"
                if self.logLevel > 0: print "setting start sensor active"
                start_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # start_sensor.setKnownState(ACTICE)
                pass#
                
        if self.logLevel > 0: print "finished OffActionMaster setup"

    def setup(self):
        if self.logLevel > 0: print "starting OffActionMaster setup"
        #get dictionary of buttons self.button_dict
        #self.get_route_dispatch_buttons()

        return True
        
    def handle(self):
        if self.logLevel > 0: print "started handle"
        #for pairs of buttons, if one goes off the other is set on
        self.button_sensors_to_watch = self.run_sensor_to_look_for
        if self.logLevel > 0: print "button to watch" , str(self.button_sensors_to_watch)
        #wait for one to go active
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)      
        self.waitSensorState(button_sensors_to_watch_JavaList, INACTIVE)
        #determine which one changed
        if self.logLevel > 0: print "sensor went inactive"
        sensor_that_went_inactive = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == INACTIVE][0]
        
        if sensor_that_went_inactive in self.run_stop_sensors:
            if self.logLevel > 0: print "run stop sensor went inactive"
            start_sensor = sensors.getSensor("startDispatcherSensor")
            #start_sensor = sensors.getSensor("IS96004")
            stop_sensor =  sensors.getSensor("stopMasterSensor")
            if sensor_that_went_inactive == start_sensor:
                self.sensor_to_look_for = stop_sensor
                if self.logLevel > 0: print "start sensor went inactive"
                if self.logLevel > 0: print "setting stop sensor active"
                stop_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # if self.logLevel > 0: print "setting start sensor active"
                # start_sensor.setKnownState(ACTICE)
            elif sensor_that_went_inactive == stop_sensor:
                self.sensor_to_look_for = start_sensor
                if self.logLevel > 0: print "stop sensor went inactive"
                if self.logLevel > 0: print "setting start sensor active"
                start_sensor.setKnownState(ACTIVE)
                
        # if sensor_that_went_inactive in self.route_dispatch_sensors: 
            # if self.logLevel > 0: print "run route dispatch sensor went inactive"
            # route_sensor = sensors.getSensor("setDispatchSensor")
            # dispatch_sensor =  sensors.getSensor("setRouteSensor")
            # if sensor_that_went_inactive == route_sensor:
                # dispatch_sensor.setKnownState(INACTIVE)
            # else:
                # route_sensor.setKnownState(INACTIVE)
                
        if self.logLevel > 0: print "end handle"
        #self.waitMsec(20000)
        return False
    def get_route_dispatch_buttons(self):
        self.route_dispatch_sensors = [sensors.getSensor(sensorName) for sensorName in ["setDispatchSensor","setRouteSensor"]]
        #self.route_dispatch_states = [self.check_sensor_state(rd_sensor) for rd_sensor in self.route_dispatch_sensors]
        pass        
        
    def get_run_buttons(self):
        #self.run_stop_sensors = [sensors.getSensor(sensorName) for sensorName in ["IS96004","stopMasterSensor"]]
        self.run_stop_sensors = [sensors.getSensor(sensorName) for sensorName in ["IS96004"]]



class ResetButtonMaster(jmri.jmrit.automat.AbstractAutomaton):

    # if a button is turned on, this routing turns it off
    # another class will actually respond to the button and do something
    
    button_sensors_to_watch = []
    def __init__(self):
        self.logLevel = 0
        
    def init(self):
        if self.logLevel > 0: print 'Create ResetButtonMaster Thread'

    def setup(self):
        if self.logLevel > 0: print "starting ResetButtonMaster setup"

        #get dictionary of buttons self.button_dict
        self.get_buttons()
        self.get_route_dispatch_buttons()
        #set all move_to buttons inactive
        for sensor in self.button_sensors:
            sensor.setKnownState(INACTIVE)
            
        for sensor in self.route_dispatch_sensors:
            sensor.setKnownState(INACTIVE)
        #store the values in a clone
        #self.store_button_states()
        # #at moment there are no trains so:
        self.button_sensors_to_watch = self.button_sensors + self.route_dispatch_sensors

        if self.logLevel > 0: print "self.button_sensors_to_watch_init", [sensor.getUserName() for sensor in self.button_sensors_to_watch]

        self.sensor_active = None
        self.sensor_active_route_dispatch = None
        self.sensor_active_old = None
        self.sensor_active_route_dispatch_old = None
        
        # #wait for one to go active
        # aJavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
        # if self.logLevel > 0: print aJavaList[0].getUserName()
        # self.waitSensorState(aJavaList, jmri.Sensor.ACTIVE)
        # #determine which one changed
        # self.sensor_active = [sensor for sensor in button_sensors_to_watch if sensor.getKnownState() == ACTIVE][0]
        # #we really need to determine what train it was
          # #just work with one train for now
        # #get the list of sensors to watch
        # self.button_sensors_to_watch = self.button_sensors - [sensor_changed]

        if self.logLevel > 0: print "finished ResetButtonMaster setup"
        return True

    def handle(self):
        #only one button is active. We will keep it that way
        if self.logLevel > 0: print "handle"
        #wait for one to go active
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
        
        self.waitSensorState(button_sensors_to_watch_JavaList, ACTIVE)
        #determine which one changed
        #if self.logLevel > 0: print "sensor went active"
        sensor_active_all = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == ACTIVE][0]
        
        if sensor_active_all in self.button_sensors: 
            self.sensor_active = sensor_active_all
        if sensor_active_all in self.route_dispatch_sensors: 
            self.sensor_active_route_dispatch = sensor_active_all
        
        if self.sensor_active != None and self.sensor_active != self.sensor_active_old:
            self.process_button_sensors(self.sensor_active)
            self.sensor_active_old =self.sensor_active
        if self.sensor_active_route_dispatch != None and self.sensor_active_route_dispatch != self.sensor_active_route_dispatch_old:
            self.process_route_dispatch_sensors(self.sensor_active_route_dispatch)
            self.sensor_active_route_dispatch_old = self.sensor_active_route_dispatch
        
        # exclude the current active buttons from the button to watch
        self.button_sensors_to_watch = self.button_sensors + self.route_dispatch_sensors
        
        if self.sensor_active_old != None:
            self.button_sensors_to_watch.remove(self.sensor_active_old) 
        if self.sensor_active_route_dispatch_old != None:
            if self.logLevel > 0: print "self.sensor_active_route_dispatch_old" , self.sensor_active_route_dispatch_old
            self.button_sensors_to_watch.remove(self.sensor_active_route_dispatch_old)
            
        self.waitMsec(2000)
        return True
        # #if self.logLevel > 0: print "sensor_changed",sensor_changed.getUserName()
        # #set other buttons to inactive
        # if self.sensor_active != None:
            # self.sensor_active.setKnownState(INACTIVE)
            # self.waitMsec(2000)
        # #remember the active button
        # self.sensor_active = sensor_changed
        # #get the list of sensors to watch
        # #if self.logLevel > 0: print "self.button_sensors_to_watch_before_remove", [sensor.getUserName() for sensor in self.button_sensors_to_watch]
        # self.button_sensors_to_watch.remove(sensor_changed)
        # #if self.logLevel > 0: print "self.button_sensors_to_watch", [sensor.getUserName() for sensor in self.button_sensors_to_watch]
        # #if self.logLevel > 0: print "end handle"
        # return True
        
    def process_button_sensors(self, sensor_changed):
        [sensor.setKnownState(INACTIVE) for sensor in self.button_sensors if sensor != sensor_changed]
       
    def process_route_dispatch_sensors(self, sensor_changed):
        if sensor_changed == sensors.getSensor("setDispatchSensor"):
            sensors.getSensor("setRouteSensor").setKnownState(INACTIVE)
            msg = "Press section buttons to set dispatch \nA train needs to be set up in a section first"
            OptionDialog().displayMessage(msg)
            #show the trains setup
            self.show_trains_setup()
        elif sensor_changed == sensors.getSensor("setRouteSensor"):
            sensors.getSensor("setDispatchSensor").setKnownState(INACTIVE)
            msg = "Press section buttons to set route \nThe route may be used to schedule a train"
            OptionDialog().displayMessage(msg)
        elif sensor_changed == sensors.getSensor("runRouteSensor"):  
            self.run_route()
            sensors.getSensor("runRouteSensor").setKnownState(INACTIVE)
            
    def show_trains_setup(self):
        pass
        
    def get_buttons(self):    
        self.button_sensors = [self.get_button_sensor_given_block_name(station_block_name) for station_block_name in g.station_block_list]
        self.button_sensor_states = [self.check_sensor_state(button_sensor) for button_sensor in self.button_sensors]
        # for button_sensor in self.button_sensors:
            # self.button_dict[button_sensor] = self.check_sensor_state(button_sensor)
            
    def get_route_dispatch_buttons(self):
        self.route_dispatch_sensors = [sensors.getSensor(sensorName) for sensorName in ["setDispatchSensor","setRouteSensor","runRouteSensor"]]
        self.route_dispatch_states = [self.check_sensor_state(rd_sensor) for rd_sensor in self.route_dispatch_sensors]
            
    def check_sensor_state(self, sensor):
        #if self.logLevel > 0: print("check_sensor_state",sensor)
        if sensor == None :
            #if self.logLevel > 0: print('Sensor in check_sensor_state is none')
            return None
        #sensor = sensors.getSensor(sensor_name)
        if sensor is None:
            OptionDialog().displayMessage('Sensor {} not found'.format( sensor_name))
            return
        currentState = True if sensor.getKnownState() == ACTIVE else False
        #if self.logLevel > 0: print("check_sensor_state {}".format(currentState))
        return currentState
       
    def store_button_states(self):
        self.button_sensor_states_old = self.button_sensor_states
        if self.logLevel > 0: print "self.button_sensor_states_old",self.button_sensor_states_old
        #self.button_dict_old = dict(self.button_dict)
        
    def get_button_sensor_given_block_name(self, block_name):
        button_sensor_name = "MoveTo"+block_name.replace(" ","_") +"_stored"
        button_sensor = sensors.getSensor(button_sensor_name)
        return button_sensor        
           
    # def reset_buttons(self):
        # for button_dict_old_value, button_dict_value in zip(button_dict_old.iteritems(), button_dict.iteritems()):
            # if button_dict_old_value == button_dict_value:
                # if self.logLevel > 0: print 'Ok', button_dict_old_value, button_dict_value
                # sensor, val = button_dict_old_value
                # if val = True:
                    # sensor.setKnownState(INACTIVE)
            # else:
                # if self.logLevel > 0: print 'Not', button_dict_old_value, button_dict_value
                # sensor, val = button_dict_value
        
    def run_route(self):
        list_items = ("Run Route", "Run Route / Station Combo", "Cancel")
        title = "choose option"
        result = OptionDialog().List(title, list_items)
        if result == "Run Route":
            RouteManager=jmri.InstanceManager.getDefault(jmri.jmrit.operations.routes.RouteManager)
            list_items = RouteManager.getRoutesByNameList()
            title = "choose route"
            routeName = str(OptionDialog().List(title, list_items))
            print "routeName", routeName
            route = RouteManager.getRouteByName(routeName)
            
            list_items = self.get_list_of_engines_to_move()
                    # msg = "trains_to_choose" + str(trains_to_choose)
            if list_items == []:
                return
            title = "what train do you want to move?"
            engine = OptionDialog().List(title, list_items)
            station_from = self.get_position_of_train(engine)
            
            list_items = ["stop at end of route", "return to start position", "return to start position and repeat", "cancel"]
            title = "What do you want to do"
            option = OptionDialog().List(title, list_items)
            repeat = False

            if option == "stop at end of route":
                station_to = None
                repeat = False
            elif option == "return to start position":
                station_to = station_from
                repeat = False
            elif option == "return to start position and repeat":
                station_to = station_from
                repeat = True
            print "station_from",    station_from, "station_to",station_to, "repeat",repeat
            run_train = RunRoute(route, g.g_express, station_from, station_to, repeat)
            run_train.setName("running_route_" + routeName)
            run_train.start()

        
    def get_list_of_engines_to_move(self):
        global trains_allocated
        global trains_dispatched 
        
        #find what train we want to move
        #select only from available trains  %%%%todo%%%%%
        all_trains = self.get_all_roster_entries_with_speed_profile()
        #trains to choose from are the allocated - dispatched
        trains_to_choose = copy.copy(trains_allocated)
        if self.logLevel > 0: print "trains_dispatchedx", trains_dispatched
        if self.logLevel > 0: print "trains_allocated",trains_allocated
        if self.logLevel > 0: print "trains_to_choose",trains_to_choose
        if trains_dispatched != []:
            for train in trains_dispatched:
                if self.logLevel > 0: print "removing" ,train
                trains_to_choose.remove(train)
                if self.logLevel > 0: print "trains_to_choose",trains_to_choose
                
        # JOptionPane.showMessageDialog(None,msg)
        if trains_to_choose == []:
            str_trains_dispatched= (' '.join(trains_dispatched))
            msg = "There are no trains available for dispatch\nTrains dispatched are:\n"+str_trains_dispatched+"\nOK (yes) RESET (no)"
            title = ""
            result = JOptionPane.showConfirmDialog(None, msg, title, JOptionPane.YES_NO_OPTION)
            if result == JOptionPane.NO_OPTION:
                trains_dispatched = []                      
            #sensor_changed.setKnownState(INACTIVE)
        # else:
            # msg = "select train you want to move"
            # train_to_move = modifiableJComboBox(trains_to_choose,msg).return_val()
            # title = "choose train to move"
            # engine = OptionDialog().MultipleBox(title, list_items)
            # station_from =     #location of engine
        return trains_to_choose
        
    def get_position_of_train(self, train_to_move):
        ## Check the pressed button
        for station_block_name in g.station_block_list:
            if self.logLevel > 0: print "station_block_name", station_block_name
            
            #get a True if the block block_value has the train name in it
            block_value_state = self.check_train_in_block(station_block_name, train_to_move)
            if self.logLevel > 0: print "block_value_state= ",block_value_state
            
            #get a True if the block is occupied
            block_occupied_state = self.check_sensor_state_given_block_name(station_block_name)
            if self.logLevel > 0: print "block_occupied_state= ",block_occupied_state
            if self.logLevel > 0: print ("station block name {} : {}". format(station_block_name, str(block_occupied_state)))
            
            # # do not attempt to move to where you are
            # button_pressed_in_occupied_station = (button_station_name == station_block_name)
            
            #check if the block is occupied and has the required train in it  
            if block_value_state == True and block_occupied_state == True:
                # and button_pressed_in_occupied_station == False:
                return station_block_name
        return None
        
    def get_blockcontents(self, block_name):
        block = blocks.getBlock(block_name)
        value =  block.getValue()
        return value        
        
    def check_train_in_block(self, block_name, train_name):
        mem_val = self.get_blockcontents(block_name)
        if train_name == mem_val:
            return True
        else:
            return False

    def check_sensor_state_given_block_name(self, station_block_name):
        #if self.logLevel > 0: print("station block name {}".format(station_block_name))
        layoutBlock = layoutblocks.getLayoutBlock(station_block_name)
        station_sensor = layoutBlock.getOccupancySensor() 
        if station_sensor is None:
            OptionDialog().displayMessage(' Sensor in block {} not found'.format(station_block_name))
            return
        currentState = True if station_sensor.getKnownState() == ACTIVE else False
        return currentState              
            
    def get_all_roster_entries_with_speed_profile(self):
        roster_entries_with_speed_profile = []
        r = jmri.jmrit.roster.Roster.getDefault()
        for roster_entry in jmri.jmrit.roster.Roster.getAllEntries(r):
            if self.logLevel > 0: print "roster_entry.getSpeedProfile()",roster_entry,roster_entry.getSpeedProfile()
            if roster_entry.getSpeedProfile() != None:
                roster_entries_with_speed_profile.append(roster_entry.getId())
                if self.logLevel > 0: print "roster_entry.getId()",roster_entry.getId()
        return roster_entries_with_speed_profile        


          

class DispatchMaster(jmri.jmrit.automat.AbstractAutomaton):
    
    button_sensors_to_watch = []
    button_dict = {}
    
    def __init__(self):
        self.logLevel = 0
        global trains_dispatched
        trains_dispatched = []
        #initialise all block_value variables
        for block in blocks.getNamedBeanSet():
            LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
            if LayoutBlockManager.getLayoutBlock(block) != None:
                block.setValue(None)                                
    
    def init(self):
        if self.logLevel > 0: print 'Create DispatchMaster Thread'
        

    def setup(self):
        if self.logLevel > 0: print "starting DispatchMaster setup"

        #get dictionary of buttons self.button_dict
        self.get_buttons()
        #set all move_to buttons inactive
        for sensor in self.button_sensors:
            sensor.setKnownState(INACTIVE)
        #store the values in a clone
        #self.store_button_states()
        # #at moment there are no trains so:
        self.button_sensors_to_watch = copy.copy(self.button_sensors)

        if self.logLevel > 0: print "self.button_sensors_to_watch_init", [str(sensor.getUserName()) for sensor in self.button_sensors_to_watch]

        self.sensor_active = None
        if self.logLevel > 0: print "finished DispatchMaster setup"
        return True

    def handle(self):
    
        global trains_allocated
        global trains_dispatched   
    
        #only one button is active. We will keep it that way
        
        if self.logLevel > 0: print "**********************"
        if self.logLevel > 0: print "handle DispatchMaster1"
        if self.logLevel > 0: print "buttons to watch",[str(sensor.getUserName()) for sensor in self.button_sensors_to_watch]
        if self.logLevel > 0: print "**********************" 
        #wait for one to go active
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
        self.waitSensorState(button_sensors_to_watch_JavaList, ACTIVE)
        
        #determine the button
        if self.logLevel > 0: print "sensor went active"
        sensor_changed = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == ACTIVE][0]
        if self.logLevel > 0: print "sensor_changed",sensor_changed.getUserName()
        
        #find location of that want to move to
        button_sensor_name = sensor_changed.getUserName()
        button_station_name = self.get_block_name_from_button_sensor_name(button_sensor_name)
        if self.logLevel > 0: print "button_sensor_name",button_sensor_name
        if self.logLevel > 0: print "button_station_name",button_station_name
        
        #if SchedulerSensor2 button is pressed then set up route, otherwise attempt to dispatch train
        if self.logLevel > 0: print "!!!!!!!!!!!!!!!!!!!!!!!!"
        setup_dispatch_sensor = sensors.getSensor("setDispatchSensor") 
        set_route_sensor = sensors.getSensor("setRouteSensor")
        run_route_sensor = sensors.getSensor("runRouteSensor")
        if self.logLevel > 0: print "set_route_sensor.getKnownState()",set_route_sensor.getKnownState(), ACTIVE
        if set_route_sensor.getKnownState() == ACTIVE:
            if self.logLevel > 0: print ("set_route")
            test = self.set_route(sensor_changed, button_sensor_name, button_station_name)
            if self.logLevel > 0: print "test = " , test
            if test == False:
                self.button_sensors_to_watch = copy.copy(self.button_sensors)
                sensor_changed.setKnownState(INACTIVE)
        elif setup_dispatch_sensor.getKnownState() == ACTIVE:
            if self.logLevel > 0: print ("dispatch_train")
            self.dispatch_train(sensor_changed, button_sensor_name, button_station_name)
        #if run_route_sensor is active - do nothing from here
            
        if self.logLevel > 0: print "end handle"                    
        return True 
        
    def set_route(self, sensor_changed, button_sensor_name, button_station_name):
    
        msg = "selected station " + button_station_name + ". \nHave you more stations on route?" 
        title = "Continue selecting stations"
        
        opt1 = "Select another station"
        opt2 = "Cancel Route"
        
        s = OptionDialog().customQuestionMessage2(msg,title,opt1,opt2)
    
    
        # msg = "selected station " + button_station_name + "\nClick YES to proceed\nthen press the next station on the route.\nPress No or cancel if you don't want to create a route."
        # title = ""
        # s = JOptionPane.showConfirmDialog(None, msg, title, JOptionPane.YES_NO_CANCEL_OPTION)
        if s == JOptionPane.NO_OPTION:
            return False 
        if self.logLevel > 0: print "button_station_name", button_station_name
        if self.logLevel > 0: print "button_sensor_name", button_sensor_name
        #set name of route
        if self.logLevel > 0: print ("in dispatch train")
        # msg = "Name of Route"
        # route_name = JOptionPane.showInputDialog(None,msg)
        #create route
        RouteManager=jmri.InstanceManager.getDefault(jmri.jmrit.operations.routes.RouteManager)
        route = RouteManager.newRoute("temp_name")
        
        LocationManager=jmri.InstanceManager.getDefault(jmri.jmrit.operations.locations.LocationManager)
        #if self.logLevel > 0: print "button_station_name", button_station_name
        location = LocationManager.newLocation(button_station_name)
        first_station = button_station_name
        last_station = first_station
        route.addLocation(location)       
        self.button_sensors_to_watch = copy.copy(self.button_sensors)
        self.button_sensors_to_watch.remove(sensor_changed) 
        complete = False
        while complete == False:
            if self.logLevel > 0: print ("In loop")
            button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
            self.waitSensorState(button_sensors_to_watch_JavaList, ACTIVE)
            sensor_changed = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == ACTIVE][0]
            button_sensor_name = sensor_changed.getUserName()
            button_station_name = self.get_block_name_from_button_sensor_name(button_sensor_name)

            location = LocationManager.newLocation(button_station_name)
            route.addLocation(location)
            last_station = button_station_name
            
            msg = "selected station " + button_station_name + ". \nHave you more stations on route?" 
            title = "Continue selecting stations"
            
            opt1 = "Select another station"
            opt2 = "Complete Route"
            opt3 = "Cancel Route"
            
            s = OptionDialog().customQuestionMessage(msg,title,opt1,opt2,opt3)
            if s == JOptionPane.NO_OPTION:
                complete = True
            if s == JOptionPane.CANCEL_OPTION:
                sensor_changed.setKnownState(INACTIVE)
                RouteManager.deregister(route)
                return
            Firstloop = False
            self.get_buttons()
            self.button_sensors_to_watch = copy.copy(self.button_sensors)
            self.button_sensors_to_watch.remove(sensor_changed)
            
        route_name_prefix = first_station + "_to_" + last_station
        route_name = route_name_prefix
        i = 0
        while RouteManager.getRouteByName(route_name) != None:
            i+=1
            route_name = route_name_prefix + "_" + str(i)
        route.setName(route_name)            
        msg = "completed route  " + route_name + ". you may see the route by clicking View/Edit Routes."
        opt1 = "Finish"
        opt2 = "View Route"
        reply = OptionDialog().customQuestionMessage2(msg, title, opt1, opt2)
        sensor_changed.setKnownState(INACTIVE)
        if reply == JOptionPane.NO_OPTION:
            self.show_routes()
        if self.logLevel > 0: print ("terminated dispatch")
        return True
        
    def show_routes(self):
        a = jmri.jmrit.operations.routes.RoutesTableAction()
        a.actionPerformed(None)
        
    def dispatch_train(self, sensor_changed, button_sensor_name, button_station_name):
        global trains_allocated
        global trains_dispatched 
        
        #find what train we want to move
        #select only from available trains  %%%%todo%%%%%
        all_trains = self.get_all_roster_entries_with_speed_profile()
        #trains to choose from are the allocated - dispatched
        trains_to_choose = copy.copy(trains_allocated)
        if self.logLevel > 0: print "trains_dispatchedx", trains_dispatched
        if self.logLevel > 0: print "trains_allocated",trains_allocated
        if self.logLevel > 0: print "trains_to_choose",trains_to_choose
        if trains_dispatched != []:
            for train in trains_dispatched:
                if self.logLevel > 0: print "removing" ,train
                trains_to_choose.remove(train)
                if self.logLevel > 0: print "trains_to_choose",trains_to_choose
        # msg = "trains_to_choose" + str(trains_to_choose)
        # JOptionPane.showMessageDialog(None,msg)
        if trains_to_choose == []:
            str_trains_dispatched= (' '.join(trains_dispatched))
            msg = "There are no trains available for dispatch\nTrains dispatched are:\n"+str_trains_dispatched+"\nOK (yes) RESET (no)"
            title = ""
            result = JOptionPane.showConfirmDialog(None, msg, title, JOptionPane.YES_NO_OPTION)
            if result == JOptionPane.NO_OPTION:
                trains_dispatched = []                      
            sensor_changed.setKnownState(INACTIVE)
        else:
            msg = "select train you want to move"
            train_to_move = modifiableJComboBox(trains_to_choose,msg).return_val()
            
            print "+++++++++++++++++++"
            print "checking pressed button"
            print "+++++++++++++++++++"
            
            ## Check the pressed button
            for station_block_name in g.station_block_list:
                if self.logLevel > 0: print "station_block_name", station_block_name
                #get a True if the block block_value has the train name in it
                block_value_state = self.check_train_in_block(station_block_name, train_to_move)
                if self.logLevel > 0: print "block_value_state= ",block_value_state
                #get a True if the block is occupied
                block_occupied_state = self.check_sensor_state_given_block_name(station_block_name)
                if self.logLevel > 0: print "block_occupied_state= ",block_occupied_state
                if self.logLevel > 0: print ("station block name {} : {}". format(station_block_name, str(block_occupied_state)))
                # do not attempt to move to where you are
                button_pressed_in_occupied_station = (button_station_name == station_block_name)
                #check if the block is occupied and has the required train in it  
                if block_value_state == True and block_occupied_state == True and button_pressed_in_occupied_station == False:
                    #move from station_block_Name to button_name_station

                    express = self.get_express_flag()   # flag determining whether want to stop at all stations or not stop
                    
                    title = "will the train stop at all stations?"
                    msg = "select the train type:"
                    if express:
                        options = ["express", "stopping"]
                        default = "express"
                        result = OptionDialog().variable_combo_box(options, default, msg, title, JOptionPane.QUESTION_MESSAGE)
                    else:
                        options = ["stopping", "express"]
                        default = "stopping"
                        result = OptionDialog().variable_combo_box( options, default, msg, title, JOptionPane.QUESTION_MESSAGE)
                    if self.logLevel > 0: print "result = ",result    
                    if result == "express":
                        if self.logLevel > 0: print "moving express"                                          
                        if g == None:
                            if self.logLevel > 0: print "G IS NONE"
                        #graph = self.mark_occupied_blocks(g.g_express)
                        #self.move_between_stations(station_block_name, button_station_name, train_name, g.g_express)
                        move_train = MoveTrain(station_block_name, button_station_name, train_to_move, g.g_express)
                        instanceList.append(move_train)
                        if move_train.setup():
                            move_train.setName(train_to_move)
                            move_train.start()
                        if self.logLevel > 0: print "station_block_name",station_block_name
                        if self.logLevel > 0: print "button_station_name", button_station_name
                        #if self.logLevel > 0: print "button_block_name", button_block_name
                        if self.logLevel > 0: print "**********************"

                    elif express == False:
                        if self.logLevel > 0: print "moving slow"
                        #OptionDialog().displayMessage("a stopping train")
                        if g == None:
                            if self.logLevel > 0: print "G IS NONE"
                        move_train = MoveTrain(station_block_name, button_station_name, train_to_move, g.g_stopping)
                        instanceList.append(move_train)
                        if move_train.setup():
                            move_train.setName(train_to_move)
                            if self.logLevel > 0: print "********calling thread move**************"
                            move_train.start()
                            if self.logLevel > 0: print "********called thread move***************"
                        if self.logLevel > 0: print "station_block_name",station_block_name
                        if self.logLevel > 0: print "button_station_name", button_station_name
                        #if self.logLevel > 0: print "button_block_name", button_block_name
                        if self.logLevel > 0: print "**********************"                    
                        #self.move_between_stations(station_block_name, button_station_name, train_name, g.g_stopping)
                    else:
                        #express flag not set up
                        pass
                    break
            #set old button which activated the same train to inactive
            if self.button_dict != {}:
                if self.logLevel > 0: print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                if self.logLevel > 0: print "self.button_dict = ",self.button_dict
                if self.logLevel > 0: print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                if train_to_move in self.button_dict:
                    old_button_sensor = self.button_dict[train_to_move]
                    old_button_sensor.setKnownState(INACTIVE)
                    self.button_sensors_to_watch.append(old_button_sensor)
            #associate new button with train
            if self.logLevel > 0: print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            if self.logLevel > 0: print "train_to_move", train_to_move
            if self.logLevel > 0: print "sensor_changed", sensor_changed
            if self.logLevel > 0: print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            self.button_dict[train_to_move] = sensor_changed
            if self.logLevel > 0: print "self.button_dict = ",self.button_dict

            # #set other buttons to inactive
            # if self.sensor_active != None:
                # self.sensor_active.setKnownState(INACTIVE)
                # self.waitMsec(2000)
            #remember the active button
            # self.sensor_active = sensor_changed
            #get the list of sensors to watch
            #if self.logLevel > 0: print "self.button_sensors_to_watch_before_remove", [sensor.getUserName() for sensor in self.button_sensors_to_watch]
            self.button_sensors_to_watch.remove(sensor_changed)
        #if self.logLevel > 0: print "self.button_sensors_to_watch", [sensor.getUserName() for sensor in self.button_sensors_to_watch]
        
           

    def get_block_name_from_button_sensor_name(self, button_sensor_name):
        #button_sensor_name MoveToblock8_stored
        #block_name block8
        block_name = button_sensor_name.replace("MoveTo","").replace("_stored","").replace("_"," ")
        return block_name

    def get_button_sensor_given_block_name(self, block_name):
        button_sensor_name = "MoveTo"+block_name.replace(" ","_") +"_stored"
        button_sensor = sensors.getSensor(button_sensor_name)
        return button_sensor 

    def get_express_flag(self):
        self.express_sensor = sensors.getSensor("Express")
        if self.express_sensor is None:
            OptionDialog().displayMessage("No Express Sensor set up")
            return None
        express_state = self.express_sensor.getKnownState()
        if self.logLevel > 0: print express_state,jmri.Sensor.ACTIVE
        #msg = "express sensor is ", str(express_state)
        #OptionDialog().displayMessage(msg)
        if express_state == jmri.Sensor.ACTIVE:
            express_flag = True
        else:
            express_flag = False
        return express_flag
        
    def get_blockcontents(self, block_name):
        block = blocks.getBlock(block_name)
        value =  block.getValue()
        return value

    def check_train_in_block(self, block_name, train_name):
        mem_val = self.get_blockcontents(block_name)
        if train_name == mem_val:
            return True
        else:
            return False 

    def check_sensor_state_given_block_name(self, station_block_name):
        #if self.logLevel > 0: print("station block name {}".format(station_block_name))
        layoutBlock = layoutblocks.getLayoutBlock(station_block_name)
        station_sensor = layoutBlock.getOccupancySensor() 
        if station_sensor is None:
            OptionDialog().displayMessage(' Sensor in block {} not found'.format(station_block_name))
            return
        currentState = True if station_sensor.getKnownState() == ACTIVE else False
        return currentState    

    def get_all_roster_entries_with_speed_profile(self):
        roster_entries_with_speed_profile = []
        r = jmri.jmrit.roster.Roster.getDefault()
        for roster_entry in jmri.jmrit.roster.Roster.getAllEntries(r):
            if self.logLevel > 0: print "roster_entry.getSpeedProfile()",roster_entry,roster_entry.getSpeedProfile()
            if roster_entry.getSpeedProfile() != None:
                roster_entries_with_speed_profile.append(roster_entry.getId())
                if self.logLevel > 0: print "roster_entry.getId()",roster_entry.getId()
                if self.logLevel > 0: print "roster_entries_with_speed_profile",roster_entries_with_speed_profile
        return roster_entries_with_speed_profile      
 
    def get_buttons(self):    
        self.button_sensors = [self.get_button_sensor_given_block_name(station_block_name) for station_block_name in g.station_block_list]
        self.button_sensor_states = [self.check_sensor_state(button_sensor) for button_sensor in self.button_sensors]
        # for button_sensor in self.button_sensors:
            # self.button_dict[button_sensor] = self.check_sensor_state(button_sensor)
        
            
    def check_sensor_state(self, sensor):
        #if self.logLevel > 0: print("check_sensor_state",sensor)
        if sensor == None :
            #if self.logLevel > 0: print('Sensor in check_sensor_state is none')
            return None
        #sensor = sensors.getSensor(sensor_name)
        if sensor is None:
            OptionDialog().displayMessage('Sensor {} not found'.format( sensor_name))
            return
        currentState = True if sensor.getKnownState() == ACTIVE else False
        #if self.logLevel > 0: print("check_sensor_state {}".format(currentState))
        return currentState
       
    def store_button_states(self):
        self.button_sensor_states_old = self.button_sensor_states
        if self.logLevel > 0: print "self.button_sensor_states_old",self.button_sensor_states_old
        #self.button_dict_old = dict(self.button_dict)
        
    def get_button_sensor_given_block_name(self, block_name):
        button_sensor_name = "MoveTo"+block_name.replace(" ","_") +"_stored"
        button_sensor = sensors.getSensor(button_sensor_name)
        return button_sensor        
           
    def show_operations_trains(self):
        a = jmri.jmrit.operations.trains.TrainsTableAction()
        a.actionPerformed(None)
        
# End of class StopMaster




class RunDispatcherMaster():

    def __init__(self):
        global g
        global le
        my_path_to_jars = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/jars/jgrapht.jar')
        import sys
        sys.path.append(my_path_to_jars) # add the jar to your path
        CreateGraph = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/CreateGraph.py')
        exec(open (CreateGraph).read())
        #execfile(CreateGraph)
        le = LabelledEdge
        g = StationGraph()

        new_train_master = NewTrainMaster()
        instanceList.append(new_train_master)
        if new_train_master.setup():
            new_train_master.setName('New Train Master')
            new_train_master.start()  

        stop_master = StopMaster()
        if stop_master.setup():
            stop_master.setName('Stop Master')
            stop_master.start()

        reset_button_master = ResetButtonMaster()
        instanceList.append(reset_button_master)
        if reset_button_master.setup():
            pass
            reset_button_master.setName('Reset Button Master')
            reset_button_master.start()

        dispatch_master = DispatchMaster()
        instanceList.append(dispatch_master)
        if dispatch_master.setup():
            dispatch_master.setName('Dispatch Master')
            dispatch_master.start() 

        simulation_master = SimulationMaster()
        instanceList.append(simulation_master)
        if simulation_master.setup():
            simulation_master.setName('Simulation Master')
            simulation_master.start()             
                    
        scheduler_master = SchedulerMaster()
        instanceList.append(scheduler_master)
        if scheduler_master.setup():
            scheduler_master.setName('Scheduler Master')
            scheduler_master.start()
            
        off_action_master = OffActionMaster()
        instanceList.append(off_action_master)
        
        if off_action_master.setup():
            off_action_master.setName('Off-Action Master')
            off_action_master.start() 
        else:
            if self.logLevel > 0: print("Off-Action Master not started")
            
        #set default valus of buttons
        sensors.getSensor("Express").setKnownState(ACTIVE)
        sensors.getSensor("simulateSensor").setKnownState(INACTIVE)
            
            
if __name__ == '__builtin__':
    RunDispatcherMaster()
    # NewTrainMaster checksfor the new train in siding. Needs to inform what station we are in 
    #DispatchMaster checks all button sensors 

    
# if __name__ == "__main__":
    # if self.logLevel > 0: print "hi"            
    # logLevel = 4
    # #stopMasterSensor = "stopMasterSensor"
    # #newTrainSensor = "newTrainSensor"
    # instanceList = []   # List of file based instances 
    # trains = {}
    # g = StationGraph()
    # if self.logLevel > 0: print "hi"
