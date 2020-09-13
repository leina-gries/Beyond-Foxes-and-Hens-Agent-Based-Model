# Beyond Foxes and Hens: README
This program is designed to model a variety of realistic ecosystems based off of parameters given by the user. 
In order to modify the parameters by which the model will be excecuted, modify the file "procedures.py" to match your desired parameters. Instructions for doing so, and for adding more species, can be found in this file. Species and the number of plants will be added or modified in the main function, plant parameters are modified in make_plants, weather is modified in make_weather, and habitat specifics are set in create_habitat. The program is currently set to run a five species model. The behavior of this system varies immensely based on random elements, but this system can create a stable ecosystem. 

In order to run this program, both "procedures.py" and "ecosystem_classes.py" are necessary. The former calls the classes and creates time, and the latter defines the classes and the methods of the species, weather, plants, and habitat objects. It is set up this way for ease of use, and to allow methods to be viewed side by side with the procedures that manipulate them. 

This program is available to be used freely- it is designed to be used as a research aid for biologists and students. For research purposes, you may modify this code as you like- whether it be the parameters or the methods. However, please do properly cite any data or charts that are sourced from this code. If you want to use any section of this code in your own, please contact Leina Gries to discuss this. Similarly, with any questions about usage, suggestions for improvements, or other comments, please reach out to the author. 

Thank you for reading! I hope this program can be helpful to you. 
