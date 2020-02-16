import DeepMinning as dm

px = "{http://autosar.org/schema/r4.0}"

def getTagIndex(toor, tag_name):
    for each_tag in range(len(toor)):
        if toor[each_tag].tag.find(tag_name) != -1:
            return toor[each_tag]
    return -1


class signal:
    def __init__(self, CompuMethod_TagList, Unit_TagList, ISignal_TagList, ISignalIPDU_TagList):
        self.name = None
        self.length = None
        self.description = None
        self.initial_value = None
        self.offset = None
        self.resolution = None
        self.range = []
        self.hex_range = []
        self.enums = [] #This will be a list of tuples, first of which will be the code and second the description
        self.enum_str = ""
        self.unit = None
        self.data_type = None
        self.parent = None
        self.start_position = None
        self.applicability = False
        self.CompuMethod_TagList = CompuMethod_TagList
        self.Unit_TagList = Unit_TagList
        self.ISignal_TagList = ISignal_TagList
        self.ISignalIPDU_TagList = ISignalIPDU_TagList


    def get_signal_param1(self, root):    #Gets Range(lower and upper limit), Offset and Resolution of the signal
        compus = 0
        lompus = 0

        for com in range(len(self.CompuMethod_TagList)):
            if dm.getUniqueDescendant(self.CompuMethod_TagList[com], px+"SHORT-NAME").text == self.name + "_CompuMethod":
                category = dm.getUniqueDescendant(self.CompuMethod_TagList[com], px+"CATEGORY").text
                COMPU_SCALES = dm.getUniqueDescendant(self.CompuMethod_TagList[com], px+"COMPU-SCALES")
                if category == "TEXTTABLE":
                    CompuScale_TagList = dm.digAllTags(COMPU_SCALES, px+"COMPU-SCALE")
                    for csc in range(len(CompuScale_TagList)):
                        shortLabelText = dm.getUniqueDescendant(CompuScale_TagList[csc], px+"SHORT-LABEL").text
                        lowerLimitText = dm.getUniqueDescendant(CompuScale_TagList[csc], px+"LOWER-LIMIT").text
                        self.enums.append((shortLabelText, lowerLimitText))

                elif category == "LINEAR":
                    COMPU_SCALE = dm.getUniqueDescendant(COMPU_SCALES, px+"COMPU-SCALE")
                    if COMPU_SCALE != -1:
                        LOWER_LIMIT = getTagIndex(COMPU_SCALE,"LOWER-LIMIT")
                        if LOWER_LIMIT != -1:
                            self.range.append(str(LOWER_LIMIT.text))
                        UPPER_LIMIT = getTagIndex(COMPU_SCALE, "UPPER-LIMIT")
                        if UPPER_LIMIT != -1:
                            self.range.append(str(UPPER_LIMIT.text))
                        COMPU_RATIONAL_COEFFS = getTagIndex(COMPU_SCALE, "COMPU-RATIONAL-COEFFS")
                        if COMPU_RATIONAL_COEFFS != -1:
                            COMPU_NUMERATOR = getTagIndex(COMPU_RATIONAL_COEFFS, "COMPU-NUMERATOR")
                            if COMPU_NUMERATOR != -1:
                                self.offset = COMPU_NUMERATOR[0].text
                                self.resolution = COMPU_NUMERATOR[1].text
                                lompus+=1
                    compus += 1

    def get_signal_unit(self, root):  #Gets the Unit of the signal
        for units in range(len(self.Unit_TagList)):
            if dm.getUniqueDescendant(self.Unit_TagList[units], px+"SHORT-NAME").text == self.name + "_Units":
                self.unit = dm.getUniqueDescendant(self.Unit_TagList[units], px+"DISPLAY-NAME").text
        if self.unit == None:
            self.unit = "N/A"

    def get_signal_datatype(self, root):  #Gets the data type of the signal
        for i in range(len(self.ISignal_TagList)):
            if dm.getUniqueDescendant(self.ISignal_TagList[i], px+"SHORT-NAME").text == self.name:
                BASE_TYPE_REF = dm.getUniqueDescendant(self.ISignal_TagList[i], px+"BASE-TYPE-REF")
                if BASE_TYPE_REF != -1:
                    if len(BASE_TYPE_REF.text) > 0:
                        self.data_type = str(BASE_TYPE_REF.text).split('/')[-1]

    def get_start_position_and_mapping(self, root):
        """
        Gets the start position(eg. starts at the 4th bit) of the signal within a PDU and determines which PDU the signal belongs to.
        :return:
        """

        for i in range(len(self.ISignalIPDU_TagList)):
            parent_name = dm.getUniqueChild(self.ISignalIPDU_TagList[i], px + "SHORT-NAME").text
            I_SIGNAL_TO_PDU_MAPPINGS = dm.getUniqueDescendant(self.ISignalIPDU_TagList[i], px + "I-SIGNAL-TO-PDU-MAPPINGS")
            for j in range(len(I_SIGNAL_TO_PDU_MAPPINGS)):
                signal_name = dm.getUniqueDescendant(I_SIGNAL_TO_PDU_MAPPINGS[j], px + "I-SIGNAL-REF")
                if signal_name != -1:
                    if signal_name.text.split('/')[-1] == self.name:

                        START_POSITION = dm.getUniqueDescendant(I_SIGNAL_TO_PDU_MAPPINGS[j], px + "START-POSITION")
                        if START_POSITION != -1:
                            self.start_position = START_POSITION.text
                            self.parent = parent_name

    def convert_enums_to_string(self, root):
        for i in range(len(self.enums)):
            self.enum_str += str(self.enums[i][0]) + ": " + str(self.enums[i][1]) + "\n"

    def get_signal_info(self):
        print("Name: ")
        print(self.name)
        print("Length: ")
        print(self.length)
        print("Description: ")
        print(self.description)
        print("Initial Value: ")
        print(self.initial_value)
        print("Offset: ")
        print(self.offset)
        print("Resolution: ")
        print(self.resolution)
        print("Range: ")
        print(self.range)
        print("Unit: ")
        print(self.unit)
        print("Data Type: ")
        print(self.data_type)
        print("Parent: ")
        print(self.parent)
        print("Start Position: ")
        print(self.start_position)
        print("\n\n")

