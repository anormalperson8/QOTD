# QOTD Eevee

A Discord bot for asking Question of the Day regularly.<br/>
Written specifically for friends' Discord servers.
A lot of the code is referenced from my other project [Birthday Eevee](https://github.com/anormalperson8/Birthday).

## Version 1.0
- Most, if not all, planned functions have been implemented!
- This bot allows users to submit questions to the system, moderators approve them,
and ask them in the designated channel every day.
- Currently, this bot does not support different questions for different servers<br/>
  (i.e. all servers share the same question "database")

## Main files

### [main.py](/main.py)
The file that stores all the commands and interactions.

### [pageClasses](/pageClasses)
The directory that contains UI class files.

### [question.py](/question.py)
The file that stores functions to read and write questions.

### [info_command.py](/info_command.py)
The file that stores contents of the `info` slash command, as there are a lot of text in that.

### [server_info.py](/server_info.py)
The file that stores all the code that is used to retrieve server data, such as its ID of the announcement channel.

### [Dependencies](/requirements.txt)
This file holds packages one needs to additionally install to host this bot.

## FAQ
#### Can I host this bot myself?
- Yes, but please contact me for permission if you do.

#### How do I host this bot myself?
- To be added.

#### Is the code really spaghetti?
- Served with inconsistencies.

