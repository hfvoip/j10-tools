import re
import sys
import time
import typing
import warnings
import struct
 

if __name__ == '__main__':
   infile = "dmic0417_1.log";
   outfile = "dmic0417_1.raw";
   #头 n 个字节可能有帧结构混乱（因为rtt buffer overwrite)
   skip_headerbytes = 0;
   f = open(infile,"rb");
   f2 = open(outfile,"wb")
  
   wrong_datastart = 0;
   loop_read = 0;
   while True:
       line = f.read(1000)
       tmp_len = len(line);
       bad_dataflag = 0;
       for j in range(0,tmp_len):
           if (line[j] ==0x9):
               bad_dataflag = 1;
               wrong_datastart = loop_read*1000+j;
               break;
       loop_read =loop_read+1;
       if (tmp_len <1000):
           break
   f.close()
   skip_headerbytes = wrong_datastart +1000; 
   print ('skip bytes:'+str(skip_headerbytes))
   f = open(infile,"rb");
   
   unit_size = 96*2;
   chs = 1;
   sample_len = unit_size*chs*2+1 ;

   #所有input,output数据是以1作为分割的
   f.read(skip_headerbytes)
   contents = f.read(1000)
   total_len = (len(contents))
   for i in  range(0,total_len):
       if (contents[i] == 1):
           print('i='+ str(i))
           contents = contents[i+1:]
           break
   #print('total len='+str(total_len))
   f.close()
  
  
    
     
   start_time = time.time()
   f = open(infile,"rb");
   f.read(skip_headerbytes);
   f.read(i+1);
   frame_index = 0;
   some_bytes = bytearray();
   total_packets = 0
   while True:
       frame_index = frame_index +1;
       if (frame_index % 1000 ==0):
           print('frame = '+str(frame_index)+", writing...")
           immutable_bytes = bytes(some_bytes)
           f2.write(immutable_bytes) 
           some_bytes = bytearray()
           
       #line = contents[0:sample_len]
       line = f.read(sample_len)
       #print(line[sample_len-1])
       #print (line)
       tmp_len = len(line);
       total_packets = total_packets+1;
      
           
     
      
       if (tmp_len<sample_len):
           print('break')
           break
       
       
       #if (line[tmp_len-1] !=0x01):
       if (line[tmp_len-1] >0x0f):
           print(line)
           print('break43,tmp_len='+str(tmp_len))
           print(line[sample_len-1])
           break
       
            
       arr_newline =[]
       
       #print (line[0:4]) 
       for j in range(0,unit_size):
           a1 = line[j*2+0] -0xa0;
           a2 = line[j*2+1] -0x80;
           a3 = 0+ a1* 16 +a2;
           #print(a1,a2,a3)
           a3 = a3 &0xff
           #tmp = struct.pack('B',a3)
           #f2.write(tmp)
           
           some_bytes.append(a3)
           arr_newline.append( a3)
           
           
       #print((arr_newline))
       #print(some_bytes)
     
   immutable_bytes = bytes(some_bytes)
   f2.write(immutable_bytes)  
 
   f2.close()
   f.close()
   end_time  =time.time()
   print('Running time: %s Seconds'%(end_time-start_time))
   print('total packets:'+str(total_packets))