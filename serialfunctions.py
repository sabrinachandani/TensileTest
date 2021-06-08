
#Don't rename!!! otherwise interface file will
#not be able to find any of the functions

#File contains all the functions for the backend of GUI

import serial
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def set_controlling_var(serialcom):
    """Sends 1 to micrcontroller"""

    serialcom.write('1\r'.encode('utf-8'))  #writes to board using pyserial
    sleep(6)                                #sleep to match with HAL_Delay(500) on micro


def write_to_board(serialcom, varlist):
    """writes list of variables to microcontroller"""

    for var in varlist:
        variable = str(var) + '\r'          #attach EOL char
        serialcom.write(variable.encode('utf-8'))
        sleep(2)



def read_from_board(serialcom):
    """Reads data ouput and seperates into three arrays.

    Uses serial to read and decode the output from the MCU. Assumes
    output has each datapoint seperated by an EOL charater, and that
    each line has the structrue 'references, positions, current'
    """

    data_str = []
    finishing_point = "END OF DATA READOUT"
    references = []                         #initialise data arrays
    positions = []
    current = []
    gap = []
    while serialcom.is_open:
        new_line = (serialcom.readline()).decode('utf-8')   #reads data seperated by EOL char
        data_str.append(new_line)                           #append to array
        print(new_line)                                     #print to give user indication test is running
        if finishing_point in new_line:
            serialcom.close()                               #close port when test finished
            for datapoint in data_str[2:-1]:                #ignores first 2 and last lines of readout (not values)
                points = datapoint.split(',')               #split datapoints by ,
                references.append(float(points[0]))
                positions.append(float(points[1]))
                current.append(float(points[2]))
    return references, positions, current

def plot_stress_strain(references, positions, current, length, diameter):
    """Takes output from MCU and calculates stress and strain values.

    Currently doesn't use user input for length and diameter,  but
    just uncomment the l0 and A code (and delete exsisitng).
    """

    d_ball = 0.004                                          #initialise constants
    F0 = 6.13*10**6
    #F0 = F0*(d_ball/0.004)**3
    g0 = 0.002258 #in meters
    #define specimin size - this should really be set from user input (uncomment code)
    t = 0.0003 #thickness
    w = 0.0005 #width
    l0 = 0.015 #l0 = length*10**(-3) convert to meters

    A = 0.001*0.001 #A = np.pi*((diameter*10**(-3))/2)**2

    references = [r/(10**6) for r in references]  #put all values in meters
    current = [c/(10**6) for c in current]
    gap = [(20000-p)/(10**6) for p in positions]
    #print(gap)
    positions = [p/(10**6) for p in positions]

    stress = []
    for i in range(len(gap)):
        force = F0*(current[i]**2)*(d_ball**3)*np.exp(-gap[i]/g0) #force calculation from empiracle relationship
        stress.append(force/A)

    x_in = sum(positions[0:49])/50
    strain = []
    for p in positions:
        strain1 =(p-x_in)/l0  #calculate strain change
        strain.append(strain1)

    return stress, strain

def filter_stress_strain(stress, strain):
    """Data processing for stress and strain values.

    Takes stress strain and performs data processing. Currently
    subtracts the initial values from the rest of the array,
    bounds any negative values to zero and then indexes only from
    non-zero values.
    """

    strain_filtered = []
    int_strain = strain[0]
    for s in strain:
        s =s - int_strain
        if s < 0:
            strain_filtered.append(0)
        else:
            strain_filtered.append(s)

    stress_filtered = []
    int_stress = stress[0]
    for s in stress:
        s = s - int_stress
        if s < 0:
            stress_filtered.append(0)
        else:
            stress_filtered.append(s)

    k_strain_ind = [i for i, element in enumerate(strain_filtered) if element == 0]
    k_stress_ind = [i for i, element in enumerate(stress_filtered) if element == 0]

    k_ind = max(k_strain_ind[-1], k_stress_ind[-1])
    ind = min(k_ind, int(len(stress)/2))

    return stress_filtered[ind:-99], strain_filtered[ind:-99]

def test(x, a, b):
    """Function to fit stress and strain values to."""

    return a*x + b

def fit_line(stress, strain):
    """Function to calculate parameters of stress and strain line of best fit.

    Takes the stress and strain values, cuvre_fit performs
    least squares to calculate gradient and intercept.
    param[0] is estimate of gradient (Young's modulus)
    """

    param, param_cov = param, param_cov = curve_fit(test, strain, stress)
    x_inputs = np.linspace(min(strain), max(strain), 100)
    y_inputs = serialfunctions.test(x_inputs, param[0], param[1])

    return x_inputs, y_inputs, param[0]

################## functions under this line aren't implemented sucessfully yet#######
def CCD_reading(serialcom):
    arr_temp = serialcom.read(3694)
    for index, element in enumerate(arr_temp):
        arr[index] = int(element)

    return arr

def CCD_live(serialcom):
    finishing_point = "\r\nTest Ended\r\n"  #Haven't managed to integrate this yet -
    arrs = []                               #supposed to allow live plot of CCD
    plt.ion()
    while plt.isinteractive():
        new_value = serialcom.read(3684)
        print(new_value)
        arrs.append(int(new_value))
        if new_value == finishing_point:
            plt.close()
            plt.ioff()
        else:
            plt.cla()
            plt.plot(arrs)
            plt.pause(0.1)

def CCD_plotting(serialcom):
    array = CCD_reading(serialcom)
    plt.ion()
    plt.cla()
    plt.plot(array)
    plt.pause(0.1)
