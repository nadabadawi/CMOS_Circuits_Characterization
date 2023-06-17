import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
import os
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('NAND3x2')
circuit.include("./data/sky130.sp")
circuit.V('vdd', 'vdd', 'gnd', '1.8v')

circuit.X('X1', 'sky130_fd_pr__pfet_01v8', 'Y ', 'A', 'vdd', 'vdd', W='2000000u', L='150000u')
circuit.X('X2', 'sky130_fd_pr__pfet_01v8', 'Y', 'B', 'vdd', 'vdd', W='2000000u', L='150000u')
circuit.X('X3', 'sky130_fd_pr__pfet_01v8', 'Y', 'C', 'vdd', 'vdd', W='2000000u', L='150000u')
circuit.X('X4', 'sky130_fd_pr__nfet_01v8', 'Y', 'A', 'n1', 'n1', W='3000000u', L='150000u')
circuit.X('X5', 'sky130_fd_pr__nfet_01v8', 'n1', 'B', 'n2', 'n2', W='3000000u', L='150000u')
circuit.X('X6', 'sky130_fd_pr__nfet_01v8', 'n2', 'B', 'gnd', 'gnd', W='3000000u', L='150000u')
circuit.PulseVoltageSource('vina', 'A', 'gnd', 0, 1.8, 0, 0, 0, 0, 0)
circuit.PulseVoltageSource('vinb', 'B', 'gnd', 0, 1.8, 0, 0, 0, 0, 0)
circuit.PulseVoltageSource('vinc', 'C', 'gnd', 0, 1.8, 0, 0, 0, 0, 0)
circuit.C('C1', 'Y', 'gnd', '1fF')

#Modify capacitor value
C1 = circuit['CC1']
V1 = circuit['Vvina']
V2 = circuit['Vvinb']
V3 = circuit['Vvinc']
V1.rise_time = 0.1@u_ns
V2.rise_time = 0.1@u_ns
V3.rise_time = 0.1@u_ns
V1.fall_time = 0.1@u_ns
V2.fall_time = 0.1@u_ns
V3.fall_time = 0.1@u_ns
V1.period = 24@u_ns
V2.period = 24@u_ns
V3.period = 24@u_ns
V1.pulse_width = 12@u_ns
V2.pulse_width = 12@u_ns
V3.pulse_width = 12@u_ns

C1.capacitance = 0.001@u_pF

capacitance = 0.001 # changes 8 times
ip_trans = 0 # changes 7 times
delay = "tpdf"
ctr = 1
tpdf = ""
tpdr = ""
lines_tpdr = ""
lines_tpdf = ""

if (delay == "tpdf"):
    V1.initial_value = 1.8@u_V
    V2.initial_value = 1.8@u_V
    V3.initial_value = 1.8@u_V
    V1.pulsed_value = 0@u_V
    V2.pulsed_value = 0@u_V
    V3.pulsed_value = 0@u_V
    
elif (delay == "tpdr"):
    V1.initial_value = 0@u_V
    V2.initial_value = 0@u_V
    V3.initial_value = 0@u_V
    V1.pulsed_value = 1.8@u_V
    V2.pulsed_value = 1.8@u_V
    V3.pulsed_value = 1.8@u_V

# file naming convention: SpiceFile_Cap_#_Trans_#_tpdr.sp

# V1.initial_value = 1.8@u_V
# V2.initial_value = 1.8@u_V
# V3.initial_value = 1.8@u_V
# V1.pulsed_value = 0@u_V
# V2.pulsed_value = 0@u_V
# V3.pulsed_value = 0@u_V

print("Circuit")
print(circuit)

results = open("Results_" + delay + ".csv", "w")
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
        V3.fall_time = ip_trans@u_ns
        V3.rise_time = ip_trans@u_ns
    for j in range(1, 9): # 1 to 8
        C1.capacitance = capacitance@u_pF
        capacitance+=0.002
        ctr+=2
        filename = str(ctr - 2) + "_Tran_" + str(ip_trans) + "_" + delay 
        f = open("SpiceFile_Cap"+ filename + ".sp", "w")
        f.write(str(circuit))
        f.write('''
        .tran 10ps 40ns  
        .control
            run     
            meas tran tpdr          
                + TRIG v(A) VAL=0.9 FALL=1         
                + TARG v(Y) VAL=0.9 RISE=1
            meas tran tpdf          
                + TRIG v(A) VAL=0.9 RISE=1         
                + TARG v(Y) VAL=0.9 FALL=1 
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
        results.write("%s, %s, %s\n" % (ctr - 2, ip_trans, tpd))


results.close()



