Neuroptimus tutorial
==================

Target data tab
-------

After the program started, the first tab will appear where the user can select the file containing the target data. The user must specify the path to this file, and the working directory (base directory)
where the outputs will be written. Apart from these the user must input the requested parameters of the
trace set they want to use. After loading the selected file, the user can check if the traces were loaded
properly with the help of a plot which displays all the traces concatenated and with the help of a tree
display. The concatenation is performed only for displaying purposes, the traces are otherwise handled
separately. The program only handles one input file (loading a new file will overwrite the existing one),
but with an arbitrary number of traces.


.. figure:: um001.png
   :align: center

=       ========================================= 
A    	Path to input data.
B	Select the location of the input data.
C	Indicates whether the input file also contains time.
D	Type of input (voltage, current trace or features).
E	Path to base directory (resulting files will be
 	stored here).
F	Select the base location.
G	Number of traces in file (trace set).
H	Units of the data.
I	Length of trace(s). (in case of multiple traces, they
 	must have the same length)
J	Sampling frequency (in case of multiple traces,
 	it must be the same for all).
K	Loads the target data from the given file.
L	Input tree
M	Displays the loaded trace (if given file contains 
 	more, the trace will be concatenated for
 	displaying).

=       ========================================= 


Model tab
-------

On the Model tab the user can specify the simulator which can be Neuron or external.
If Neuron is used as the simulator then the model file must contain only the necessary
structure and mechanisms (without any graphical interface or runtime modification). The model can be loaded after selecting the model file and the
special folder where the necessary .mod files are located (optional).
As Neuron cannot load external mechanisms after startup, if the special files were not found, the software must be
restarted. Once the model is loaded successfully, the content of the model will be displayed, and the
user can choose the parameters to be optimized by selecting them from the list and pressing the “set” button. Removing a
parameter can be performed in a similar fashion.
Alternatively, instead of choosing parameters from the list, the user can load or create a special python function which defines high level parameters to be optimized and maps them onto actual model parameters. See example for user function in test cases 2, 3 and 6.

.. figure:: um003.png
   :align: center

=       ========================================= 
A         Simulator type selection (Neuron or external)
B         Path to model file.
C         Select the model file.
D         Loads the specified model.
E         Path to special files (the compiled mod files for
          Neuron). This should point to a folder that
          contains a subfolder with the compiled files (e.g.: to a
          folder which has an x86-64 subdirectory)
F         Select special file location.
G        Displays the recognized parameters. These can be
         selected for optimization. If the parameters you
         need are missing, you can create a user-defined
         function.
H        Opens the window to define/load your own
         function for the optimization.
I        Adds the currently selected parameter to the list of
         parameters subject to optimization.
J        Removes the parameter from the aforementioned list.
=       ========================================= 


Choosing External as the simulator allows the user to call an arbitrary executable file to perform the simulations. 

.. figure:: um004.png
   :align: center

=       ========================================= 
A         Here you can give the command which runs the model in an
          external simulator.
B         The number of parameters subject to optimization
=       =========================================        


Settings tab
-------

The Settings tab defines the stimulation and recording protocol for the simulations. The user can select the
stimulation protocol which can be either current clamp or voltage clamp (the voltage clamp is
implemented as a SEClamp from Neuron). The stimulus type can also be selected, and can either be a step protocol
or a custom waveform. If the step protocol is selected the properties of the step can be specified. See example for custom waveform in test case 3.
In case of multiple stimuli, only the amplitude of the stimuli can vary, no other parameter (position of stimulus, duration, delay, etc) can be changed. 
The user can make use of external files here as well by selecting the custom waveform as stimulus
type. After the stimulation parameters are selected, the user must choose a section and a position inside
that section to stimulate the model.
In the second column the parameters regarding the simulation and the recording process can be given.
The user must give an initial voltage parameter, the length of the simulation and the integration step
used for calculations (variable time step methods are not supported yet). After these settings are done,
the user can select the parameter to be measured (either current or voltage), the section and the position
where the measurement takes place.

.. figure:: um006.png
   :align: center

=     ======================================
A     Stimulation protocol (Vclamp or Iclamp).
B     Type of the stimulus (Step protocol or Custom
      Waveform).
C     Opens the window for specifying step amplitudes
      or loading custom waveform (depending on the previous options).
D     Delay of stimulus onset.
E     Duration of stimulus.
F     Section which receives stimulus.
G     Location of stimulation inside the section.
H     The parameter to be recorded.
I     The section where the recordings take place.
J     Location inside the recording section. 
K     Initial membrane potential.
L     Length of the recording.
M     Integration step size.

=     ======================================

Fitness tab
-------

On the Fitness tab the combination of fitness functions (error functions / objective functions / cost functions) can be selected with the desired weights.
Weights can be normalized so that they sum to 1, but this is optional. The user can fine tune the behavior of the functions by giving parameters to them
(the value of the same parameter should be the same across the functions).

.. figure:: um008.png
   :align: center

=     ==================================
A     List of available fitness functions and weights assigned to the selected functions.
B     Normalizes the weights (optional).
C     Spike detection treshold passed to the fitness functions.
D     Spike window time passed to the fitness functions.
=     ==================================

Run tab
-------

On the Run tab, the user can select the desired algorithm from the lists that appear under tabs corresponding to the various optimization packages and set parameters of the selected algorithm. The program also requires
boundaries for the parameters.

.. figure:: um009.png
   :align: center

=     ========================================
A     Avaiable algorithms (grouped by package)
B     Boundaries of the parameters subject to optimization.
C     Parameters of the
      selected optimization algorithm.
D     Perform a single evaluation for a specific parameter set.      
E     Run the optimization.
=     ========================================

Results tab
-------

The Results tab shows the parameters and fitness value(s) of the best evaluation. The figure visualizes the trace of the best-fitting model and compares it the target trace (when available).

.. figure:: um011.png
   :align: center

=     ===========================================
A     The resulting parameters.
B     The trace(s) obtained with the resulting
      parameters.
=     ===========================================

Statistics tab
-------

This final tab displays some additional statistics for the final population and allows the user to view time evolution of the fitness statistics across generations.

.. figure:: um012.png
   :align: center

=     =============================================
A     The resulting parameters.

B     Fitness statistics


C     Fitness components: name of fitness function; fitness value;calculated by the function; weight assigned to the function; the weighted fitness value; the resulting cumulated fitness value.

D     Displays the progression of the fitness statistics of the population through the generations.
=     =============================================

Other windows
------------------------

User function window

.. figure:: um014.png
   :align: center

=     ===============================================
A     Entry field for function definition.
B     Load a previously defined function from a txt.
C     Done editing, save function and continue.
D     Discard function and go back.
=     ===============================================

Stimuli window

First the user must select the number of stimuli and press the Create button. Next the amplitude of each step must be given.



.. figure:: um015.png
   :align: center

=     ===============================================
A     Number of stimuli.
B     Create the specified number of stimuli.
C     Specify the amplitude of the stimuli.
=     ===============================================

Boundary window

The user can either set lower and upper bounds explicitly or load these values from a previously saved file.

.. figure:: um016.png
   :align: center

=     ===============================================
A     The list of selected parameters.
B     Lower bounds.
C     Upper bounds.
D     Boundaries are set, continue.
E     Save boundaries to file.
F     Load boundaries from file.
=     ===============================================
