CDRecording
==============
Recording for Call Detail Reports

Synopsis
--------------
For use with the VoIP Barracuda Communications Server. Will grab Call Detail Records(CDRs) from the server from the previous day. Will count the incoming calls by each hour of the day and also provide averages by the hour for each day of the week.

Code Example
--------------

Motivation
--------------
The Barracuda Communications Server currently provides reporting features for calls, but it is limited in the features it provides and the counts it comes up with for various criteria and generally inaccurate in that they count each phone ringing as a call, rather then each incoming number. If you have 20 phones set to ring if someone calls your business it will say you had 20 calls, and this can change depending on if some of these phones are currently in use. 

This project aims to provide more useful counts and features so that business can more accurately gauge their highest call volume times.

Installation
--------------
No Need to install. The script will run as is.

API Reference
--------------

Tests
--------------

Contributors
--------------

License
--------------