import numpy as np
from Simulator.stats import COST
from Simulator.origin_class import team_traits, game_comp_tiers


# Includes the vector of the shop, bench, board, and item list.
# Add a vector for each player composition makeup at the start of the round.
# action vector = [Decision, shop, champion_bench, item_bench, x_axis, y_axis, x_axis 2, y_axis 2]
class Observation:
    def __init__(self):
        self.shop_vector = np.zeros(45)
        self.game_comp_vector = np.zeros(208)

    def observation(self, player, buffer, action_vector):
        shop_vector = self.shop_vector
        game_state_vector = self.game_comp_vector
        complete_game_state_vector = np.concatenate([np.expand_dims(shop_vector, axis=0),
                                                     np.expand_dims(player.board_vector, axis=0),
                                                     np.expand_dims(player.bench_vector, axis=0),
                                                     np.expand_dims(player.chosen_vector, axis=0),
                                                     np.expand_dims(player.item_vector, axis=0),
                                                     np.expand_dims(player.player_vector, axis=0),
                                                     np.expand_dims(game_state_vector, axis=0),
                                                     np.expand_dims(action_vector, axis=0), ], axis=-1)
        i = 0
        input_vector = complete_game_state_vector
        while i < buffer.len_observation_buffer() and i < 0:
            i += 1
            input_vector = np.concatenate([input_vector, buffer.get_prev_observation(i)], axis=-1)

        while i < 0:
            i += 1
            input_vector = np.concatenate([input_vector, np.zeros(buffer.get_observation_shape())], axis=-1)
        # std = np.std(input_vector)
        # if std == 0:
        # input_vector = input_vector - np.mean(input_vector)
        # else:
        #     input_vector = (input_vector - np.mean(input_vector)) / std
        # print(input_vector.shape)
        return input_vector, complete_game_state_vector

    def dummy_observation(self, buffer):
        input_vector = buffer.get_prev_observation(0)
        i = 0
        while i < buffer.len_observation_buffer() and i < 0:
            i += 1
            input_vector = np.concatenate([input_vector, buffer.get_prev_observation(i)], axis=-1)

        while i < 0:
            i += 1
            input_vector = np.concatenate([input_vector, np.zeros(buffer.get_observation_shape())], axis=-1)

        return input_vector

    def generate_game_comps_vector(self):
        output = np.zeros(208)
        for i in range(len(game_comp_tiers)):
            tiers = np.array(list(game_comp_tiers[i].values()))
            tierMax = np.max(tiers)
            if tierMax != 0:
                tiers = tiers / tierMax
            output[i * 26: i * 26 + 26] = tiers
        self.game_comp_vector = output

    def generate_shop_vector(self, shop):
        # each champion has 6 bit for the name, 1 bit for the chosen.
        # 5 of them makes it 35.
        output_array = np.zeros(45)
        shop_chosen = False
        chosen_shop_index = -1
        chosen_shop = ''
        for x in range(0, len(shop)):
            input_array = np.zeros(8)
            if shop[x]:
                chosen = 0
                if shop[x].endswith("_c"):
                    chosen_shop_index = x
                    chosen_shop = shop[x]
                    c_shop = shop[x].split('_')
                    shop[x] = c_shop[0]
                    chosen = 1
                    shop_chosen = c_shop[1]
                i_index = list(COST.keys()).index(shop[x])
                # This should update the item name section of the vector
                for z in range(6, 0, -1):
                    if i_index > 2 ** (z - 1):
                        input_array[6 - z] = 1
                        i_index -= 2 ** (z - 1)
                input_array[7] = chosen
            # Input chosen mechanics once I go back and update the chosen mechanics.
            output_array[8 * x: 8 * (x + 1)] = input_array
        if shop_chosen:
            if shop_chosen == 'the':
                shop_chosen = 'the_boss'
            i_index = list(team_traits.keys()).index(shop_chosen)
            # This should update the item name section of the vector
            for z in range(5, 0, -1):
                if i_index > 2 * z:
                    output_array[45 - z] = 1
                    i_index -= 2 * z
            shop[chosen_shop_index] = chosen_shop
        self.shop_vector = output_array
