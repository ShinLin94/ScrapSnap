# import torch
# import open_clip
from PIL import Image
# import os
# print(os.listdir())

from PIL import Image

def estimate_calories(image_path):
    clip, head, preprocess = load_model()  # ✅ cached

    img = preprocess(Image.open(image_path)).unsqueeze(0)

    with torch.no_grad():
        features = clip.encode_image(img)
        calories = head(features).item()

    return int(calories)


# def estimate_calories(image_path):

#     img = Image.open(image_path)
#     img.show()  # display the image

#     # Load CLIP
#     clip, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
#     checkpoint = torch.load('calorie_clip.pt', map_location='cpu', weights_only=False)
#     clip.load_state_dict(checkpoint['clip_state'], strict=False)

#     # Load regression head
#     import torch.nn as nn
#     class RegressionHead(nn.Module):
#         def __init__(self):
#             super().__init__()
#             self.net = nn.Sequential(
#                 nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.4),
#                 nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.3),
#                 nn.Linear(256, 64), nn.ReLU(), nn.Linear(64, 1)
#             )
#         def forward(self, x): return self.net(x)

#     head = RegressionHead()
#     head.load_state_dict(checkpoint['regressor_state'])
#     clip.eval(); head.eval()

#     # Predict
#     img = preprocess(Image.open(image_path)).unsqueeze(0)
#     with torch.no_grad():
#         features = clip.encode_image(img)
#         calories = head(features).item()
#     print(f"{calories:.0f} calories")

#     return calories