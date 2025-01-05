from torch.autograd import Variable
from torch import nn, load, cuda

from torchvision import transforms
from torchvision import models

from PIL import Image
import numpy as np




class Validator:
    def __init__(self, path_to_model):
        self.model = models.resnet50()
        self.model.fc = nn.Sequential(nn.Linear(2048, 512),
                                        nn.ReLU(),
                                        nn.Dropout(0.2),
                                        nn.Linear(512, 10),
                                        nn.LogSoftmax(dim=1))
        
        if cuda.is_available():
            self.model.load_state_dict(load(path_to_model))
        else:
            self.model.load_state_dict(load(path_to_model, map_location='cpu'))
        self.model.eval()



    # Как выглядит модель
    def about_model(self):
        print(self.model)



    # Загружаем изображение, которое будем проверять
    def __get_image(self, image_path):
        test_transforms = transforms.Compose(
            [
                transforms.Resize(224),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ]
        )

        image = Image.open(image_path)
        image_tensor = test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)

        if cuda.is_available():
            image_tensor.cuda()

        return image_tensor




    class_names = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    def isNSFW(self, image_path):
        data = self.__get_image(image_path)

        input = Variable(data)
        output = self.model(input)
        #index = output.data.numpy().argmax()
        if cuda.is_available():
            index = output.detach().numpy().argmax()
        else:
            index = output.detach().cpu().numpy().argmax()

        return not (index == 0 or index == 2)
    

    def isJPG(self, image_path):
        return image_path[-3:] == "jpg"
        



# "ТЕСТЫ"
# validator = Validator("pretrained_models\\ResNet50_nsfw_model.pth")

# while(True):
#     print("\n Choose image")

#     image = "images\\" + input()

#     correct_ext = validator.isJPG(image)

#     if correct_ext:
#         nsfw_check = "nsfw" if validator.isNSFW(image) else "sfw"
#         print(nsfw_check)
#     else:
#         print("Error: incorrect extention")
    



