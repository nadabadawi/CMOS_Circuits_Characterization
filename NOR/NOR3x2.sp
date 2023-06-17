.include ./data/sky130.sp
*For NOR2x2 --> 2 inputs, size 2 // size of each pmos cell will be 4kp, while size of nmos cell will be 2
*Instance of the cmos/pmos (source gate drain source sky130_fd_pr__esd_nfet_01v8__tt W=// L=//  )
* d g s b
*b pmos vdd
*b nmos gnd
X1 n1 a vdd vdd sky130_fd_pr__pfet_01v8 W=7000000u L=150000u
X2 n2 b n1 n1 sky130_fd_pr__pfet_01v8 W=7000000u L=150000u
X3 d c n2 n2 sky130_fd_pr__pfet_01v8 W=7000000u L=150000u

X4 d a gnd gnd sky130_fd_pr__nfet_01v8 W=840000u L=150000u
X5 d b gnd gnd sky130_fd_pr__nfet_01v8 W=840000u L=150000u
X6 d c gnd gnd sky130_fd_pr__nfet_01v8 W=840000u L=150000u


*v(a)=0, v(b)=0, v(c)=0, v(d)= 1 correct
*v(a)=1, v(b)=0, v(c)=0, v(d)= 0 correct
*v(a)=0, v(b)=1, v(c)=0, v(d)= 0 correct
*v(a)=1, v(b)=1, v(c)=0, v(d)= 0 correct
*v(a)=0, v(b)=0, v(c)=1, v(d)= 0 correct
*v(a)=1, v(b)=0, v(c)=1, v(d)= 0 correct
*v(a)=0, v(b)=1, v(c)=1, v(d)= 0 correct
*v(a)=1, v(b)=1, v(c)=1, v(d)= 0 correct

vdd vdd gnd 1.8v
vina a gnd PULSE 0 1.8 0ps 0ps 0ps 10ns 100ns 
vinb b gnd PULSE 0 1.8 0ps 0ps 0ps 10ns 100ns
vinc c gnd PULSE 0 1.8 0ps 0ps 0ps 10ns 100ns

CL1 d gnd 5ff


.tran 10ps 100ns
.control
 run
 set color0=white
 set color1=black
 set xbrushwidth=2
 plot v(a), v(b), v(c),v(d)
 meas tran tpdr 
 + TRIG v(a) VAL=0.9 FALL=1
 + TARG v(d) VAL=0.9 RISE=1
 meas tran tpdf 
 + TRIG v(a) VAL=0.9 RISE=1
 + TARG v(d) VAL=0.9 FALL=1
.endc
