streakalert
===========

Pointless script that will remind you to commit something to GitHub to keep your current streak going.

How
---

* Define your `from_email` and `to_email` addresses in config.py
* Define the minimum current streak you must have before you are notified
* Setup a cron job to run this once a day or something (at a time where you might forget you need to commit something, but still have time to do so).

Requires
-------
* BeautifulSoup4 (because there's no GitHub API call for current streaks)
* urllib2

Why?
---

Uh, I dunno. Maybe to help you get an amazing contribution streak on GitHub so that you can show off to all your friends? Yay for arbitrary numbers!

I take no responsibility if people just commit spam pointless things to keep their streak going.
