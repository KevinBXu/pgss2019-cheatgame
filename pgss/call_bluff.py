import game_state

class CallBluffCalculator:

"""
Determines whether the bot should call bluff or not.
Returning a value of 1.0 means it is guaranteed to call bluff.
Otherwise, returns a float indicating the probability that it should
call bluff.
This float is used in bot.py by comparison against a threshold to ultimately
tell the bot if it should call or not.
"""
    def should_call_bluff(self,game_state, opponent, card_val, num_cards_played):
        # decides whether or not the bot should call bluff on another player.

	card_played = card_played
	if card_val=="J":
            card_val=10
        elif card_val=="Q":
            card_val=11
        elif card_val=="K":
            card_val=12
        k = game_state.__bot.__num_each_card[card_val] #should be the number of the sought card in own hand
        r = num_cards_played #should be the number of the sought card played by the opponent
        h = game_state.__bot.__hand.len() #should be own hand size
        l = game_state.__players[opponent].__hand.len() #should be opponent's hand size
        j = game_state.__bot.__cycles_until_win #should be how many turns until bot wins

	#immediately call bluff if it's the opponent's last card
        if (l==0):
            return 1.0

	#immediately call bluff if there appear to be more than four of a kind
        if (k+r > 4):
            return 1.0

	#otherwise, calculate the probability of the player lying
	#considers both the probability of the opponent not having the card
	#as well as how many cards are in the center pile (risk)
        #and how close the bot is to winning (it will not lie if it can win
        #in the next two turns), as it returns a negative float then.

        prob=probfunc.ncr(4-k,r)*probfunc.ncr(48-h+k,l-r)/probfunc.ncr(52-h,l)

        return  (1-prob)*(1/self.cards_in_pile)*((j-2)/20)
        #TODO: maybe find a better way to represent the risk considering
        #how close the bot is to winning, currently represented
        #by ((j-2)/20)

