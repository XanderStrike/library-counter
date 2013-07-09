library-counter
===============

Door Counter for the Voskuyl Library.

This simple python app was designed to run on a Raspberry Pi (R2) and interface with a sensor that has a normally closed relay to count the number of people who pass through a given area. It records the events in the database as a timestamp, allowing for graphing activity over time, and it can save over a million records on an 8 gig card. It also provides a simple web interface for displaying daily counts and graphing.

Similar systems can cost hundreds or thousands of dollars and have half the features. This does it for less than $150.

Installation & Running
--------------------

**You'll Need**

* Raspberry Pi (Tested on Model B Revision 2)
* SD Card
* Sensor (like [this magnetic one](http://www.amazon.com/Directed-Electronics-8601-Magnetic-Switch/dp/B0009SUF08/ref=sr_1_1?ie=UTF8&qid=1373390827&sr=8-1&keywords=magnetic+door+switch) or [this infrared one](http://www.amazon.com/Enforcer-Indoor-Outdoor-Mounted-Photoelectric/dp/B001LFPB0M/ref=pd_sim_sbs_hi_2) if you're hardcore)
* Some wires
* Network connectivity, wireless or otherwise

**Installing**

1. Flash the newest version of Raspbian to your SD Card
2. Install git and run `git clone https://github.com/XanderStrike/library-counter.git`
3. Attach your relay to the 3.3v out and GPIO4 (see [here](http://i.imgur.com/Px57C0c.png) for reference)
4. Run `sudo python counter.py` and `sudo python server.py` in your favorite daemonized way, I prefer screen but you can also run `sudo python counter.py & sudo python server.py &`

Usage
-----

To test that you've got the sensor connected properly, simply run `counter.py` and make sure that it's outputting values when the sensor trips. To test the webserver, run `server.py` and visit the Pi's IP address.

**Views**

`/` Displays the count for today, starting at midnight, and has provides a graph of activity over the last 24 hours.

`/graph` Displays a graph of activity over the last 24 hours. Useful for embedding into larger information boards.

**API**

`/api/<period>` Outputs a JSON array of all the times in the given time period*

`/api/count/<period>` Outputs a count of all recorded activity in the given time period*

*Periods include `today` for current day starting at midnight, `hour` for the past hour, `day` for last 24 hours, `week` for last 7 days, `month` for last 30 days, `year` for last 365 days.