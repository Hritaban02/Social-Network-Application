# Social-Network-Application

Consider a social network application where there are:
- Users: identified by unique user id (String)
- Groups: which are sets of users who are members of the group. The group is identified
by a unique group id.
- Contacts: A list of other users who are in the contact list of a given user.
- Posts: A string and / or an image which can be posted by the user.
Like in a social network, posts of users can be to a contact or a group. All posts to a group
appear in the incoming messages list for all members of the group. All direct posts from a
contact also appear as incoming messages. For this current assignment, the list of users, their
contacts, and the list of groups is given as an input from a file (named
social_network.txt) of the following format:
# users
<user_id1: contact_user1, contact_user2, …>
…
<user_idn: contact_user1, contact_user2, …>
#groups
<group_id1: member1, member2, …>
…
<group_idn: member1, member2, …>

Initially there are zero messages. As the system operates, the users may post messages, which
should be displayed appropriately. Additionally, all the posted messages should be saved in file
messages.txt, for future runs of the program.
There are four visual modules to be displayed on the screen. Each module displays information
pertaining to a current user. The information in the modules should change dynamically as the
user changes. The modules are:
- A module to display incoming messages. The text of the message and the image (if any)
should both be displayed, formatted appropriately.
- A module to display existing contacts.
- A module to display groups of which the current user is member of.
- A module to compose and post messages. This should also include the
Additionally, there should be a droplist / menu for selecting the current user.
Write a python program which implements the above mentioned functionality using TKinter
GUI toolkit in python.
