Uses open_clip huggingface model to calculate the amount of calories in an 
food image taken by an arduino camera connected to the computer.

To use the program, run dash.py
A window will pop up in your browser displaying the calorie information. (there will be no information initially)
After you have connected your computer with an arduino camera, you can use the button on the screen to take a picture,
and the calorie information of the image taken will be displayed after calcuation.

Note: Due to limitations of the calorie clip model from huggingface, the information displayed has a large error bound.
The first time running the program might take a while to load on the web, sometimes rerunning the program will help.
