# split-srt-file
Split a subtitle (.srt format) file into two parts. The initial version is tailored to Seven Samurai 1954, which is available in two DVDs. The available subtitle file was for the full length movie. This script produces two subtitle files, one for each of the two DVDs that hold the full movie. The original subtitle file is by prospero.13t@gmail.com

To generalize this script, simply replace the lines in the first code section "parameters" to specify the input file, the two output file names, the duration of the first DVD, and the data string that marks the last subtitle in the first DVD. The duration can be read from the DVD viewer when the first disk is loaded. (At least in the case of Seven Samurai 1954, in which the duration of the Intermission is included in the timing of the subtitle file.)

The files uploaded initially are:
- parse-srt-file.py        : the script
- Seven Samurai 1954.srt   : the original subtitle file by prospero.13t@gmail.com, downloaded 2026-09-16 from
                             https://www.opensubtitles.com/en/subtitles/seven-samorai
- Seven Samurai 1954.1.srt : the subtitle file for the first of two DVDs that hold the Seven Samurai 1954 movie
- Seven Samurai 1954.2.srt : the subtitle file for the second of two DVDs that hold the Seven Samurai 1954 movie

Comments to: github.com@cecst.com
