# Deisgn Document for bs
Terminal-based single-player card game of BS.

### Instructions for running code
1. Download Python from https://www.python.org/
2. Download bs.py program
2. Open command line/terminal
3. Run the program
* On Windows: type C:\python37\python.exe {fileDirectory}\bs.py
* On Mac: cd into correct directory where downloaded program is located, then type python bs.py

### Tests ran
The tests I wrote mostly deal with invalid inputs, for example:
* Invalid card type (not A, J, Q, K, or number 2-10)
* No input at all 
* Cards not in hand
* Non Y or N answers

### Rules for BS
From the following source:
https://considerable.com/how-to-play-cheat/

"Deal the cards out evenly. If there are remainders, place them face down in the center of the table as the beginning of the discard pile.

Play begins with the player to the left of the dealer. He places the Aces in his hand facedown on the discard pile and announces his play to the table: “One Ace.” If the player does not have any Aces, or if he wishes to get rid of more than one card, he may bluff and play non-Ace cards while announcing: “Two Aces.” The next player plays 2s, the next player plays 3s, and so on. If a player doesn’t believe an announcement, he can call out, “Cheat!” The person who played the cards must turn them over and show the challenger whether he is bluffing or not. A player who is caught bluffing must pick up the entire discard pile and add it to his hand. If a challenged player is not bluffing, then the challenger must pick up the discard pile. When the rank to play reaches Kings, it then goes back to Aces and the numbers start again.

The first player to get rid of all his cards wins. Usually this is the first player to actually have the last card that must be played on his turn."

### Design choices
I decided to make three class types, a Card class, a Deck class, and a Player class. Within each class, I made object-specific functions (for example, adding cards to a deck, removing cards from a deck, deciding to call BS or not). This helped make things more straightforward with coding. Otherwise, the only data structures I used were lists and dictionaries. Lists were used to store cards, dictionaries to look up the correct string card rank for a number or vice versa. 

I unfortunately didn't have the time to develop a better algorithm for deciding to call BS or not for the non-user players, so it only roughly approximates the behavior based on number of cards played, the current card, and a short-term "memory" of whether the card is in the pile or not. The algorithm for non-user players playing cards is either the players has the card and plays it, or the player plays a random number of cards. 

### Why Python
I was thinking of writing this in C, however, it would have taken longer than 3 hours. I was able to utilize Python's random and time libraries, as well as built-in functions to work with lists (sorting in place, search for elements, append and extend lists, etc.)
