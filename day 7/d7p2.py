from functools import cmp_to_key

# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

def score_hand(hand):
    # Sort the cards - doesn't matter what order they are as long as like cards are grouped
    sorted_hand = sorted(hand)

    # Iterate the cards in the hand keeping track of what we last saw and how many we've seen
    match_list = []
    last_card = ""
    matched_so_far = 0
    jokers = 0
    for card in sorted_hand:
        if card == 'J':
            # First of all deal with any card matches we've just seen
            if matched_so_far > 1:
                match_list.append(matched_so_far)

            # Now deal with jokers differently - just count them for now and move on
            jokers += 1
            last_card = ""
            matched_so_far = 0
        else:
            if card == last_card:
                # Card matches last card - increment the match counter
                matched_so_far += 1
            else:
                # Card doesn't match last card - if we saw 2 or more before this one then note it
                if matched_so_far > 1:
                    match_list.append(matched_so_far)
                # Note this card and reset matched counter
                last_card = card
                matched_so_far = 1
    # Note any pairs or more that were found at the end of the sorted hand
    if matched_so_far > 1:
        match_list.append(matched_so_far)
    
    # Now sort our list of matches and increase the highest value by the number of jokers
    if len(match_list) > 0:
        match_list.sort()
        match_list[-1] += jokers
    else:
        # If we have a high hard hand then add the jokers to that high card - jokers + 1
        match_list.append(jokers + 1)

    # Return a number indicating the strength of the hand
    if(match_list == [5] or match_list == [6]): # The [6] is special case where we have a hand of JJJJJ
        return 7    # 5 of a kind
    elif(match_list == [4]):
        return 6    # 4 of a kind
    elif(match_list == [2,3]):
        return 5    # full house
    elif(match_list == [3]):
        return 4    # 3 of a kind
    elif(match_list == [2,2]):
        return 3    # 2 pair
    elif(match_list == [2]):
        return 2    # pair
    elif(match_list == [1]):
        return 1    # high card
    else:
        print(f"PANIC - unrecognized hand - {match_list} - hand: {sorted_hand}")
        exit(-1)

# Goes through the cards 1 by 1 comparing them and when they differ it returns -1 or 1 
# depending on which hard is higher just like a sort comparator function
def compare_card_by_card(line1, line2):
    card_order = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    
    for i in range(5):
        if line1[i] != line2[i]:
            return card_order.index(line1[i]) - card_order.index(line2[i])

# This is a sort comparator function which we have to use cmp_to_key() from functools
# to use since they took cmp= out of list.sort. It takes 2 values and returns -1, 0 or 1
# depending on which item is higher or lower
def poker_sort(line1, line2):
    # Get the scores of each hand
    hand1_score = score_hand(line1.split()[0])
    hand2_score = score_hand(line2.split()[0])
    
    # Return -1, 0 or 1
    if hand1_score == hand2_score:
        return compare_card_by_card(line1, line2)
    else:
        return hand1_score - hand2_score

#########################
# PROCESSING STARS HERE #
#########################

# All we need to do is sort our input using our poker sort function
input.sort(key=cmp_to_key(poker_sort))

# And then add up the score based on the sorted list
rank = 1
total = 0
for line in input:
    bet = line.split()[1]
    total += int(bet) * rank
    rank += 1

# Print the result
print(f"Total winnings: {total}")