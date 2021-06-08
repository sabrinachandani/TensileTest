import tkinter as tk
import serialfunctions
import serial
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys
from scipy.optimize import curve_fit
import numpy as np

def btn_generate_ramp_func():
    board=serial.Serial(port="COM5", baudrate=57600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=None)#connection to serial
    list = [start.get(), finish.get(), length.get(), test_type_var.get()]
    print(list)
    serialfunctions.set_controlling_var(board)
    serialfunctions.write_to_board(board, list)
    print('writing to board')
    [ref, pos, current] = serialfunctions.read_from_board(board)
    [stress, strain] = serialfunctions.plot_stress_strain(ref, pos, current, sample_length.get(), sample_diameter.get())
    [stress_filter, strain_filter] = serialfunctions.filter_stress_strain(stress, strain)
    [x_inputs, y_inputs, Youngs_mod] = serialfunctions.fit_line(stress_filter, strain_filter)

    subplot.cla()
    subplot.title.set_text('Stress - Strain')
    subplot.set_ylabel('Stress (Pa)')
    subplot.set_xlabel('Strain')
    subplot.plot(strain_filter, stress_fitler, 'o', color='red')
    subplot.plot(x_inputs, y_inputs, '--', color='blue')
    canvas_plot.draw()
    print("Young's Modulus Estimate:{}".format(param[0]))

window = tk.Tk()
window.title("Tensile Test")
window.configure(bg="#607D8B")
test_type_var= tk.IntVar()
test_type_var.set(0)
start=tk.IntVar()
finish=tk.IntVar()
length=tk.IntVar()

#sample dimension Variables
sample_length=tk.IntVar()
sample_diameter=tk.IntVar()

frm_inputs = tk.Frame(
                    master = window,
                    bg="#607D8B"
                    )
frm_variables = tk.Frame(
                        master=frm_inputs,
                        bg="#607D8B"
                        )
frm_entry_boxes = tk.Frame(
                        master=frm_variables,
                        bg="#455A64",
                        relief=tk.GROOVE,
                        borderwidth=1
                        )

ent_start = tk.Entry(
                    master=frm_entry_boxes,
                    width=10, bg="#455A64",
                    fg="#ECEFF1",
                    textvariable = start
                    ).grid(row=0, column=1, sticky="w")
lbl_start = tk.Label(
                    master=frm_entry_boxes,
                    text = "Start value:",
                    bg="#455A64",
                    fg="#ECEFF1"
                    ).grid(row=0, column=0, sticky="e")


ent_finish = tk.Entry(
                    master=frm_entry_boxes,
                    width=10,
                    bg="#455A64",
                    fg="#ECEFF1",
                    textvariable=finish
                    ).grid(row=1, column=1, sticky="w")
lbl_finish = tk.Label(
                    master=frm_entry_boxes,
                    text = "Finish value:",
                    bg="#455A64",
                    fg="#ECEFF1"
                    ).grid(row=1, column=0, sticky="e")



ent_length = tk.Entry(
                    master=frm_entry_boxes,
                    width=10,
                    bg="#455A64",
                    fg="#ECEFF1",
                    textvariable=length
                    ).grid(row=2, column=1, sticky="w")
lbl_length = tk.Label(
                    master=frm_entry_boxes,
                    text = "Length:",
                    bg="#455A64",
                    fg="#ECEFF1"
                    ).grid(row=2, column=0, sticky="e")



frm_buttons = tk.Frame(
                        master=frm_variables,
                        relief=tk.GROOVE,
                        borderwidth=1,
                        bg="#455A64"
                        )
rdbtn_tensile = tk.Radiobutton(
                            master=frm_buttons,
                            text="Tensile Test",
                            fg="#ECEFF1",
                            bg="#455A64",
                            variable=test_type_var,
                            value=0,
                            ).grid(row=0, column=0, padx=10, pady=10)

rdbtn_hysterisis = tk.Radiobutton(
                                master=frm_buttons,
                                text="Hysterisis Test",
                                fg="#ECEFF1",
                                bg="#455A64",
                                variable=test_type_var,
                                value=1,
                                ).grid(row=1, column=0, padx=10, pady=10)
tensile_test_lbl = tk.Label(
                            master=frm_inputs,
                            text="Test Variables",
                            relief=tk.GROOVE,
                            width=35,
                            borderwidth=1).grid(row=0, column=0)

frm_entry_boxes.grid(row=1, column=0, padx=10, pady=10)
frm_buttons.grid(row=1, column=1, padx=10, pady=10)
frm_variables.grid(row=1, column=0)

btn_generate_ramp=tk.Button(
                    master=frm_inputs,
                    text="Run Test",
                    width=35,
                    height=5,
                    command=btn_generate_ramp_func
                    ).grid(row=4, column=0, padx=10, pady=10)
frm_output=tk.Frame(
                    master=window,
                    bg="#607D8B"
                    )
lbl_display=tk.Label(
                    master=frm_output,
                    text="Output",
                    relief=tk.GROOVE,
                    width=35,
                    borderwidth=1
                    ).grid(row=0, column=0, padx=10, pady=10)
lbl_serialoutput=tk.Frame(
                    master=frm_output,
                    relief=tk.GROOVE,
                    width=35,
                    height=10,
                    borderwidth=1
                    )
lbl_serialoutput.grid(row=1, column=0, padx=10, pady=10)

fig = Figure(figsize=(6,4), dpi=100)
subplot = fig.add_subplot(1,1,1)
subplot.title.set_text('Stress - Strain')
subplot.set_ylabel('Stress (Pa)')
subplot.set_xlabel('Strain')
canvas_plot = FigureCanvasTkAgg(
                    fig,
                    master=lbl_serialoutput
                    )
canvas_plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas_plot.draw()


#additional entry boxes for specimen dimensions - all within frm_inputs
frm_sample = tk.Frame(
                    master = frm_inputs,
                    bg="#607D8B"
                    )

ent_sample_length = tk.Entry(
                    master=frm_sample,
                    width=10,
                    bg="#455A64",
                    fg="#ECEFF1",
                    textvariable=sample_length
                    ).grid(row=0, column=1, sticky="w")

lbl_sample_length = tk.Label(
                    master=frm_sample,
                    text = "Sample length:",
                    bg="#455A64",
                    fg="#ECEFF1"
                    ).grid(row=0, column=0, sticky="e")

ent_sample_diameter = tk.Entry(
                    master=frm_sample,
                    width=10,
                    bg="#455A64",
                    fg="#ECEFF1",
                    textvariable=sample_diameter
                    ).grid(row=1, column=1, sticky="w")

lbl_sample_diameter = tk.Label(
                    master=frm_sample,
                    text = "Sample Diameter:",
                    bg="#455A64",
                    fg="#ECEFF1"
                    ).grid(row=1, column=0, sticky="e")
frm_sample.grid(row=3, column=0)

lbl_sample_dimensions=tk.Label(
                                master=frm_inputs,
                                text="Sample Dimensions (mm)",
                                relief=tk.GROOVE,
                                width=35,
                                borderwidth=1
                                ).grid(row=2, column=0, pady=10)
frm_inputs.grid(row=0, column=0)
frm_output.grid(row=0, column=1)
window.mainloop()
