import pandas as pd
import random
from io import StringIO

# Load the win probability matrix
win_prob_matrix = pd.read_csv('winprob_matrix_tipped_off_6.10.csv', index_col=0) ## changed file path; ask me for csv if you need it

# List of seeded players
seeded_players = [
    'Zain', 'Cody Schwab', 'aMSa', 'Mang0', 'Hungrybox', 'Jmook', 'moky', 'Plup',
    'Soonsay', 'Wizzrobe', 'Spark', 'Joshman', 'Aklo', 'SDJ', 'Salt', 'Krudo',
    'Axe', 'KoDoRiN', 'Chem', 'Ossify', 'ckyulmiqnudaetr', 'Junebug', 'Lucky', 'Wally', 
    'S2J', 'bobby big ballz', 'mvlvchi', '2saint', 'Zamu', 'Colbol', 'Akir', 'Panda',
    'n0ne', 'KJH', 'Drephen', 'CPU0', 'Wevans', 'Fro116', 'MOF', 'Preeminent',
    'essy', 'Khryke', 'Zanya', 'Lowercase hero', 'max', 'Gahtzu', 'Zasa', 'Inky',
    'Maelstrom', 'Komodo', 'Unsure', 'Balloon Day', 'Dawson', 'Louis', 'mayb', 'Paladin',
    'Chango', 'salami', 'Beezy', 'SDeems', 'Egg$', 'billybopeep', 'Kalvar', 'Panko'
]