class message:
    def __init__(self, name, PDU_name, CANFrame_TagList, FrameTriggering_TagList, ISignalIPDU_TagList):
        self.name = name
        self.PDU_name = PDU_name
        self.length = None
        self.ID = 0
        self.IDH = -1
        self.minimum_delay = None
        self.period = None
        self.repetitions = None
        self.signals = []
        self.type = None
        self.direction = None
        self.draft = None
        self.common = False
        self.CANFrame_TagList = CANFrame_TagList
        self.FrameTriggering_TagList = FrameTriggering_TagList
        self.ISignalIPDU_TagList = ISignalIPDU_TagList

    def getIdentifier(self, root):
        for i in range(len(self.FrameTriggering_TagList)):
            if dm.getUniqueChild(self.FrameTriggering_TagList[i], px+"FRAME-REF").text.split('/')[-1] == self.name:
                self.ID = dm.getUniqueChild(self.FrameTriggering_TagList[i], px+"IDENTIFIER").text
                return self.ID
        return -1

    def getTriggers(self, root):
        for i in range(len(self.ISignalIPDU_TagList)):
            if self.PDU_name == dm.getUniqueChild(self.ISignalIPDU_TagList[i], px+"SHORT-NAME").text:
                TRANSMISSION_MODE_TRUE_TIMING = dm.getUniqueDescendant(self.ISignalIPDU_TagList[i], px+"TRANSMISSION-MODE-TRUE-TIMING")
                min_del = dm.getUniqueDescendant(self.ISignalIPDU_TagList[i], px+"MINIMUM-DELAY")
                if min_del != -1:
                    self.minimum_delay = min_del.text
                if TRANSMISSION_MODE_TRUE_TIMING != -1:
                    CYCLIC_TIMING = getTagIndex(TRANSMISSION_MODE_TRUE_TIMING, "CYCLIC-TIMING")
                    if CYCLIC_TIMING != -1:
                        TIME_PERIOD = getTagIndex(CYCLIC_TIMING, "TIME-PERIOD")
                        self.period = TIME_PERIOD[0].text

                    EVENT_CONTROLLED_TIMING = getTagIndex(TRANSMISSION_MODE_TRUE_TIMING, "EVENT-CONTROLLED-TIMING")
                    if EVENT_CONTROLLED_TIMING != -1:
                        NUMBER_OF_REPETITIONS = getTagIndex(EVENT_CONTROLLED_TIMING, "NUMBER-OF-REPETITIONS")
                        self.repetitions = NUMBER_OF_REPETITIONS.text

    def getType(self, root):
        if self.repetitions != None and self.period == None:
            self.type = "Event_Controlled"
        elif self.repetitions == None and self.period != None:
            self.type = "Fixed_Periodic"
        elif self.repetitions != None and self.period != None:
            self.type = "Event_Periodic"
        else:
            pass

    def getDirection(self, root):
        ECU_COMM_PORT_INSTANCES = dm.getUniqueDescendant(root, px+"ECU-COMM-PORT-INSTANCES")
        for f_ports in range(len(ECU_COMM_PORT_INSTANCES)):
            if ECU_COMM_PORT_INSTANCES[f_ports].tag == px+"FRAME-PORT":
                if ECU_COMM_PORT_INSTANCES[f_ports][0].text.find(self.name) != -1:
                    self.direction = getTagIndex(ECU_COMM_PORT_INSTANCES[f_ports], "COMMUNICATION-DIRECTION").text

    def sort_signals_by_start_bit(self, root):
        for i in range(len(self.signals)):
            for j in range(len(self.signals) - 1):
                if int(self.signals[j].start_position) > int(self.signals[j+1].start_position):
                    self.signals[j], self.signals[j+1] = self.signals[j+1], self.signals[j]

    def calc_length(self, root):
        total_length = 0
        for sgn in self.signals:
            total_length += int(sgn.length)
        self.length = str(int((total_length + (total_length % 8))/8))

    def getLength(self, root):
        for msg in range(len(self.CANFrame_TagList)):
            if dm.getUniqueChild(self.CANFrame_TagList[msg], px+"SHORT-NAME").text == self.name:
                FRAME_LENGTH = dm.getUniqueChild(self.CANFrame_TagList[msg], px+"FRAME-LENGTH")
                if FRAME_LENGTH != -1:
                    self.length = FRAME_LENGTH.text

