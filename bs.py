import random
import operator
import time
import sys

"""
Heuristics for players
1) For each individual player, the chance that they call BS is equal to the number of cards they have divided by 4 + the remaining chance divided by other players - 1
    For example: if you have 3 9's, and there are 4 players playing you have a 75% + 25%/(3-1)chance of calling BS when a player says they played a 9
2) Should have different types of players: under-calls, "perfect" calls
3) The more cards in the pile, the less likely to call BS
4) Short-term "memory" to keep track of what was in the pile: the last time the number was played, if it is still in the pile factor that into
    BS calculation
5) 100% chance of calling BS is a player holds all four cards
6) There is a chance that a player plays both a real card and adds an additional card(s)
Display:
1) Number of cards each player is holding
2) Your cards, without suit, in order (ex: A, 2, 5, 10, J, Q, K)
User input:
1) For each turn, can choose to call BS
2) For user's turn, can input up to four cards (select from user's array of cards)
3) 
"""

class Card():
    
    ranks = {1: 'A', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 
             2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 
             7: '7', 8: '8', 9: '9'}
    
    def __init__(self, rank):
        # rank: ace through king
        self.rank = rank
        
    def __str__(self):
        return Card.ranks[self.rank]
    
    def __eq__(self, otherCard):
        # if not isinstance(otherCard, Card):
        #     raise TypeError("Arg not a card object")
        return self.rank == otherCard.rank
    
    def __gt__(self, otherCard):
        if not isinstance(otherCard, Card):
            raise TypeError("Arg not a card object")
        return self.rank > otherCard.rank
    
    def __ge__(self, otherCard):
        if not isinstance(otherCard, Card):
            raise TypeError("Arg not a card object")
        return self.rank >= otherCard.rank
    
    def __lt__(self, otherCard):
        if not isinstance(otherCard, Card):
            raise TypeError("Arg not a card object")
        return self.rank < otherCard.rank
    
    def __le__(self, otherCard):
        if not isinstance(otherCard, Card):
            raise TypeError("Arg not a card object")
        return self.rank <= otherCard.rank
    
    def __ne__(self, otherCard):
        if not isinstance(otherCard, Card):
            raise TypeError("Arg not a card object")
        return self.rank != otherCard.rank

class Deck():
    def __init__(self):
        self.deck = []
        self.size = 0
        
    
    def __str__(self):
        return " ".join([str(card) for card in self.deck])
    
    def new_deck(self):
        ranks = 4 * list(range(1, 14))
        self.deck = [Card(r) for r in ranks]
        temp = []
        for l in range(52, 0, -1):
            temp.append(self.deck.pop(random.randrange(l)))
        self.deck = temp
        self.size = 52
    
    def deal_card(self):
        if self.size == 0:
            return None
        self.size -= 1
        return self.deck.pop()
    
    
    def play_card(self, card):
        # play a card in the deck
        if card not in self.deck:
            return None
        self.size -= 1
        return self.deck.pop(self.deck.index(card))
    
    def play_random_card(self):
        # play a card in the deck
        if  self.size == 0:
            return None
        self.size -= 1
        return self.deck.pop(random.randrange(self.size))
    
    def add_card(self, card):
        self.deck = [card] + self.deck
        self.size += 1
    
    def add_list_of_cards(self, cards):
        self.deck.extend(cards)
        self.size += len(cards)
        
    def add_deck(self, newDeck):
        self.deck.extend(newDeck.deck)
        self.size += len(newDeck.deck)

    def num_cards(self, card):
        # return number of cards in deck that match given card
        return self.deck.count(card)
            
    def cards_in_deck(self, cards):
        # cards: an array of cards
        temp = []
        for c in cards:
            if c not in self.deck:
                self.add_list_of_cards(temp)
                return False
            else:
                temp.append(c)
                self.deck.remove(c)
        self.add_list_of_cards(temp)
        return True

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = Deck()
        
    def __str__(self):
        return self.name + "'s hand: " + str(self.hand)
    
    def __eq__(self, player):
        return self.name == player.name
    
    def call_BS(self, currPlayer, total_players, currentCard, num_cards_played, pile):
        """
        return True if player decides to call BS 
        total_players: number of players playing the game
        currentCard: current card object that should be played
        playedCards: list of cards played by the player that played
        pile: deck of cards that is the pile
        """
        # memory of number of last appearnces of current card being played in pile
        # assuming player would keep track of peanut butter, know if card played not legitimate
        matching_pile = pile.size // 13
        matching_hand = self.hand.num_cards(currentCard)
        magic = matching_pile + matching_hand + num_cards_played
        
        # there can't be more than four of one card
        if magic > 4: 
            return True
        if currPlayer.hand.size == 0: 
            return True #otherwise they would win the game
        if num_cards_played == 4: #matching_hand, matching_pile == 0
            return random.random() < 0.9 ** pile.size #if few cards in pile, almost certainly will call it, otherwise would be risky for other player to call BS, so more likely to be true
        else:
            return random.random() < (1 - ((5 - magic) / total_players)) - 0.3 

