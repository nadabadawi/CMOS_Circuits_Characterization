import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
import os
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('NOR 2x2')
circuit.include("./data/sky130.sp")
circuit.V('vdd', 'vdd', 'gnd', '1.8v')

circuit.X('X1', 'sky130_fd_pr__pfet_01v8', 'n1', 'a', 'vdd', 'vdd', W='4000000u', L='150000u')
circuit.X('X2', 'sky130_fd_pr__pfet_01v8', 'c', 'b', 'n1', 'vdd', W='4000000u', L='150000u')
circuit.X('X3', 'sky130_fd_pr__nfet_01v8', 'c', 'a', 'gnd', 'gnd', W='840000u', L='150000u')
circuit.X('X4', 'sky130_fd_pr__nfet_01v8', 'c', 'b', 'gnd', 'gnd', W='840000u', L='150000u')
circuit.PulseVoltageSource('vina', 'a', 'gnd', 0, 1.8, 0, 0, 0, 0, 0)
circuit.PulseVoltageSource('vinb', 'b', 'gnd', 0, 1.8, 0, 0, 0, 0, 0)
circuit.C('C1', 'c', 'gnd', '1fF')

#Modify capacitor value
C1 = circuit['CC1']
V1 = circuit['Vvina']
V2 = circuit['Vvinb']
V1.rise_time = 0.1@u_ns
V2.rise_time = 0.1@u_ns
V1.fall_time = 0.1@u_ns
V2.fall_time = 0.1@u_ns
V1.period = 100@u_ns
V2.period = 100@u_ns
V1.pulse_width = 20@u_ns
V2.pulse_width = 20@u_ns

C1.capacitance = 0.001@u_pF




capacitance = 0.001 # changes 8 times
ip_trans = 0 # changes 7 times
delay = "tpdf"
ctr = 1
tpdf = ""
tpdr = ""
lines_tpdr = ""
lines_tpdf = ""

if (delay == "tpdr"):
    V1.initial_value = 1.8@u_V
    V2.initial_value = 1.8@u_V
    V1.pulsed_value = 0@u_V
    V2.pulsed_value = 0@u_V
    
elif (delay == "tpdf"):
    V1.initial_value = 0@u_V
    V2.initial_value = 0@u_V
    V1.pulsed_value = 1.8@u_V
    V2.pulsed_value = 1.8@u_V

# file naming convention: SpiceFile_Cap_#_Trans_#_tpdr.sp

print("Circuit")
print(circuit)

results = open("Results_nor_2x2_tpdf.csv", "w")
results.write("Capacitance, Input Transition Time, Rise Delay, Fall Delay\n")

# write a for loop
for i in range(1, 8): # 1 to 7
    ctr = 1
    capacitance = 0.001
    if i != 1:
        ip_trans+=0.25
        V1.rise_time = ip_trans@u_ns
        V2.rise_time = ip_trans@u_ns
        V1.fall_time = ip_trans@u_ns
        V2.fall_time = ip_trans@u_ns
    for j in range(1, 9): # 1 to 8
        C1.capacitance = capacitance@u_pF
        capacitance+=0.002
        ctr+=2
        filename = str(ctr - 2) + "_Tran_" + str(ip_trans) + "_" + delay 
        f = open("SpiceFile_Cap"+ filename + ".sp", "w")
        f.write(str(circuit))
        f.write('''
        .tran 10ps 100ns
        .control
            run     
            meas tran tpdr          
                + TRIG v(a) VAL=0.9 FALL=1         
                + TARG v(c) VAL=0.9 RISE=1     
            meas tran tpdf          
                + TRIG v(a) VAL=0.9 RISE=1         
                + TARG v(c) VAL=0.9 FALL=1 
            set wr_singlescale
            wrdata Values_Cap%s.txt %s
            exit
        .endc ''' % (filename, delay))
        f.close()
        os.system("ngspice SpiceFile_Cap" + filename + ".sp")
        print(filename)
        file = open("Values_Cap" + filename + ".txt", "r")
        lines = file.readlines()
        tpd = lines[1].split()[1]
        file.close()
        results.write("%s, %s, %s\n" % (ctr, ip_trans, tpd))


results.close()