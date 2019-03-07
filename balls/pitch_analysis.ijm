
var folder_name = "C:/Users/My Pc/Desktop/20190305 - MCNC 0kjg 1mM/"
var file_name = "MCNC 0kjg 1mM - in dodacane 0.5wt% span80 - 7wt% -20x -080"
open(folder_name + file_name + ".jpg");
selectWindow(file_name + ".jpg");
run("RGB Stack");
setSlice(2);
run("Brightness/Contrast...");


while (!isKeyDown("space")) {
    wait(10);
}
run("Normalize Local Contrast");
// run("Normalize Local Contrast", "block_radius_x=20 block_radius_y=20 standard_deviations=2 center stretch stack");