def main():
    new_deck = Deck()
    new_deck.new_deck()
    # 1 player playing, other players are automated
    username = input("What is your name?\n")
    user = Player(username) 
    
    while True: 
        num_players = input("Enter number of other players (3-6):\n")
        if num_players.isdigit() and int(num_players) >= 3 and int(num_players) <= 6:
            num_players = int(num_players)
            break 
        print("Invalid input, please try again")
    
    # create list of players to store players
    players = []
    players.append(user)
    # create new players for number of players inputed
    for x in range(num_players):
        players.append(Player("player{0}".format(x+1)))
        
    total_players = num_players + 1 # includes user
    # deal hands to all players
    for x in range(new_deck.size):
        players[x % total_players].hand.add_card(new_deck.deal_card())
    
    currentCardRank = 0
    rank_lookup = {a: b for b, a in Card.ranks.items()}
    pile = Deck()
    while True:
        for currPlayer in players:
            currentCard = Card((currentCardRank % 13) + 1)
            # print current card totals for each player
            print("\n" * 50) #"clear" playing screen
            print("-" * 60)
            user.hand.deck.sort()
            print(user)
            print("Current card totals: ")
            for y in players:
                print(y.name + ": " + str(y.hand.size), end = "  ")
            print("\nCard being played: " + str(currentCard) + " | Cards in pile: " + str(pile.size))
            print("Turn: " + currPlayer.name)
            
            print("\n" * 4)
            time.sleep(1)
            num_cards_played = 0
            if currPlayer == user:
                tryagain = False
                while True:
                    currPlayer.hand.deck.sort()
                    print(currPlayer)
                    cardRanks = input("Type the cards you want to play (with a space between them): ")
                    cardRanks = cardRanks.split()
                    cards = []
                    for rank in cardRanks:
                        try: 
                            cards.append(Card(rank_lookup[rank]))
                        except KeyError:
                            print("Invalid card name(s), try again\n")
                            time.sleep(2)
                            print("\n" * 50) #"clear" playing screen
                            print("-" * 60)
                            user.hand.deck.sort()
                            print(user)
                            print("Current card totals: ")
                            for y in players:
                                print(y.name + ": " + str(y.hand.size), end = "  ")
                            print("\nCard being played: " + str(currentCard) + " | Cards in pile: " + str(pile.size))
                            print("Turn: " + currPlayer.name)
                            print("\n" * 4)
                            tryagain = True
                    if tryagain:
                        tryagain = False
                        continue
                    if currPlayer.hand.cards_in_deck(cards): #cards chosen are in player's hand
                        print("\n" * 50) #"clear" playing screen
                        print("-" * 60)
                        user.hand.deck.sort()
                        print(user)
                        print("Current card totals: ")
                        for y in players:
                            print(y.name + ": " + str(y.hand.size), end = "  ")
                        print("\nCard being played: " + str(currentCard) + " | Cards in pile: " + str(pile.size))
                        print("Turn: " + currPlayer.name)
                        print("\n" * 4)
                        print("Card(s) played successfully")
                        num_cards_played = len(cards)
                        for c in cards: # add cards from player to pile
                            pile.add_card(currPlayer.hand.play_card(c))                        
                        time.sleep(2)
                        break
                    else: 
                        print("You don't have all of those cards, try again\n")
                        time.sleep(2)
                        print("\n" * 50) #"clear" playing screen
                        print("-" * 60)
                        user.hand.deck.sort()
                        print(user)
                        print("Current card totals: ")
                        for y in players:
                            print(y.name + ": " + str(y.hand.size), end = "  ")
                        print("\nCard being played: " + str(currentCard) + " | Cards in pile: " + str(pile.size))
                        print("Turn: " + currPlayer.name)
                        print("\n" * 4)
            else: #simple behavior for calling BS
                if currentCard in currPlayer.hand.deck:
                    while currentCard in currPlayer.hand.deck:
                        pile.add_card(currPlayer.hand.play_card(currentCard))
                        num_cards_played += 1
                else:
                    for i in range(random.randrange(1, 4)):
                        pile.add_card(currPlayer.hand.play_random_card())
                        num_cards_played += 1
                print("\n" * 50) #"clear" playing screen
                print("-" * 60)
                user.hand.deck.sort()
                print(user)
                print("Current card totals: ")
                for y in players:
                    print(y.name + ": " + str(y.hand.size), end = "  ")
                print("\nCard being played: " + str(currentCard) + " | Cards in pile: " + str(pile.size))
                print("Turn: " + currPlayer.name)
                print("\n" * 4)
                print(currPlayer.name + " plays " + str(num_cards_played) + " cards")
                
            # TODO: user input controls, display auto player actions, option to call BS
            player_truthful = all(elem == currentCard for elem in cards) #True if played cards are all same as current card
            # randomize the order of players choosing when to call BS
            shuffled_players = players.copy()
            random.shuffle(shuffled_players)
            for p in shuffled_players:
                if p == currPlayer:
                    continue
                elif p == user:
                    while True:
                        response = input("Do you want to call BS? (Y/N) ")
                        if response.upper() == "Y":
                            print(p.name + " calls BS!")
                            time.sleep(2)
                            if player_truthful:
                                print(p.name + " was wrong! " + p.name + " takes the pile.")
                                p.hand.add_deck(pile)
                                pile = Deck()
                            else: 
                                print(p.name + " was right! " + currPlayer.name + " takes the pile.")
                                currPlayer.hand.add_deck(pile)
                                pile = Deck()
                            time.sleep(2)
                            break
                        elif response.upper() == "N":
                            break
                        else:
                            print("Invalid input, please try again")
                    break
                elif p.call_BS(currPlayer, total_players, currentCard, num_cards_played, pile):
                    print(p.name + " calls BS!")
                    time.sleep(2)
                    if player_truthful:
                        print(p.name + " was wrong! " + p.name + " takes the pile.")
                        p.hand.add_deck(pile)
                        pile = Deck()
                    else:
                        print(p.name + " was right! " + currPlayer.name + " takes the pile.")
                        currPlayer.hand.add_deck(pile)
                        pile = Deck()
                    time.sleep(2)
                    break
            if currPlayer.hand.size == 0:
                print(currPlayer.name + " won!")
                time.sleep(3)
                sys.exit()
            time.sleep(1)
            currentCardRank += 1
        
        
        
main()