def run_tournament_simulation(win_prob_matrix, seeded_players):

    # Initialize the DataFrame for Winners Round 1
    data = {
        'Player 1': seeded_players[:32],
        'Player 2': seeded_players[63:31:-1],  # Reverse the second half
        'WinProb': [0] * 32,
        'Winner': [None] * 32,
        'Loser': [None] * 32
    }

    df = pd.DataFrame(data)

    placements = {
        '1st': [],
        '2nd': [],
        '3rd': [],
        '4th': [],
        '5th': [],
        '7th': [],
        '9th': [],
        '13th': [],
        '17th': [],
        '25th': [],
        '33rd': [],
        '49th': []
    }

    def update_placement(position, player):
        placements[position].append(player)

    # Fill the WinProb column using the win probability matrix
    for i in range(32):
        player1 = df.at[i, 'Player 1']
        player2 = df.at[i, 'Player 2']
        df.at[i, 'WinProb'] = win_prob_matrix.at[player1, player2]

    # Determine the winners and losers for WR1
    for i in range(32):
        player1 = df.at[i, 'Player 1']
        player2 = df.at[i, 'Player 2']
        win_prob = df.at[i, 'WinProb']
    
        if random.random() < win_prob:
            df.at[i, 'Winner'] = player1
            df.at[i, 'Loser'] = player2
            print(f"{player1} beats {player2} (WR1)")
        else:
            df.at[i, 'Winner'] = player2
            df.at[i, 'Loser'] = player1
            print(f"{player2} beats {player1} (WR1)")

    # Prepare for the next round of loser's matches
    losers = df['Loser'].tolist()
    losers_df = pd.DataFrame({
        'Player 1': losers[::2],
        'Player 2': losers[1::2],
        'WinProb': [0] * 16,
        'Winner': [None] * 16,
        'Loser': [None] * 16
    })

    # Calculate win probabilities for the loser's matches
    for index, row in losers_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches
    for index, row in losers_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_df.at[index, 'Winner'] = winner
        losers_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (49th)")
        update_placement('49th', loser)
    
    # Initialize the DataFrame for Winners Round 2
    winners = df['Winner'].tolist()
    winners_1st_half = winners[:16]
    winners_2nd_half = winners[16:][::-1]  # Reverse the second half for correct matching

    wr2_data = {
        'Player 1': winners_1st_half,
        'Player 2': winners_2nd_half,
        'WinProb': [0] * 16,
        'Winner': [None] * 16,
        'Loser': [None] * 16
    }

    wr2_df = pd.DataFrame(wr2_data)

    # Fill the WinProb column using the win probability matrix
    for i in range(16):
        player1 = wr2_df.at[i, 'Player 1']
        player2 = wr2_df.at[i, 'Player 2']
        wr2_df.at[i, 'WinProb'] = win_prob_matrix.at[player1, player2]

    # Determine the winners and losers for WR2
    for i in range(16):
        player1 = wr2_df.at[i, 'Player 1']
        player2 = wr2_df.at[i, 'Player 2']
        win_prob = wr2_df.at[i, 'WinProb']
    
        if random.random() < win_prob:
            wr2_df.at[i, 'Winner'] = player1
            wr2_df.at[i, 'Loser'] = player2
            print(f"{player1} beats {player2} (WR2)")
        else:
            wr2_df.at[i, 'Winner'] = player2
            wr2_df.at[i, 'Loser'] = player1
            print(f"{player2} beats {player1} (WR2)")

    # Prepare for the next round of loser's matches (33rd place)
    losers_wr2 = wr2_df['Loser'].tolist()
    winners_losers = losers_df['Winner'].tolist()

    losers_33rd_data = {
        'Player 1': winners_losers,
        'Player 2': losers_wr2,
        'WinProb': [0] * 16,
        'Winner': [None] * 16,
        'Loser': [None] * 16
    }

    losers_33rd_df = pd.DataFrame(losers_33rd_data)

    # Calculate win probabilities for the loser's matches (33rd place)
    for index, row in losers_33rd_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_33rd_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches (33rd place)
    for index, row in losers_33rd_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_33rd_df.at[index, 'Winner'] = winner
        losers_33rd_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (33rd)")
        update_placement('33rd', loser)

    # Prepare for the next round of loser's matches (25th place)
    losers_33rd_winners = losers_33rd_df['Winner'].tolist()

    # Organize the winners to match top vs bottom, etc.
    half_length = len(losers_33rd_winners) // 2
    losers_25th_data = {
        'Player 1': losers_33rd_winners[:half_length],
        'Player 2': losers_33rd_winners[-1:-half_length-1:-1],
        'WinProb': [0] * half_length,
        'Winner': [None] * half_length,
        'Loser': [None] * half_length
    }

    losers_25th_df = pd.DataFrame(losers_25th_data)

    # Calculate win probabilities for the loser's matches (25th place)
    for index, row in losers_25th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_25th_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Combine initial DataFrames for WR1 and Losers Round 1
    combined_df = pd.concat([df, losers_df], ignore_index=True)

    # Simulate the loser's matches (25th place)
    for index, row in losers_25th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_25th_df.at[index, 'Winner'] = winner
        losers_25th_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (25th)")
        update_placement('25th', loser)

    # Combine the DataFrames for WR2 and Losers Round 2
    combined_df = pd.concat([combined_df, wr2_df, losers_33rd_df, losers_25th_df], ignore_index=True)

    # Initialize the DataFrame for Winners Round 3
    winners_wr2 = wr2_df['Winner'].tolist()
    winners_wr3_1st_half = winners_wr2[:8]
    winners_wr3_2nd_half = winners_wr2[8:][::-1]  # Reverse the second half for correct matching

    wr3_data = {
        'Player 1': winners_wr3_1st_half,
        'Player 2': winners_wr3_2nd_half,
        'WinProb': [0] * 8,
        'Winner': [None] * 8,
        'Loser': [None] * 8
    }

    wr3_df = pd.DataFrame(wr3_data)

    # Fill the WinProb column using the win probability matrix
    for i in range(8):
        player1 = wr3_df.at[i, 'Player 1']
        player2 = wr3_df.at[i, 'Player 2']
        wr3_df.at[i, 'WinProb'] = win_prob_matrix.at[player1, player2]

    # Determine the winners and losers for WR3
    for i in range(8):
        player1 = wr3_df.at[i, 'Player 1']
        player2 = wr3_df.at[i, 'Player 2']
        win_prob = wr3_df.at[i, 'WinProb']
    
        if random.random() < win_prob:
            wr3_df.at[i, 'Winner'] = player1
            wr3_df.at[i, 'Loser'] = player2
            print(f"{player1} beats {player2} (WR3)")
        else:
            wr3_df.at[i, 'Winner'] = player2
            wr3_df.at[i, 'Loser'] = player1
            print(f"{player2} beats {player1} (WR3)")

    # Prepare for the next round of loser's matches (17th place)
    losers_wr3 = wr3_df['Loser'].tolist()
    winners_losers_25th = losers_25th_df['Winner'].tolist()

    losers_17th_data = {
        'Player 1': winners_losers_25th,
        'Player 2': losers_wr3,
        'WinProb': [0] * 8,
        'Winner': [None] * 8,
        'Loser': [None] * 8
    }

    losers_17th_df = pd.DataFrame(losers_17th_data)

    # Calculate win probabilities for the loser's matches (17th place)
    for index, row in losers_17th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_17th_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches (17th place)
    for index, row in losers_17th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_17th_df.at[index, 'Winner'] = winner
        losers_17th_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (17th)")
        update_placement('17th', loser)

    # Combine the DataFrames for WR3 and Losers Round 3
    combined_df = pd.concat([combined_df, wr3_df, losers_17th_df], ignore_index=True)

    # Prepare for the next round of loser's matches (13th place)
    losers_17th_winners = losers_17th_df['Winner'].tolist()

    # Organize the winners to match top vs bottom, etc.
    half_length = len(losers_17th_winners) // 2
    losers_13th_data = {
        'Player 1': losers_17th_winners[:half_length],
        'Player 2': losers_17th_winners[-1:-half_length-1:-1],
        'WinProb': [0] * half_length,
        'Winner': [None] * half_length,
        'Loser': [None] * half_length
    }

    losers_13th_df = pd.DataFrame(losers_13th_data)

    # Calculate win probabilities for the loser's matches (13th place)
    for index, row in losers_13th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_13th_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches (13th place)
    for index, row in losers_13th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_13th_df.at[index, 'Winner'] = winner
        losers_13th_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (13th)")
        update_placement('13th', loser)

    # Combine the DataFrames for Losers Round 4 (13th place)
    combined_df = pd.concat([combined_df, losers_13th_df], ignore_index=True)

    # Prepare for the Winners Quarterfinals matches (WQF)
    winners_wr3 = wr3_df['Winner'].tolist()
    winners_wr3_1st_half = winners_wr3[:4]
    winners_wr3_2nd_half = winners_wr3[4:][::-1]  # Reverse the second half for correct matching

    wqf_data = {
        'Player 1': winners_wr3_1st_half,
        'Player 2': winners_wr3_2nd_half,
        'WinProb': [0] * 4,
        'Winner': [None] * 4,
    '   Loser': [None] * 4
    }

    wqf_df = pd.DataFrame(wqf_data)

    # Fill the WinProb column using the win probability matrix
    for i in range(4):
        player1 = wqf_df.at[i, 'Player 1']
        player2 = wqf_df.at[i, 'Player 2']
        wqf_df.at[i, 'WinProb'] = win_prob_matrix.at[player1, player2]

    # Determine the winners and losers for WQF
    for i in range(4):
        player1 = wqf_df.at[i, 'Player 1']
        player2 = wqf_df.at[i, 'Player 2']
        win_prob = wqf_df.at[i, 'WinProb']
    
        if random.random() < win_prob:
            wqf_df.at[i, 'Winner'] = player1
            wqf_df.at[i, 'Loser'] = player2
            print(f"{player1} beats {player2} (WQF)")
        else:
            wqf_df.at[i, 'Winner'] = player2
            wqf_df.at[i, 'Loser'] = player1
            print(f"{player2} beats {player1} (WQF)")

    # Combine the DataFrames for Winners Quarterfinals (WQF)
    combined_df = pd.concat([combined_df, wqf_df], ignore_index=True)

    # Prepare for the Loser's matches for 9th place
    losers_wqf = wqf_df['Loser'].tolist()
    winners_losers_13th = losers_13th_df['Winner'].tolist()

    losers_9th_data = {
        'Player 1': winners_losers_13th,
        'Player 2': losers_wqf,
        'WinProb': [0] * 4,
        'Winner': [None] * 4,
        'Loser': [None] * 4
    }

    losers_9th_df = pd.DataFrame(losers_9th_data)

    # Calculate win probabilities for the loser's matches (9th place)
    for index, row in losers_9th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_9th_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches (9th place)
    for index, row in losers_9th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_9th_df.at[index, 'Winner'] = winner
        losers_9th_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (9th)")
        update_placement('9th', loser)

    # Combine the DataFrames for Loser's 9th place matches
    combined_df = pd.concat([combined_df, losers_9th_df], ignore_index=True)

    # Prepare for the Loser's matches for 7th place
    losers_9th_winners = losers_9th_df['Winner'].tolist()

    # Organize the winners to match top vs bottom, etc.
    half_length = len(losers_9th_winners) // 2
    losers_7th_data = {
        'Player 1': losers_9th_winners[:half_length],
        'Player 2': losers_9th_winners[-1:-half_length-1:-1],
        'WinProb': [0] * half_length,
        'Winner': [None] * half_length,
        'Loser': [None] * half_length
    }

    losers_7th_df = pd.DataFrame(losers_7th_data)

    # Calculate win probabilities for the loser's matches (7th place)
    for index, row in losers_7th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            losers_7th_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the loser's matches (7th place)
    for index, row in losers_7th_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        losers_7th_df.at[index, 'Winner'] = winner
        losers_7th_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (7th)")
        update_placement('7th', loser)

    # Combine the DataFrames for Loser's 7th place matches
    combined_df = pd.concat([combined_df, losers_7th_df], ignore_index=True)

    # Prepare for the Winners Semifinals matches
    winners_wsf = wqf_df['Winner'].tolist()

    # Organize the winners to match top vs bottom, etc.
    half_length = len(winners_wsf) // 2
    wsf_data = {
        'Player 1': winners_wsf[:half_length],
        'Player 2': winners_wsf[-1:-half_length-1:-1],
        'WinProb': [0] * half_length,
        'Winner': [None] * half_length,
        'Loser': [None] * half_length
    }

    wsf_df = pd.DataFrame(wsf_data)

    # Calculate win probabilities for the Winners Semifinals matches
    for index, row in wsf_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            wsf_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Winners Semifinals matches
    for index, row in wsf_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        wsf_df.at[index, 'Winner'] = winner
        wsf_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (WSF)")

    # Combine the DataFrames for Winners Semifinals
    combined_df = pd.concat([combined_df, wsf_df], ignore_index=True)

    # Prepare for the Losers Quarterfinals matches (5th place)
    losers_wsf = wsf_df['Loser'].tolist()
    winners_losers_7th = losers_7th_df['Winner'].tolist()

    lqf_data = {
        'Player 1': winners_losers_7th,
        'Player 2': losers_wsf,
        'WinProb': [0] * len(winners_losers_7th),
        'Winner': [None] * len(winners_losers_7th),
        'Loser': [None] * len(winners_losers_7th)
    }

    lqf_df = pd.DataFrame(lqf_data)

    # Calculate win probabilities for the Losers Quarterfinals matches
    for index, row in lqf_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            lqf_df.at[index, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Losers Quarterfinals matches
    for index, row in lqf_df.iterrows():
        player1 = row['Player 1']
        player2 = row['Player 2']
        win_prob = row['WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        lqf_df.at[index, 'Winner'] = winner
        lqf_df.at[index, 'Loser'] = loser
        print(f"{winner} beats {loser} (5th)")
        update_placement('5th', loser)

    # Combine the DataFrames for Losers Quarterfinals
    combined_df = pd.concat([combined_df, lqf_df], ignore_index=True)

    # Prepare for the Losers Semifinals match
    winners_lqf = lqf_df['Winner'].tolist()

    # Since there are only two players, create the DataFrame directly
    lsf_data = {
        'Player 1': [winners_lqf[0]],
        'Player 2': [winners_lqf[1]],
        'WinProb': [0],
        'Winner': [None],
        'Loser': [None]
    }

    lsf_df = pd.DataFrame(lsf_data)

    # Calculate win probability for the Losers Semifinals match
    player1 = lsf_df.at[0, 'Player 1']
    player2 = lsf_df.at[0, 'Player 2']
    try:
        win_prob = win_prob_matrix.at[player1, player2]
        lsf_df.at[0, 'WinProb'] = win_prob
    except KeyError:
        print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Losers Semifinals match
    win_prob = lsf_df.at[0, 'WinProb']
    if random.random() < win_prob:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    lsf_df.at[0, 'Winner'] = winner
    lsf_df.at[0, 'Loser'] = loser
    print(f"{winner} beats {loser} (4th)")
    update_placement('4th', loser)

    # Combine the DataFrames for Losers Semifinals
    combined_df = pd.concat([combined_df, lsf_df], ignore_index=True)

    # Prepare for the Winners Finals match
    winners_wf = wsf_df['Winner'].tolist()

    # Since there are only two players, create the DataFrame directly
    wf_data = {
        'Player 1': [winners_wf[0]],
        'Player 2': [winners_wf[1]],
        'WinProb': [0],
        'Winner': [None],
        'Loser': [None]
    }

    wf_df = pd.DataFrame(wf_data)

    # Calculate win probability for the Winners Finals match
    player1 = wf_df.at[0, 'Player 1']
    player2 = wf_df.at[0, 'Player 2']
    try:
        win_prob = win_prob_matrix.at[player1, player2]
        wf_df.at[0, 'WinProb'] = win_prob
    except KeyError:
        print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Winners Finals match
    win_prob = wf_df.at[0, 'WinProb']
    if random.random() < win_prob:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    wf_df.at[0, 'Winner'] = winner
    wf_df.at[0, 'Loser'] = loser
    print(f"{winner} beats {loser} (WF)")

    # Combine the DataFrames for Winners Finals
    combined_df = pd.concat([combined_df, wf_df], ignore_index=True)

    # Prepare for the Losers Finals match
    losers_lf = lsf_df['Winner'].tolist()
    loser_wf = wf_df['Loser'].tolist()

    # Since there is only one match, create the DataFrame directly
    lf_data = {
        'Player 1': [losers_lf[0]],
        'Player 2': [loser_wf[0]],
        'WinProb': [0],
        'Winner': [None],
        'Loser': [None]
    }

    lf_df = pd.DataFrame(lf_data)

    # Calculate win probability for the Losers Finals match
    player1 = lf_df.at[0, 'Player 1']
    player2 = lf_df.at[0, 'Player 2']
    try:
        win_prob = win_prob_matrix.at[player1, player2]
        lf_df.at[0, 'WinProb'] = win_prob
    except KeyError:
        print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Losers Finals match
    win_prob = lf_df.at[0, 'WinProb']
    if random.random() < win_prob:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    lf_df.at[0, 'Winner'] = winner
    lf_df.at[0, 'Loser'] = loser
    print(f"{winner} beats {loser} (3rd)")
    update_placement('3rd', loser)

    # Combine the DataFrames for Losers Finals
    combined_df = pd.concat([combined_df, lf_df], ignore_index=True)

    # Prepare for the Grand Finals match
    grand_finals = {
        'Player 1': [wf_df.at[0, 'Winner']],  # Winner from Winners Finals
        'Player 2': [lf_df.at[0, 'Winner']],  # Winner from Losers Finals
        'WinProb': [0],
        'Winner': [None],
        'Loser': [None]
    }

    gf_df = pd.DataFrame(grand_finals)

    # Calculate win probability for the Grand Finals match
    player1 = gf_df.at[0, 'Player 1']
    player2 = gf_df.at[0, 'Player 2']
    try:
        win_prob = win_prob_matrix.at[player1, player2]
        gf_df.at[0, 'WinProb'] = win_prob
    except KeyError:
        print(f"Win probability not found for match: {player1} vs {player2}")

    # Simulate the Grand Finals match
    win_prob = gf_df.at[0, 'WinProb']
    if random.random() < win_prob:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    gf_df.at[0, 'Winner'] = winner
    gf_df.at[0, 'Loser'] = loser

    # Check for bracket reset
    if winner == player2:
        print(f"{winner} beats {loser}")
        print("The bracket reset!")
        # Simulate the reset Grand Finals match
        gf_reset_df = pd.DataFrame(grand_finals)  # Reuse the same structure

        # Calculate win probability for the reset Grand Finals match
        try:
            win_prob = win_prob_matrix.at[player1, player2]
            gf_reset_df.at[0, 'WinProb'] = win_prob
        except KeyError:
            print(f"Win probability not found for match: {player1} vs {player2}")

        # Simulate the reset Grand Finals match
        win_prob = gf_reset_df.at[0, 'WinProb']
        if random.random() < win_prob:
            winner, loser = player1, player2
        else:
            winner, loser = player2, player1
        gf_reset_df.at[0, 'Winner'] = winner
        gf_reset_df.at[0, 'Loser'] = loser
        print(f"{winner} beats {loser} (2nd)")
        update_placement('2nd', loser)
        update_placement('1st', winner)

        # Combine the DataFrames for Grand Finals with a reset
        combined_df = pd.concat([combined_df, gf_df, gf_reset_df], ignore_index=True)
    else:
        print(f"{winner} beats {loser}")
        print("No bracket reset")
        update_placement('2nd', loser)
        update_placement('1st', winner)
        # Combine the DataFrames for Grand Finals without a reset
        combined_df = pd.concat([combined_df, gf_df], ignore_index=True)

    # Convert placements to DataFrame
    placements_df = pd.DataFrame({k: '\n'.join(v) for k, v in placements.items()}, index=[0])
    placements_df = placements_df.T.reset_index()
    placements_df.columns = ['Placement', 'Players']

    return combined_df, placements_df

# Number of simulations to run
num_simulations = 1000

# List to store results of each simulation
simulation_results = []
placement_results = []

for i in range(num_simulations):
    combined_df, placements_df = run_tournament_simulation(win_prob_matrix, seeded_players)
    simulation_results.append(combined_df)
    placement_results.append(placements_df)

# Save each simulation result to a CSV file
for i, (combined_df, placements_df) in enumerate(zip(simulation_results, placement_results)):
    combined_df.to_csv(f'simulation_result_{i+1}.csv', index=False)
    placements_df.to_csv(f'placements_result_{i+1}.csv', index=False)
