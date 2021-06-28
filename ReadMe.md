# OPTIONS
 - 1: create the whole thing from scratch in C. Just copy what you need from arp-scan and do the whole thing as
      a C program, then all you would need is a compiler and you could literally run it on any system (fuck windows)
 - 2: Keep what we are doing and lave the user in charge of doing the arp-scan install (lame)
 - 3: Download the C code, and build as needed. What would that take? Is there a way to compile C code using python,
      natively?


## Lets do this incrementally...
 - Start out with 2, since that is the easiest
 - Combine 1 and 3, and use the arp-scan code on github for now then create a modified one in the future to substitute
 - Eventually could have a standalone c version (down the road)


## TODO
 - We had an issue where the .zshrc file wouldn't get updated, fix that 
 - We should change the format of the config file. An entry should be a 'machine' to look for. Specify attributes such as
   description 'hitlist', MAC address, etc.... then the files/patterns that you want to update.
