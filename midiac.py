import mido
import serial
import time
import sys
import datetime
import signal

mid = mido.MidiFile('e1m1.mid') #the input MIDI file


print(mid.tracks) #print out the track names in the file

# TO DO: DISABLE STEPPER DRIVER WHEN NOT PLAYING A NOTE TO REDUCE MOTOR STRESS AND HEATING



floppy1 = serial.Serial('/dev/cu.usbserial-144330', baudrate = 115200, timeout = 0.007)
floppy2 = serial.Serial('/dev/cu.usbserial-144340', baudrate = 115200, timeout = 0.007)
scanners = serial.Serial('/dev/cu.usbserial-144310', baudrate = 115200, timeout = 0.007)
percussion1 = serial.Serial('/dev/cu.usbserial-144320', baudrate = 115200, timeout = 0.007) #open the serial connections to the Arduinos
time.sleep(4) #wait for the sound modules to reset
currentlyPlaying = []
currentlyPlaying1 = []
currentlyPlaying2 = []
currentlyPlaying3 = []
currentlyPlaying4 = []
currentlyPlaying5 = []
currentlyPlaying6 = [] #lists to hold the currrently playing notes for each sound module


def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart)) #function that maps a value to a certain range

#floppyModule controls a stack of floppy drives
#printerModule plays music on the carriage motor of a printer (adjust the maxSteps to account for different printers). THIS TENDS TO SOUND AWFUL
#percussionModule plays percussion on hard drives connected through a L293D and differentiates between high and low drum notes
#hardDriveModule plays music on the heads of hard drives and supports multiple independent drives, thus requiring commands to be sent with a drive number at the end (adjust the velocity to clickDelay mapping if the drives are clicking instead of playing notes) THIS ALSO SOUNDS PRETTY BAD
#dotMatrixModule plays music on a dot matrix print head and supports multiple indepenedent pins, thus requiring commands to be sent with a drive number at the end

#e1m1 is 2 on both floppies and 0 and 1 on the scanners
#sail is 0, 0, 0, 4, 11, 14, 9
#believer is 8 on both floppies, 2 and 6 on the dot matrix, and 3 on the scanner
#sandstorm is 4 and 11 on floppies, 6 and 7 on the dot matrix, and 5 on the scanner
#candionEdited2 is 1 and 2 on the floppies and 0 and 3 on the scanners
#bloxonius is 3 on both floppies and 1 and 2 on the scanners

#CHANGE THE VALUE OF X IN THE "if msg.channel == x:" STATEMENTS TO CHANGE THE MIDI CHANNEL THAT EACH SOUND MODULE PLAYS


