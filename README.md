# ChopChop:<br> lightweight snipping tool

ChopChop was created as an alternative for bulkier screenshot tools such as
windows default snipping tool or Screenpresso.

The goal is to be as quick, lightweight and minimalistic as possible - to accomplish
the same things with fewest mouse clicks possible.

Main characteristics:
-
- You start snipping immediately after running ChopChop - 
this will be indicated by cursor changing to crosshair
- There is no static menu or window 
- You choose what you want to do with your
snip by using the contextual menu that appears after you select the area
- If you press ESC at any stage, ChopChop is gone and out of your way
- Default saving behavior is to just give the name of the file (it will be saved at a default location) - if you're taking
a bunch of screenshots in quick succession, no need to go through the browse window every time.
- Pop open the default folder at any time - just right click anywhere in 
snipping mode or with context menu open to see all your saved snips

How to use ChopChop
-
copy image to clipboard
![Clipboard demo](Examples/clipboard.gif)
 
save image to file

![file demo](Examples/to_file.gif)
<br><br>


- to see all your previously saved snips, 
just press right mouse button anywhere on the screen
or choose "folder" option from the context menu

- pick the "email" option from context menu to create a new email
with your snip in the body (requires email client, eg. Outlook)

- MS Teams integration will be added in the future - currently the "teams" button is greyed out


Installing ChopChop in 3 steps:
-
(make sure you have Python3 and git installed)
- clone this repository to your computer with <br> 
```git clone https://github.com/raczynskid/ChopChop.git```<br>
- install the requirements with <br> 
```pip install requirements txt```<br>
- create a shortcut where target is <br>
```[path to your pythonw (the "w" means no console window)][space][path to __main__.py]```
example:
![shortcut](Examples/shortcut.png)