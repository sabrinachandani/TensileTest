import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
def calculate_stress_strain(references, positions, current):
    d_ball = 0.004
    F0 = 6.13*10**6
    F0 = F0*(d_ball/0.004)**3
    g0 = 0.002258 #in meters
    #define specimin size
    t = 0.0003
    w = 0.0005
    l0 = 0.01
    A = w*t

    references = [r/(10**6) for r in references]    #put data back in terms of metres
    current = [c/(10**6) for c in current]
    gap = [(20000-p)/(10**6) for p in positions]
    positions = [p/(10**6) for p in positions]
    #print(references)                               #prints to terminal - just a checking point

    stress = []
    for i in range(len(gap)):                       #iterate through every value in list
        force = F0*(current[i]**2)*(d_ball**3)*np.exp(-gap[i]/g0)
        stress.append(force/A)

    x_in = sum(positions[0:49])/50                  #use average of first 50 values as initial length
    strain = []
    for p in positions:
        strain1 =(p-x_in)/l0
        #print(strain1)
        strain.append(strain1)

    new_strain = []
    int_strain = strain[0]
    for s in strain:
        s = s - int_strain
        if s < 0:
            new_strain.append(0)
        else:
            new_strain.append(s)

    new_stress = []
    int_stress = stress[0]
    for s in stress:
        s = s - int_stress
        if s < 0:
            new_stress.append(0)
        else:
            new_stress.append(s)

    k_strain_ind = [i for i, element in enumerate(new_strain) if element==0]
    k_stress_ind = [i for i, element in enumerate(new_stress) if element==0]

    k_ind = max(k_strain_ind[-1], k_stress_ind[-1])
    ind = min(k_ind, int(len(stress)/2))



    non_zero_stress = new_stress[ind:-99]
    non_zero_strain = new_strain[ind:-99]


    return non_zero_stress, non_zero_strain

def test(x, a, b):
    return a*x + b

if __name__ == "__main__":
    data = pd.read_excel(r'~/Documents/IIB/Project/Code/Adrien_trial5.xlsx')
    df = pd.DataFrame(data)
    df['References'] = df['References'].astype(int)
    df['Positions'] = df['Positions'].astype(int)
    df['Current'] = df['Current'].astype(int)
    stress, strain = calculate_stress_strain(df['References'], df['Positions'], df['Current'])
    #pfit = np.polynomial.Polynomial.fit(stress, strain, 1)
    param, param_cov = curve_fit(test, strain, stress)
    print(param)
    plt.plot(strain, stress, 'o', color='red')
    fake_strain = np.linspace(min(strain), max(strain),100)
    fake_stress = test(fake_strain, param[0], param[1])
    print(param[0])
    plt.plot(fake_strain, fake_stress, '--', color='blue')
    plt.grid()
    plt.xlabel('Engineering Strain')
    plt.ylabel('Stress (Pa)')
    plt.show()
