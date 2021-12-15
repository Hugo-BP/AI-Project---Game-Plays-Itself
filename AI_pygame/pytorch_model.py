import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import warnings


# FEED FORWARD NEURAL NET
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # 2 Layer FeedForward network
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    # pass tensor through net
    def forward(self, tensor):
        tensor = F.relu(self.linear1(tensor))
        tensor = self.linear2(tensor)

        return tensor

    # save model
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


# NET TRAIN FUNCTION
class QTrainer:
    def __init__(self, model, lr, gamma):
        # Default settings
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    # this is called by long and short train(), it will receive either tuples or lists, but not a mix of them.
    def train_step(self, curr_state, new_state, agent_action, reward, alive):
        warnings.filterwarnings("ignore")
        # can have multiple values per each input
        curr_state = torch.tensor(curr_state, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)
        agent_action = torch.tensor(agent_action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # if there is only 1 value per input, flatten tensor to size 1
        if len(curr_state.shape) == 1:
            curr_state = torch.unsqueeze(curr_state, 0)
            new_state = torch.unsqueeze(new_state, 0)
            agent_action = torch.unsqueeze(agent_action, 0)
            reward = torch.unsqueeze(reward, 0)

            # convert alive boolean into a tuple
            alive = (alive,)

        # AI PREDICTION:    <--------------
        # 1: predict Q values with current state
        prediction = self.model(curr_state)

        # 2: predict Q_new with formula while still playing:
        # Q_new = r + y * max(next_predicted Q value)
        # prediction.clone() to have 4 values
        target = prediction.clone()
        for idx in range(len(alive)):
            # Q_new = reward of current index
            Q_new = reward[idx]
            # while not done with session, apply formula
            if alive[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(new_state[idx]))

            # predictions[argmax(action)] = Q_new
            target[idx][torch.argmax(agent_action[idx]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        self.optimizer.step()
