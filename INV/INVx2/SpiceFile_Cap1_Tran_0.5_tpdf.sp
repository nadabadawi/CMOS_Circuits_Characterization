.title INVx4
.include /home/nadabadawi/Desktop/Sp23/DDII/Project/data/sky130.sp
Vvdd vdd gnd 1.8v
XX1 Y A vdd vdd sky130_fd_pr__pfet_01v8 L=150000u W=2000000u
XX4 Y B gnd gnd sky130_fd_pr__nfet_01v8 L=150000u W=840000u
Vvina A gnd DC 0V PULSE(0V 1.8V 0s 0.5ns 0.5ns 12ns 24ns)
Vvinb B gnd DC 0V PULSE(0V 1.8V 0s 0.5ns 0.5ns 12ns 24ns)
CC1 Y gnd 0.001pF

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
            wrdata Values_Cap1_Tran_0.5_tpdf.txt tpdf
            exit
        .endc 