import os
model_list = os.listdir("models/train-version-RFB/" + args.modelid)
lossdict = {}
for model in model_list:
    if(model[-3:] != "pth"):
        continue
    loss = model.split('-')[4][:-4]
    lossdict[loss] = model
print(lossdict[min(lossdict.keys())])