def read_messages(root):
    Messages = []
    CANFrame_TagList = dm.digAllTags(root, px+"CAN-FRAME")
    FrameTriggering_TagList = dm.digAllTags(root, px + "CAN-FRAME-TRIGGERING")
    ISignalIPDU_TagList = dm.digAllTags(root, px + "I-SIGNAL-I-PDU")

    for i in range(len(CANFrame_TagList)):
        PDU_TO_FRAME_MAPPING = dm.getUniqueDescendant(CANFrame_TagList[i], px+"PDU-TO-FRAME-MAPPING")
        PDU_name = dm.getUniqueChild(PDU_TO_FRAME_MAPPING, px + "PDU-REF").text.split('/')[-1]
        Frame_name = dm.getUniqueChild(CANFrame_TagList[i], px+"SHORT-NAME").text
        new_msg = message(Frame_name, PDU_name, CANFrame_TagList, FrameTriggering_TagList, ISignalIPDU_TagList)
        new_msg.getIdentifier(root)
        Messages.append(new_msg)
    return Messages

def read_signals(root):
    signals = []
    CompuMethod_TagList = dm.digAllTags(root, px + "COMPU-METHOD")
    Unit_TagList = dm.digAllTags(root, px + "UNIT")
    ISignal_TagList = dm.digAllTags(root, px + "I-SIGNAL")
    ISignalIPDU_TagList = dm.digAllTags(root, px + "I-SIGNAL-I-PDU")
    
    for sgn in range(len(ISignal_TagList)):
        temp_signal = signal(CompuMethod_TagList, Unit_TagList, ISignal_TagList, ISignalIPDU_TagList)
        temp_signal.name = dm.getUniqueChild(ISignal_TagList[sgn], px+"SHORT-NAME").text
        description = dm.getUniqueChild(ISignal_TagList[sgn], px+"DESC")
        if description != -1:
            temp_signal.description = description[0].text
        length = dm.getUniqueChild(ISignal_TagList[sgn], px+"LENGTH")
        if length != -1:
            temp_signal.length = length.text
        signals.append(temp_signal)
    return signals

def map_messages_to_signals(Messages, Signals):
    print(len(Signals))
    count = 0
    atleast_one_signal = False
    for msg in range(len(Messages)):
        for sgn in range(len(Signals)):
            if Messages[msg].PDU_name == Signals[sgn].parent:
                if atleast_one_signal == False:
                    atleast_one_signal = True
                Messages[msg].signals.append(Signals[sgn])
        if atleast_one_signal == True:
            count = count + 1
    print("count = " + str(count) + "/" + str(len(Messages)))
    return Messages

