Inside this directory there is a fileclient.py and fileserver.py. 

I implemented 'get' and 'put' operations on the server. 

To start the program with the stammer proxy:
  + Start stammer proxy listening on host:50000, forwarding to host:50001
  + Start the server, which listens on host:50001 by default
  + Start the client on host:50000
  
 To change the file that was being transferred I actually edited the code in the fileclient.
 Change the filename variable on fileclient line 60
 Change the action variable on fileclient line 61
 
 By default the client will 'put' a file 'soliers.txt'. Because I tested this all on the same machine, the server writes
 the file it gets as 'soldiers.txt-SERVER'.
 
 Similarly, if you do a get operation the client will write the file as 'soldiers.txt-CLIENT'.
 
 I included those two ascii art text files for testing, and to make it easy for you (the helpful TA) to grade.
 
 Both systems excessively log what they are doing.
 
 The server handles multiple clients, the client only does a single request though. 
