# SimplyPrint_Scan
Python Script that changes filament in simplyprint to match loaded filament by scanning bar and qr codes

I wanted a simpler way for my robotics students to change filaments in the SimplyPrint UI to match the physical printer.  I wrote this script to run on a dedicated pi near my printers that will just have a small screen and a barcode scanner.

My code skills are by no means on par with anyone, but I can usually make something work.  Im more than happy to hear of better ways to do things, so if you notice i did something in a dumb way let me know, it probably is there for a dumb reason.  I unfortunaly did not do squat for commenting, I will get to that when I have a bit more time.  

-A barcode/QRcode is stuck to the extruder.  The code is just the printer ID followed by the extruder ID seperated by a space. Example "12345 0" or "123455 1" indicates printer 12345 extruder 0 or 1 respectivly.

-The filament rolls have a code generated by SimplyPrint

-An additional "ABORT" or "DELETE" barcode is functional.  Scanning DELETE will allow the deletion of a roll of filament from the SimplyPrint Inventory (for when you throw one away).  Scanning ABORT will cancel the current operation of assigning or deleting.

- I will be adding a "UNASSIGN" barcode next to remove a roll from a printer without inserting a new one.
