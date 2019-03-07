var folder_name = "C:/Users/My Pc/Desktop/20190305 - MCNC 0kjg 1mM/"
var file_name = "MCNC 0kjg 1mM - in dodacane 0.5wt% span80 - 7wt% - 001.jpg"
open(folder_name + file_name);
selectWindow(file_name);
run("RGB Stack");
run("Brightness/Contrast...");
