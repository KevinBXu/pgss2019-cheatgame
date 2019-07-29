from pgss import bluff, call_bluff, game_state
import cheat
from cheat import client

def run_bot():

    game_id='a5873215-f79a-41f9-884a-b5a66d4596aa'
    #CHANGE GAME ID TO MATCH THE ONE YOU WANT TO JOIN

    bluff_thresh=.3 #temp
    call_thresh=.3 #temp
    in_progress=False
    c=cheat.client.Client("My_Cheat_Bot")

    join_game(c,game_id)
    #wait for the game to start
    while in_progress==False:
        x=c.get_current_turn()
        if x!=None:
            in_progress=True
        else:
            in_progress=False
    
    game_state=start_game(c)
    current_turn=0
    
    while in_progress==True:
        #start playing the game here
        c.update_game()
        c.update_player_info()

        print("local turn: "+str(current_turn))
        print("server turn: "+str(c.get_current_turn()))
        if current_turn!=c.get_current_turn():
            current_turn=c.get_current_turn()
            if int(current_turn['Position'])==game_state._bot_pos:
                value=c.get_current_turn()['CardValue']
                c.play_cards(decide_cards_to_play(value,game_state,bluff_thresh))
                game_state._bot._sequence.append(game_state._bot._sequence.pop(0))
                c.update_player_info()
                
            if int(current_turn['Position'])!=game_state._bot_pos:
                x=c.get_current_turn()
                if 'CardsDown' in x.keys():
                    if decide_call_bluff(x['Position'],call_thresh,x['CardValue'],x['CardsDown']):
                        c.play_call()
                        c.update_player_info()
                    else:
                        c.play_pass()
                        c.update_player_info()
            
"""
Joins the game.
"""
def join_game(client,game_id):
    c=client
    c.game_id=game_id
    c.join_game()
    c.update_game()
    c.update_player_info()

"""
Starts the game and initializes the variables within game_state.
"""
def start_game(client):
    c=client
    info=c.get_current_turn()
    c.update_game()
    c.update_player_info()
    c.hand.sort(key=lambda x:x['Value'])
    print("hand: "+str(c.hand))
    gs=game_state.GameState(c.players_connected,c.hand,int(c.position))
    return gs
    

"""
Decides which cards to play.
Considers whether or not to lie by calling decide_bluff.
Returns a list of cards to play.
"""
def decide_cards_to_play(value,game_state,bluff_thresh):
    print("hand on local: "+str(game_state._bot._hand))
    bot=game_state._bot
    value=bot.get_number_val(value)
    cards_to_play=[]
    if bot._num_each_card[bot.get_number_val(value)]!=0:
        for i in range(len(bot._hand)):
            if bot._hand[i]['Value']==value:
                bot._num_each_card[bot._hand[i]['Value']-1]-=1
                cards_to_play.append(bot._hand[i])

        bluff_card=decide_bluff(bluff_thresh,game_state,value)
        if bluff_card!=False:
            for i in range(len(bot._hand)):
                if bot._hand[i]==bluff_card:
                    bot._num_each_card[bot._hand[i]['Value']-1]-=1
                    cards_to_play.append(bot._hand[i])

        for i in cards_to_play:
            bot._hand.remove(i)
                    
        print("cards played (truth): "+str(cards_to_play))
        return cards_to_play
    else:
        print("cards played (forced to lie: "+str(bot.get_last_card_in_seq()))
        x=bot.get_last_card_in_seq()
        cards_to_play.append(x)
        bot._hand.remove(x)
        return cards_to_play
    
"""
Uses bluff.py to determine whether or not to lie.
If the bot decides to lie, it returns the card to lie with.
Otherwise, returns False.
"""
def decide_bluff(bluff_thresh,game_state,card_val):
    bluff_calc=bluff.BluffCalculator()
    if bluff_calc.should_bluff(game_state,game_state.get_number_val(card_val)) > bluff_thresh:
        bluff_card = bluff_calc.pick_card_to_lie_with(game_state)
        return bluff_card
    else:
        return False

"""
Uses call_bluff to determine whether or not to call bluff on an opponent.
Returns True if the bot decides to lie. Otherwise, returns False.
"""
def decide_call_bluff(opp,call_thresh,card_val,num_cards_played):
    call_bluff_calc = call_bluff.CallBluffCalculator()
    if call_bluff_calc.should_call_bluff(game_state,opp,card_val,num_cards_played)>=call_thresh:
        return True
    else:
        return False

"""
Updates the various variables in game_state.
This is called whenever the center pile is collected,
ie, when someone calls bluff.
"""
def center_pile_collected(game_state,player_num):
    for card in game_state.__known_center_cards:
        game_state.__players[player_num].__hand.append(game_state.__known_center_cards.pop(card))
    game_state.__num_played_cards+=game_state.__num_cards_center
    game_state.__num_cards_center=0
    #TODO: this looks good but I feel like something is missing.

if __name__ == '__main__':
    run_bot()
    
