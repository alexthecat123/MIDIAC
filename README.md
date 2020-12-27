# MIDIAC
A device that plays MIDI files on floppy drives, hard drives, scanners, and dot matrix printers.

The MIDIAC ("MIDI" because it plays MIDI files and "AC" to make it sound like ENIAC, UNIVAC, and other computers from the 1940s and 50s) is a device that plays MIDI files on scanners, floppy drives, hard drives, and dot matrix print heads. The project was inspired by the Floppotron by SFSDFSDGSGSDG (LINKKKKKK) and I attempted something similar a few years ago with Scott Means (LINKKKKKKK), but that project was never completed. A few months ago, I decided to start from scratch and here's the result. The functionality of the MIDIAC is actually very simple in theory. The device works by pulsing the stepper motors (in the case of the floppy drives and scanners) and the pins of a dot matrix print head (in the case of the dot matrix printers) at the same frequency as the musical note that it intends to play. The hard drives are used for percussion since they make a loud click noise when you apply power to the voice coils that move the heads. At the moment, the system has two scanners, two stacks of six floppies each, and two hard drives (one for low drums and one for high drums), so it has four voice polyphony plus drums. It supports dot matrix printers as well, but this functionality is currently disabled since I accidentally blew the transistors that were driving the printer and I'm waiting for more to come in the mail. Each of these individual intruments is called a sound module and is controlled by an Arduino. At the heart of the system is a Python program that processes the desired MIDI file and sends messages over serial from the appropriate MIDI channels to the corresponding sound module Arduino. Each type of sound module is running different code that allows it to interface with its specific type of hardware (floppy, scanner, hard drive, or printer). The Arduinos in the floppy sound modules connect directly to the direction, step, and enable pins on the floppy drives, the hard drives are controlled using an L293D chip, the scanners are controlled using A4988 stepper drivers, and the dot matrix print head is controlled using TIP120 transistors. The sound modules also support pitch bend messages and different velocities, allowing them to reproduce a more accurate rendition of the original MIDI file.
# Files/Folders:
  - The **arranged** folder contains 
  - The **dotMatrixModule** folder contains 
  - The **floppyModule** folder contains 
  - The **hardDriveModule** folder contains 
  - The **percussionModule** folder contains 
  - The **scannerModule** folder contains 
  - The **songs** folder contains 
  - **midiac.py** is the main Python program that parses the MIDI file and sends note commands over serial to the sound modules.
  
# To Do:
- ALLOW THE USE OF VARIABLES AS OFFSETS (LDA WITH THE ADDRESS X UNITS AWAY FROM OFFSET Y)
- MAKE CLOCK SPEEDS MORE ACCURATE
- ASSEMBLER DOESN'T TAKE * = INTO ACCOUNT WHEN FINDING LABEL ADDRESSES
- SPEED UP ARDUINO SERIAL
- ALLOW THE INPUT OF ONLY ONE DATA ARGUMENT
- A CMP INSTRUCTION WOULD BE NICE
