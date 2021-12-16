import torch
import numpy

from game_session_class import *
from collections import deque
from pytorch_model import Linear_QNet, QTrainer

MAX_MEMORY = 500_000
BATCH_SIZE = 1000  # 1000
LEARN_RATE = 0.0001  # 0.001
MAX_PADDING = 50

HIDDEN_LAYER_SIZE = 666  # 256
INPUT_LAYER_SIZE = MAX_PADDING*26 + 18
OUTPUT_SIZE = 4

class Agent:
    def __init__(self, game_session, player):
        # game variables
        self.game_session = game_session
        self.player = player
        self.is_playing = True

        # AI variables
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate, must be less than 1
        self.memory = deque(maxlen=MAX_MEMORY)

        # input_size --> size of state[] = MAX_PADDING*X (X = interest bools) + 18 (other state bools such as is_fighting or direction)
        # output_size --> size of possibilities[] = 4
        # hidden_size --> can change values TODO try different values
        self.model = Linear_QNet(INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, lr=LEARN_RATE, gamma=self.gamma)

        # score statistics
        self.total_games_played = 0
        self.individual_high_score = 0
        self.individual_all_score = []

    # ALL BOOLEAN VALS
    def get_state(self):
        # DIRECTION
        agent_dir = self.player.direction
        dir_l = agent_dir == 0  # A
        dir_r = agent_dir == 1  # D
        dir_u = agent_dir == 2  # W
        dir_d = agent_dir == 3  # S

        # TUPLES
        next_step_l = (self.player.rect.x - TILE_SIZE, self.player.rect.y)
        next_step_r = (self.player.rect.x + TILE_SIZE, self.player.rect.y)
        next_step_u = (self.player.rect.x, self.player.rect.y - TILE_SIZE)
        next_step_d = (self.player.rect.x, self.player.rect.y + TILE_SIZE)

        is_blockedL = False
        is_blockedR = False
        is_blockedU = False
        is_blockedD = False

        if self.player.check_boundaries(next_step_l):
            is_blockedL = True
        if self.player.check_boundaries(next_step_r):
            is_blockedR = True
        if self.player.check_boundaries(next_step_u):
            is_blockedU = True
        if self.player.check_boundaries(next_step_d):
            is_blockedD = True

        # DANGER
        agent_health = self.player.health
        agent_max_health = self.player.max_health
        agent_remaining_health = (agent_health * 100) / agent_max_health
        low_health = False
        full_health = False
        # If agent health bellow 33%
        if agent_remaining_health < 33:
            low_health = True
        if agent_health == agent_max_health:
            full_health = True

        # STATUS
        is_healer = self.player.is_healer
        is_fighting = self.player.is_fighting
        """
        is_blockedL = self.player.is_blockedL
        is_blockedR = self.player.is_blockedR
        is_blockedU = self.player.is_blockedU
        is_blockedD = self.player.is_blockedD
        """
        is_alive = self.player.is_alive

        state = [
            is_alive,

            # block location
            is_blockedL,
            is_blockedR,
            is_blockedU,
            is_blockedD,

            # cant go there because of block
            (dir_r and is_blockedR) or (dir_l and is_blockedL) or (dir_u and is_blockedU) or (dir_d and is_blockedD),
            (dir_r and is_blockedD) or (dir_l and is_blockedR) or (dir_u and is_blockedL) or (dir_d and is_blockedU),
            (dir_r and is_blockedU) or (dir_l and is_blockedD) or (dir_u and is_blockedR) or (dir_d and is_blockedL),
            (dir_r and is_blockedL) or (dir_l and is_blockedU) or (dir_u and is_blockedD) or (dir_d and is_blockedR),

            # movement dir
            dir_r,
            dir_l,
            dir_u,
            dir_d,

            # status
            low_health,
            full_health,
            is_fighting,
            is_healer,

            # Interests
            # ...
        ]

        # FIELD OF VIEW - INTERESTS
        has_interest = False

        # if not empty then add interests
        if self.player.places_of_interest:
            has_interest = True
            state.append(has_interest)

            for interest in self.player.places_of_interest:
                state.append(interest.x < self.player.rect.x)  # interest left
                state.append(interest.x > self.player.rect.x)  # interest right
                state.append(interest.y < self.player.rect.y)  # interest up
                state.append(interest.y > self.player.rect.y)  # interest down
                # interest type
                # player
                state.append(interest.is_player)
                if interest.is_player:
                    agent_health = interest.health
                    agent_max_health = interest.max_health
                    agent_remaining_health = (agent_health * 100) / agent_max_health
                    low_health = False
                    full_health = False
                    # If agent health bellow 33%
                    if agent_remaining_health < 33:
                        low_health = True
                    if agent_health == agent_max_health:
                        full_health = True
                    state.append(low_health)
                    state.append(full_health)
                else:
                    state.append(False)
                    state.append(False)

                # enemy
                state.append(interest.sprite_class == 'slime')
                state.append(interest.sprite_class == 'beast')
                state.append(interest.sprite_class == 'zombie')
                state.append(interest.sprite_class == 'ghost')
                state.append(interest.sprite_class == 'necromancer')
                # friend
                state.append(interest.sprite_class == 'villager')
                state.append(interest.sprite_class == 'gnome')
                state.append(interest.sprite_class == 'faery')
                state.append(interest.sprite_class == 'demon')
                # building
                state.append(interest.sprite_class == 'house')
                state.append(interest.sprite_class == 'cave')
                state.append(interest.sprite_class == 'stone_cross')
                state.append(interest.sprite_class == 'faery_house')
                state.append(interest.sprite_class == 'castle')
                state.append(interest.sprite_class == 'evil_castle')
                state.append(interest.sprite_class == 'necro_house')
                state.append(interest.sprite_class == 'bridge')
                state.append(interest.sprite_class == 'broken_bridge')
                state.append(interest.sprite_class == 'cactus')

                #state.append(interest.is_player)
                #state.append(interest.is_enemy)
                #state.append(interest.is_building)
                #state.append(interest.is_bonus)
            # PADDING SO TENSORS ARE ALL SAME SIZE = 50 places
            for i in range(MAX_PADDING - len(self.player.places_of_interest)):
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)

                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)


        else:
            print(self.player.name + ' interest in nothing ')
            # no places of interest within range of view
            state.append(has_interest)
            # PADDING SO TENSORS ARE ALL SAME SIZE = 50 places
            for i in range(MAX_PADDING):
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)

                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)
                state.append(False)

        # RETURN BOOLS AS binary INTs
        return numpy.array(state, dtype=int)

    def get_action(self, state):
        possibilities = [0, 1, 2, 3]  # [A, D, W, S]
        # either make a RANDOM MOVE or PREDICT MOVE
        # the more games played the less likely a move is to be random
        self.epsilon = 80 - self.total_games_played

        if random.randint(0, 100) < self.epsilon:
            # random moves: exploration vs exploitation tradeoff
            choice = random.choices([0, 1, 2, 3], weights=(25, 25, 25, 25), k=1)
            action = possibilities[choice[0]]
        else:
            state = torch.tensor(state, dtype=torch.float)
            # >> self.model(state) calls Linear_QNet.forward(state)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            action = possibilities[move]

        return action

    def memorize(self, curr_state, new_state, agent_action, reward, alive):
        self.memory.append((curr_state, new_state, agent_action, reward, alive))

    def train_mem_short_term(self, curr_state, new_state, agent_action, reward, alive):
        self.trainer.train_step(curr_state, new_state, agent_action, reward, alive)
        pass

    def train_mem_long_term(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        # GET STATES FROM MEMORY - These are lists
        curr_state, new_state, agent_action, reward, alive = zip(*mini_sample)

        # TRAIN
        self.trainer.train_step(curr_state, new_state, agent_action, reward, alive)



# update individual statistics
def ind_stats_update(agent):
    # INDIVIDUAL
    agent.total_games_played += 1
    if agent.player.individual_score > agent.individual_high_score:
        agent.individual_high_score = agent.player.individual_score
    agent.individual_all_score.append(agent.player.individual_score)



def run_ai():
    total_games_played = 0
    all_total_scores = []
    high_score = 0

    number_of_agents = 1  # TODO test this with several agents

    # start first session
    game_session = GameSession(number_of_agents)
    players = game_session.new_game()
    # init agents
    agents = []

    for i in range(number_of_agents):
        agents.append(Agent(game_session, players[i]))

    while game_session.running:
        # current game session
        game_session.run_game()

        for agent in agents:
            # only update agent if its still playing
            if agent.player.is_alive:
                # get agent player status
                curr_state = agent.get_state()

                # decide on action
                agent_action = agent.get_action(curr_state)

                # apply action and get rewards from it
                agent.player.player_movement(agent_action)
                reward = agent.player.current_action_reward

                # set agent player status
                new_state = agent.get_state()

                # short term training
                agent.train_mem_short_term(curr_state, new_state, agent_action, reward, agent.player.is_alive)

                # memorize action context
                agent.memorize(curr_state, new_state, agent_action, reward, agent.player.is_alive)

        # GAME OVER
        if not game_session.running:
            # OVERRAL STATS & AGENT MODEL SAVE
            if game_session.total_score > high_score:
                high_score = game_session.total_score
                for agent in agents:
                    agent.model.save()
            all_total_scores.append(game_session.total_score)
            total_games_played += 1
            print('\n\nTOTAL GAMES: ' + str(total_games_played) + ' BEST SCORE: ' + str(high_score) + '\n\n')

            # INDIVIDUAL AGENT STATS
            for agent in agents:
                ind_stats_update(agent)
                # long term training
                agent.train_mem_long_term()

            # start new game session
            game_session = GameSession(number_of_agents)
            players = game_session.new_game()

            # assign new session to agents
            i = 0
            for agent in agents:
                agent.game_session = game_session
                agent.player = players[i]
                agent.is_playing = True
                i += 1




run_ai()
