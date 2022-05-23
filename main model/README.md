# Main model
 This small project seeks to study the effect of normalization in V1 neurons
 
 In this exercise, we simulated V1 neurons in a uniform-grid set up.
 We also implemented a Macro-micro grid set up, which is also the Neuron grid in the codes.
 
 Then, we produced the animated simulation w.r.t. to a point stimulus at the center of the uniform-grid.
 
 ## File functions
 
 To get a new simulation: run **Model_Main.py**
 
 **Model_Main.py** requires **InitializationTimeMd.py** to initialize;
 
 **InitializationTimeMd.py** reuires **NeuronGrid.py** and **ModelUtil.py** to provide instruction for computations.
 
 Other necessary files:

 **NrnResponse.py** returns the response of a neuron w.r.t. a point stimulus
 
 **TuningCurves.py** provides the receptive field for a neuron to generate a response
 
 **NSclasses.py** provides the basic data structured to pack neuron and stimulus objects
 
 **Test_Radius.py** aims to find the largest viable connectivity radius in the Neuron grid for a consistent post-normalization response distribution 
 

 
 
 