try:
    for msg in mid.play(): #play the MIDI file
        print(msg)

        if msg.channel == 2: #if the note is intended for the first stack of floppies
            if msg.type == 'pitchwheel':
                floppy1.write(bytes(str('999') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "\n", 'utf8')) #if we get a pitch bend message, send the number 999 to signify to the sound module that we want to bend the pitch followed by how much we want to bend it
            if msg.type == 'note_on':
                if msg.velocity != 0 and not msg.note in currentlyPlaying:
                    currentlyPlaying.append(msg.note)
                    currentlyPlaying.append(msg.velocity) #append the note that we're turning on to currentlyPlaying
                floppy1.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "\n", 'utf8')) #if we get a note_on, send it to the arduino for this sound module
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying):
                    if value == msg.note:
                        currentlyPlaying.remove(value)
                        currentlyPlaying.pop(index) #look for the note we're turning off in currentlyPlaying and remove it from the list
                floppy1.write(bytes(str(msg.note) + "000" + "\n", 'utf8')) #if we get a note_off, send a velocity of zero to the arduino for this sound module to turn the note off
                if len(currentlyPlaying) > 0:
                    floppy1.write(bytes(str(currentlyPlaying[0]) + str(currentlyPlaying[1]).zfill(3) + "\n", 'utf8')) #if another note is still playing after turning the current one off, tell the sound module to resume playing it

        if msg.channel == 2: #if the note is intended for the second stack of floppies
            if msg.type == 'pitchwheel':
                floppy2.write(bytes(str('999') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "\n", 'utf8')) #if we get a pitch bend message, send the number 999 to signify to the sound module that we want to bend the pitch followed by how much we want to bend it
            if msg.type == 'note_on':
                if msg.velocity != 0 and not msg.note in currentlyPlaying1:
                    currentlyPlaying1.append(msg.note)
                    currentlyPlaying1.append(msg.velocity) #append the note that we're turning on to currentlyPlaying
                floppy2.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "\n", 'utf8')) #if we get a note_on, send it to the arduino for this sound module
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying1):
                    if value == msg.note:
                        currentlyPlaying1.remove(value)
                        currentlyPlaying1.pop(index) #look for the note we're turning off in currentlyPlaying and remove it from the list
                floppy2.write(bytes(str(msg.note) + "000" + "\n", 'utf8')) #if we get a note_off, send a velocity of zero to the arduino for this sound module to turn the note off
                if len(currentlyPlaying1) > 0:
                    floppy2.write(bytes(str(currentlyPlaying1[0]) + str(currentlyPlaying1[1]).zfill(3) + "\n", 'utf8')) #if another note is still playing after turning the current one off, tell the sound module to resume playing it


        if msg.channel == 0: #if the note is intended for the first scanner
              if msg.type == 'pitchwheel':
                  scanners.write(bytes(str('999') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "0" + "\n", 'utf8')) #if we get a pitch bend message, send the number 999 to signify to the sound module that we want to bend the pitch followed by how much we want to bend it
              if msg.type == 'note_on':
                  if msg.velocity != 0 and not msg.note in currentlyPlaying2:
                      currentlyPlaying2.append(msg.note)
                      currentlyPlaying2.append(msg.velocity) #append the note that we're turning on to currentlyPlaying
                  scanners.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "0" + "\n", 'utf8')) #if we get a note_on, write it to the arduino for the scanners
              if msg.type == 'note_off':
                  for index, value in enumerate(currentlyPlaying2):
                      if value == msg.note:
                          currentlyPlaying2.remove(value)
                          currentlyPlaying2.pop(index) #look for the note we're turning off in currentlyPlaying and remove it from the list
                  scanners.write(bytes(str(msg.note) + "000" + "0" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                  if len(currentlyPlaying2) > 0:
                      scanners.write(bytes(str(currentlyPlaying2[0]) + str(currentlyPlaying2[1]).zfill(3) + "0" + "\n", 'utf8')) #if another note is still playing after turning the current one off, tell the sound module to resume playing it

        if msg.channel == 1: #if the note is intended for the second scanner
              if msg.type == 'pitchwheel':
                  scanners.write(bytes(str('999') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "1" + "\n", 'utf8')) #if we get a pitch bend message, send the number 999 to signify to the sound module that we want to bend the pitch followed by how much we want to bend it
              if msg.type == 'note_on':
                  if msg.velocity != 0 and not msg.note in currentlyPlaying3:
                      currentlyPlaying3.append(msg.note)
                      currentlyPlaying3.append(msg.velocity) #append the note that we're turning on to currentlyPlaying
                  scanners.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "1" + "\n", 'utf8')) #if we get a note_on, write it to the arduino for the scanners
              if msg.type == 'note_off':
                  for index, value in enumerate(currentlyPlaying3):
                      if value == msg.note:
                          currentlyPlaying3.remove(value)
                          currentlyPlaying3.pop(index) #look for the note we're turning off in currentlyPlaying and remove it from the list
                  scanners.write(bytes(str(msg.note) + "000" + "1" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                  if len(currentlyPlaying3) > 0:
                      scanners.write(bytes(str(currentlyPlaying3[0]) + str(currentlyPlaying3[1]).zfill(3) + "1" + "\n", 'utf8')) #if another note is still playing after turning the current one off, tell the sound module to resume playing it

      #THIS CODE IS FOR THE DOT MATRIX PRINT HEAD, WHICH I ACCIDENTALLY DESTROYED A FEW WEEKS AGO BY CONNECTING POWER TO IT BACKWARD AND BLOWING ALL OF THE DRIVER TRANSISTORS.
      #THEREFORE, THIS CODE HAS NOT BEEN UPDATED IN A WHILE AND MAY BE INCONSISTENT WITH EVERYTHING ELSE. PLEASE IGNORE THIS SECTION WHEN REVIEWING MY CODE.
        '''if msg.channel == 6: #look at the messages in channel 0 for the first sound module
            if msg.type == 'pitchwheel':
                dotMatrix.write(bytes(str('696') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "0" + "\n", 'utf8'))
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    currentlyPlaying3.append(msg.note)
                    currentlyPlaying3.append(msg.velocity)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "0" + "\n", 'utf8')) #if we get a note_on, print it and write it to the arduino
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying3):
                    if value == msg.note:
                        currentlyPlaying3.remove(value)
                        currentlyPlaying3.pop(index)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + "000" + "0" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                if len(currentlyPlaying3) > 0:
                    dotMatrix.write(bytes(str(currentlyPlaying3[0]) + str(currentlyPlaying3[1]).zfill(3) + "0" + "\n", 'utf8'))
        if msg.channel == 7: #look at the messages in channel 4 for the second sound module
            if msg.type == 'pitchwheel':
                dotMatrix.write(bytes(str('696') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "1" + "\n", 'utf8'))
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    currentlyPlaying4.append(msg.note)
                    currentlyPlaying4.append(msg.velocity)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "1" + "\n", 'utf8')) #if we get a note_on, print it and write it to the arduino
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying4):
                    if value == msg.note:
                        currentlyPlaying4.remove(value)
                        currentlyPlaying4.pop(index)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + "000" + "1" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                if len(currentlyPlaying4) > 0:
                    dotMatrix.write(bytes(str(currentlyPlaying4[0]) + str(currentlyPlaying4[1]).zfill(3) + "1" + "\n", 'utf8'))
        if msg.channel == 9999: #look at the messages in channel 4 for the second sound module
            if msg.type == 'pitchwheel':
                dotMatrix.write(bytes(str('696') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "2" + "\n", 'utf8'))
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    currentlyPlaying5.append(msg.note)
                    currentlyPlaying5.append(msg.velocity)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "2" + "\n", 'utf8')) #if we get a note_on, print it and write it to the arduino
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying5):
                    if value == msg.note:
                        currentlyPlaying5.remove(value)
                        currentlyPlaying5.pop(index)
                #print(msg)o
                dotMatrix.write(bytes(str(msg.note) + "000" + "2" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                if len(currentlyPlaying5) > 0:
                    dotMatrix.write(bytes(str(currentlyPlaying5[0]) + str(currentlyPlaying5[1]).zfill(3) + "2" + "\n", 'utf8'))
        if msg.channel == 9999: #look at the messages in channel 4 for the second sound module
            if msg.type == 'pitchwheel':
                dotMatrix.write(bytes(str('696') + str(int(valmap(msg.pitch, -8192, 8192, 0, 16384))).zfill(5) + "3" + "\n", 'utf8'))
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    currentlyPlaying6.append(msg.note)
                    currentlyPlaying6.append(msg.velocity)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "3" + "\n", 'utf8')) #if we get a note_on, print it and write it to the arduino
            if msg.type == 'note_off':
                for index, value in enumerate(currentlyPlaying6):
                    if value == msg.note:
                        currentlyPlaying6.remove(value)
                        currentlyPlaying6.pop(index)
                #print(msg)
                dotMatrix.write(bytes(str(msg.note) + "000" + "3" + "\n", 'utf8')) #if we get a note_off, write it to the Arduino and set the velocity to 0 to turn the note off
                if len(currentlyPlaying6) > 0:
                    dotMatrix.write(bytes(str(currentlyPlaying6[0]) + str(currentlyPlaying6[1]).zfill(3) + "3" + "\n", 'utf8'))'''
        if msg.channel == 9:
            if msg.type == 'note_on':
                percussion1.write(bytes(str(msg.note) + str(msg.velocity).zfill(3) + "\n", 'utf8')) #if we get a percussion note, send it to the percussion sound module and the Arduino will determine whether it is a high or low pitched drum
                #print(msg)
except:
    floppy1.write(bytes(str(msg.note) + "000" + "\n", 'utf8'))
    floppy2.write(bytes(str(msg.note) + "000" + "\n", 'utf8'))
    scanners.write(bytes(str(msg.note) + "000" + "0" + "\n", 'utf8'))
    scanners.write(bytes(str(msg.note) + "000" + "1" + "\n", 'utf8'))
    time.sleep(2)
    floppy1.write(bytes(str("1024" + "\n"), 'utf8'))
    floppy2.write(bytes(str("1024" + "\n"), 'utf8'))
    scanners.write(bytes(str("1024" + "\n"), 'utf8'))
    percussion1.write(bytes(str("1024" + "\n"), 'utf8'))
    time.sleep(1)
    floppy1.close()
    floppy2.close()
    scanners.close()
    percussion1.close()
    sys.exit(0) #if an exception occured during playback (such as the user pressing Ctrl+C), silence and reset all of the sound modules

#dotMatrix.write(bytes(1024))
floppy1.write(bytes(str(msg.note) + "000" + "\n", 'utf8'))
floppy2.write(bytes(str(msg.note) + "000" + "\n", 'utf8'))
scanners.write(bytes(str(msg.note) + "000" + "0" + "\n", 'utf8'))
scanners.write(bytes(str(msg.note) + "000" + "1" + "\n", 'utf8'))
time.sleep(5)
floppy1.write(bytes(str("1024" + "\n"), 'utf8'))
floppy2.write(bytes(str("1024" + "\n"), 'utf8'))
scanners.write(bytes(str("1024" + "\n"), 'utf8'))
percussion1.write(bytes(str("1024" + "\n"), 'utf8')) #if playback finishes successfully, tell all of the sound modules to stop playing and reset them all
floppy1.close()
floppy2.close()
scanners.close()
percussion1.close()
#dotMatrix.close() #close connections to all Arduinos
