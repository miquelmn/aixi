import torch
from torch import nn


class Net(nn.Module):
    def __init__(self, numChannels, classes, do_sigmoid: bool = False):
        # call the parent constructor
        super().__init__()

        self.conv1 = nn.Conv2d(
            in_channels=numChannels, out_channels=25, kernel_size=(3, 3), padding="same"
        )
        self.relu1 = nn.ReLU()
        self.bn1 = nn.BatchNorm2d(25)
        self.maxpool1 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv2 = nn.Conv2d(
            in_channels=25, out_channels=35, kernel_size=(3, 3), padding="same"
        )
        self.relu2 = nn.ReLU()
        self.bn2 = nn.BatchNorm2d(35)
        self.maxpool2 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv3 = nn.Conv2d(
            in_channels=35, out_channels=50, kernel_size=(3, 3), padding="same"
        )
        self.relu3 = nn.ReLU()
        self.bn3 = nn.BatchNorm2d(50)
        self.maxpool3 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv4 = nn.Conv2d(
            in_channels=50, out_channels=75, kernel_size=(3, 3), padding="same"
        )
        self.relu4 = nn.ReLU()
        self.bn4 = nn.BatchNorm2d(75)
        self.maxpool4 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv5 = nn.Conv2d(
            in_channels=75, out_channels=125, kernel_size=(3, 3), padding="same"
        )
        self.relu5 = nn.ReLU()
        self.bn5 = nn.BatchNorm2d(125)
        self.maxpool5 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.fc1 = nn.Linear(in_features=4 * 4 * 125, out_features=500)  # 50
        self.dropout1 = nn.Dropout(p=0.2)
        self.relu6 = nn.ReLU()

        self.fc2 = nn.Linear(in_features=500, out_features=250)
        self.dropout2 = nn.Dropout(p=0.2)
        self.relu7 = nn.ReLU()

        self.fc3 = nn.Linear(in_features=250, out_features=50)
        self.dropout3 = nn.Dropout(p=0.2)
        self.relu8 = nn.ReLU()

        self.fc4 = nn.Linear(in_features=50, out_features=classes)

        self._do_simgoid = do_sigmoid

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        x = self.conv3(x)
        x = self.relu3(x)
        x = self.bn3(x)
        x = self.maxpool3(x)

        x = self.conv4(x)
        x = self.relu4(x)
        x = self.bn4(x)
        x = self.maxpool4(x)

        x = self.conv5(x)
        x = self.relu5(x)
        x = self.bn5(x)
        x = self.maxpool5(x)

        x = torch.flatten(x, 1)

        x = self.fc1(x)
        x = self.dropout1(x)
        x = self.relu6(x)

        x = self.fc2(x)
        x = self.dropout2(x)
        x = self.relu7(x)

        x = self.fc3(x)
        x = self.dropout3(x)
        x = self.relu8(x)

        return self._end(x)

    def _end(self, x):
        x = self.fc4(x)

        if self._do_simgoid:
            x = self.sigmoid(x)

        return x


class OOD_Net(Net):
    def __init__(self, classes, in_features, *args, **kwargs):
        super().__init__(classes=classes, *args, **kwargs)

        self.h = nn.Linear(in_features=in_features, out_features=classes, bias=False)
        self.g_fc = nn.Linear(in_features=in_features, out_features=1)
        self.g_bn = nn.BatchNorm2d(1)
        self.g_sigmoid = nn.Sigmoid()

    def _end(self, x):
        h = self.h(x)

        g = self.g_fc(x)
        g = self.g_bn(g)
        g = torch.square(g)
        g = self.g_sigmoid(g)

        return super()._end(h / g)
