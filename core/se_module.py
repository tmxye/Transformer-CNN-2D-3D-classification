from torch import nn


class SELayer(nn.Module):
    def __init__(self, channel, reduction=16):
        assert channel > reduction, "Make sure your input channel bigger than reduction which equals to {}".format(reduction)
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
                nn.Linear(channel, channel // reduction),
                nn.ReLU(inplace=True),
                nn.Linear(channel // reduction, channel),
                nn.Sigmoid()
        )

    def forward(self, x):
        x = x.cuda()
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        # print("y", y.shape)     # ([1, 64])
        y = self.fc(y).view(b, c, 1, 1)
        return x * y
