#!/usr/bin/python3

"""
Goal: split the subtitle (.srt) file into two parts, to match the two mp4 files into which
      the film is split.
Method:
This script reads the named subtitle (.srt) file for Seven Samuri and tracks the time at
which the INTERMISSION tag appears. It writes the contents of the original file unchanged
into the first output file until that tag appears. Then, it begins to subtract the duration
of the first DVD from the times of the subtitles that appear subsequently. The data are 
then written into the second output file.

This script could be generalized easily by replacing the parameters in the first section
of code below with the data that match the new DVD and .srt file.

Date:  Sept 17, 2026
Programmer: Lawrence Widman
"""

# parameters
input_file = "/home1/widman/Videos/Seven Samurai 1954.srt"
output_file1 = "/home1/widman/Videos/Seven Samurai 1954.1.srt"
output_file2 = "/home1/widman/Videos/Seven Samurai 1954.2.srt"
first_segment_duration_hour  = 1; 
first_segment_duration_min   = 52; 
first_segment_duration_sec   = 0; 

# global flags
epoch_counter = 0
the_clock     = 0
time_offset_hour = 0
time_offset_min  = 0
time_offset_sec  = 0
intermission_flag = 0

def my_exit():
  if 'fp_in' in globals():
    fp_in.close()
  if 'fp_out1' in globals():
    fp_out1.close()
  if 'fp_out2' in globals():
    fp_out2.close()
  exit()

def print_epoch():
   print(f"Epoch: {epoch}\nTimes: {the_times}\nData1: {text1}\nData2: {text2}\nExtra line: {last_line}")

try: 
  fp_in    = open(input_file, "r")
except FileNotFoundError:
  print(f"Cannot open file {input_file}")
  my_exit()
try: 
  fp_out1  = open(output_file1, "w")
except IOError:
  print(f"Cannot open file {output_file1} for writing")
  my_exit()
try: 
  fp_out2  = open(output_file2, "w")
except IOError:
  print(f"Cannot open file {output_file2} for writing")
  my_exit()

while True:
    line = fp_in.readline()
    if not line:
        break
    # print(line.strip())
    epoch = line.strip()
    
    # check epoch number
    epoch_counter = epoch_counter + 1
    if epoch_counter != int(epoch):
       print(f"error: epoch should be {epoch_counter} but I just read {epoch}")
       my_exit()

    # get and parse the times (eg 00:01:12,822 --> 00:01:14,490 where the 3 digits following the commas are milliseconds)
    the_times = fp_in.readline().strip()
    start_hour = int(the_times[0:2]); start_min  = int(the_times[3:5]); start_sec  = int(the_times[6:8]); start_msec = int(the_times[ 9:12])
    end_hour = int(the_times[17:19]); end_min  = int(the_times[20:22]); end_sec  = int(the_times[23:25]); end_msec = int(the_times[26:29])
    #print(f"original: '{the_times}'")
    #print(f"parsed:   {start_hour:02d}:{start_min:02d}:{start_sec:02d},{start_msec:03d} --> {end_hour:02d}:{end_min:02d}:{end_sec:02d},{end_msec:03d}")

    # get the first (and maybe only) text line
    text1 = fp_in.readline().strip()

    # get the next line, either blank or text line
    text2 = fp_in.readline().strip()

    if len(text2) > 0:
       # this one had better be blank
       last_line = fp_in.readline().strip()
    else:
       last_line = text2

    if len(last_line) != 0:
       print("Error: there is no blank line after a maximum of two data lines.")
       print_epoch()
       my_exit()

    # now we have read the current epoch. If we are before the intermission, we write it to fp_out1. Otherwise, we substract time_offset and write to fp_out2
    if 1 == intermission_flag:
      start_hour = start_hour - time_offset_hour; start_min = start_min - time_offset_min; start_sec = start_sec - time_offset_sec; 
      # correct to avoid negative times
      if start_sec < 0:
        start_sec = start_sec + 60
        start_min = start_min - 1
      if start_min < 0:
        start_min  = start_min + 60
        start_hour = start_hour - 1
      end_hour   = end_hour   - time_offset_hour; end_min   = end_min   - time_offset_min; end_sec   = end_sec - time_offset_sec; 
      if end_sec < 0:
        end_sec = end_sec + 60
        end_min = end_min - 1
      if start_min < 0:
        end_min  = end_min + 60
        end_hour = end_hour - 1
      # compose the new time string
      the_times_new = f"{start_hour:02d}:{start_min:02d}:{start_sec:02d},{start_msec:03d} --> {end_hour:02d}:{end_min:02d}:{end_sec:02d},{end_msec:03d}"
      # and now write to fp_out2
      fp_out2.write(f"{epoch}\n{the_times_new}\n{text1}\n")
      if len(text2) > 0:
         fp_out2.write(f"{text2}\n")
      fp_out2.write("\n")
    else:
      # come here for the first part of the input file, before the INTERMISSION tag. We write the original data to this file without modifying the times.
      fp_out1.write(f"{epoch}\n{the_times}\n{text1}\n")
      if len(text2) > 0:
         fp_out1.write(f"{text2}\n")
      fp_out1.write("\n")

    # now check to see whether we have found the end of the first DVD
    if text1 == '<font color="#ff8040">INTERMISSION</font>':
       intermission_flag = 1
       # this is the duration of the first DVD including the end-matter
       time_offset_hour  = first_segment_duration_hour; 
       time_offset_min   = first_segment_duration_min;
       time_offset_sec   = first_segment_duration_sec;

    #print_epoch()
     
print ("Done")
my_exit()


