import torch
from torch.legacy import nn

class CMulTable(nn.Module):

    def __init__(self, ):
        super(CMulTable, self).__init__()
        self.gradInput = []

    def updateOutput(self, input):
        self.output.resizeAs_(input[0]).copy(input[0])
        for i in range(1, len(input)):
            self.output.mul_(input[i])

        return self.output

    def updateGradInput_efficient(self, input, gradOutput):
        self.tout = self.tout or input[0].new()
        self.tout.resizeAs_(self.output)
        for i in range(len(input)):
            if len(self.gradInput) <= i:
                assert i == len(self.gradInput)
                self.gradInput.append(input[0].new())
            self.gradInput[i].resizeAs_(input[i]).copy(gradOutput)
            self.tout.copy(self.output).div_(input[i])
            self.gradInput[i].mul_(self.tout)

        self.gradInput = self.gradInput[:len(input)]
        return self.gradInput

    def updateGradInput(self, input, gradOutput):
        for i in range(len(input)):
            if len(self.gradInput) <= i:
                assert i == len(self.gradInput)
                self.gradInput.append(input[0].new())
            self.gradInput[i].resizeAs_(input[i]).copy(gradOutput)
            for j in range(len(input)):
                if i != j:
                    self.gradInput[i].mul_(input[j])

        self.gradInput = self.gradInput[:len(input)]
        return self.gradInput

    def clearState(self):
        nn.utils.clear(self, 'tout')
        return super(CMulTable, self).clearState()