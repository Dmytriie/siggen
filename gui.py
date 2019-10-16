from particles import Particle
from signal_generator import SignalGenerator
import PySimpleGUI as sg
from screeninfo import get_monitors
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

sg.SetOptions(window_location = (200, 200))

listbox = sg.Listbox(values = [], size = (55, 6))
listbox_values = []
listbox.select_mode = 'multiple'
listbox.change_submits = True
siggen = SignalGenerator()
P = Particle()
wave = siggen.send_waves()
freqs, fu = siggen.freq_spectre(wave)
cent_freqs = []
spreads = []
gausses = np.zeros(len(freqs))
allfreqs = []
allamps = []
allphases = []
def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def one_wave_layout(button1, button2):
    layout = [
          [sg.Text('Enter parameters of your particle: ')] ,
          [sg.Text('A', size=(25, 1)), sg.InputText('235')] ,      # size = (length*height of the field )
          [sg.Text('Z', size=(25, 1)), sg.InputText('92')] ,      # size = (length*height of the field )
          [sg.Text('Charge state ', size=(25, 1)), sg.InputText('92')] ,      # size = (length*height of the field )
          [sg.Text('Extracting energy, MeV/u ', size=(25, 1)), sg.InputText('400')] ,      # size = (length*height of the field )
          [sg.Text('Cooling ', size=(25, 1)), sg.InputText('0.00001')] ,      # size = (length*height of the field )
          [sg.Text('Shunt impedance ', size=(25, 1)), sg.InputText('50')] ,      # size = (length*height of the field )
          [sg.Text('Phase', size=(25, 1)), sg.InputText('0')] ,      # size = (length*height of the field )
          [sg.Button(button_text = str(button1), button_color=('white', 'green')), sg.Cancel()]
          ]
    return layout

sampling_layout = [
          [sg.Text('sampling rate', size=(15, 1)), sg.InputText('3000')] ,
          [sg.Button(button_text = 'Set sampling', button_color=('white', 'green')), sg.Cancel()]
          ]

menu_def = [
                    ['File', ['Save As...',['PDF', 'PNG', 'EPS', 'TXT'],  'Close']],
                    ['Particles', ['Add particle', 'Remove particle']],
                    ['Plotting', ['Plot', 'Set Bandwidth', 'Set sampling', 'Fit' ]]
                    ]

freqs_frame_layout = [
                                   [listbox],
                                   [sg.Button('Remove', button_color=('white', 'green'), key = '_DELETE_'), sg.Button('Change', button_color=('white', 'green'), key = '_CHANGE_'), sg.Button('Fit', button_color=('white', 'green')), sg.Button('Plot', button_color=('white', 'green')), sg.Button('Clear all	',button_color=('white', 'green'), key = '_CLEAR_') ]
                                   ]
main_layout = [
            [sg.Menu(menu_def, tearoff=True)],
            [ sg.Button('Add particle', button_color=('white', 'green')), sg.Button('Add bunch', button_color=('white', 'green')), sg.Button('Set Bandwidth', button_color=('white', 'green')), sg.Button('Close', button_color=('white', 'green'))  ],
            [sg.Frame('Particles on the plot', freqs_frame_layout) ]
          ]

add_bunch_layout = [
          [sg.Text('Enter parameters of your bunch: ')] ,
          [sg.Text('A', size=(25, 1)), sg.InputText('235')] ,      # size = (length*height of the field )
          [sg.Text('Z', size=(25, 1)), sg.InputText('92')] ,      # size = (length*height of the field )
          [sg.Text('Charge state ', size=(25, 1)), sg.InputText('92')] ,      # size = (length*height of the field )
          [sg.Text('Extracting energy, MeV/u ', size=(25, 1)), sg.InputText('400')] ,      # size = (length*height of the field )
          [sg.Text('Shunt impedance ', size=(25, 1)), sg.InputText('50')] ,      # size = (length*height of the field
          [sg.Text('Momentum spread, Hz', size=(25, 1)), sg.InputText('0.00001')],
          [sg.Text('Particles amount ', size=(25, 1)), sg.InputText('1000')],
          [sg.Button('Add bunch', button_color=('white', 'green')), sg.Cancel()]
          ]

sb_layout = [
          [sg.Text('Enter bandwidth: ')] ,
          [sg.Text('Bandwidth, Hz', size=(15, 1)), sg.InputText('')] ,      # size = (length*height of the field )
          [sg.Button('Set Bandwidth', button_color=('white', 'green')), sg.Cancel()]
          ]

main_window = sg.Window('Schottky signals generator').Layout(main_layout)

while True:
    button, main_values = main_window.Read()
    if button is 'Set sampling':
        samp = sg.PopupGetText('Set sampling rate in kHz:')
        if samp:
            siggen = SignalGenerator(sampfreq = int(samp))
            wave = siggen.send_waves()

    if button is 'Add particle' or button is 'Normal':
        add_window = sg.Window('Adding a new particle').Layout(one_wave_layout('Add particle', 'Cancel'))
        button, main_values = add_window.Read()

        if button == 'Cancel' or button == None :
            add_window.Close()
            continue

        if button == 'Add particle':
            P.add_particle_Z(int(main_values[0]), int(main_values[1]), int(main_values[2]))
            ampl = P.get_amplitude (int(main_values[0]), int(main_values[1]), int(main_values[2]), int(main_values[3]), float(main_values[4]), float(main_values[5]))
            freq = P.get_freq(int(main_values[0]), int(main_values[1]), int(main_values[2]))/1E3 #to go to MHz
            siggen.add_wave(ampl, freq, float(main_values[6]))
            cent_freqs.append(freq)
            allfreqs.append(freq)
            allamps.append(ampl)
            allphases.append(float(main_values[6]))
            listbox_values.append( 'A: ' + main_values[0] + ' Z: ' + main_values[1] +' charge_state: ' + main_values[2]  )
            listbox.Update(values = listbox_values)
            wave = siggen.send_waves()
            add_window.Close()

    if button is 'Add bunch' or button is 'Bunch':
        addsp_window = sg.Window('Adding bunch').Layout(add_bunch_layout)
        button, main_values = addsp_window.Read()
        if button == 'Cancel' or button == None :
            addsp_window.Close()
            continue
        if button == 'Add bunch':
            P.add_particle_Z(int(main_values[0]), int(main_values[1]), int(main_values[2]))
            P.init_T = int(main_values[3])
            #def get_amplitude(self, A, Z, charge_state, amount, cooling, R_sh):
            ampl = P.get_amplitude (int(main_values[0]), int(main_values[1]), int(main_values[2]), int(main_values[6]), float(main_values[5]), float(main_values[4]))
            freq = P.get_freq(int(main_values[0]), int(main_values[1]), int(main_values[2]))/1E3 #to go to KHz
            #def add_spread_wave(self, amp, central_frequency, phase, freqspread, bunchsize):
            siggen.add_spread_wave(ampl, freq, 0, float(main_values[5]), int(main_values[6]))
            addsp_window.Close()
            cent_freqs.append(freq)
            spreads.append(float(main_values[6]))
            for freq in siggen.wavefreqs:
                listbox_values.append( 'A: ' + main_values[0] + ' Z: ' + main_values[1]  +' charge: ' + main_values[2]  )
                allfreqs.append(float(freq))
                allamps.append(float(ampl))
                allphases.append(0)
            listbox.Update(values = listbox_values)
            wave = siggen.send_waves()
            addsp_window.Close()

    if button is 'Set Bandwidth':
        sb_window = sg.Window('Bandwidth adjustment').Layout(sb_layout)
        button, value = sb_window.Read()
        if button == 'Cancel' or button == None :
            sb_window.Close()
            continue
        if button == 'Set Bandwidth':
            siggen = SignalGenerator(sampfreq = int(value[0]))
            wave = siggen.send_waves()
            sb_window.Close()

    if button is 'Plot':
        plt.ion()
        plt.clf()
        freqs, fu = siggen.freq_spectre(wave)
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('signal power (W)')
        plt.title('Schottky frequency spectrum')
        plt.grid(True)
        plt.plot(freqs, fu)
        plt.show()

    if button is 'PDF' or button is 'EPS' or button is 'PNG':
        text = sg.PopupGetText('Enter filename', 'Save as ' + button)
        if type(text) == str:
            plt.savefig(text + '.' + button.lower(), bbox_inches = 'tight')

    if button is 'TXT':
        text = sg.PopupGetText('Enter filename', 'Save as ' + button)
        if type(text) == str:
            data= []
            fu = np.transpose(np.array(fu))
            freqs = np.transpose(np.array(freqs))
            if len(gausses) != 0:
                gausses = np.transpose(np.array(gausses))
                data = np.transpose(np.reshape(np.concatenate((freqs, fu, gausses), axis = 0), (3, len(fu))))
            if len(gausses)== 0:
                data = np.transpose(np.reshape(np.append([freqs, fu], axis = 0), (2, len(fu))))
            np.savetxt(text + '.' +  button.lower(), data, header=' Frequency, Hz                            Amplitude, V                             Gauss fit, V')

    if button is 'Fit':
        gausses = np.zeros(len(freqs))
        plt.clf()
        popt_all=[]
        for mean, sigma in zip(cent_freqs, spreads):
            popt,pcov = curve_fit(gaus,freqs,fu, p0=[1, mean, sigma])
            popt_all.append(popt)
        for popt in popt_all:
            gausses = np.sum([gausses, gaus(freqs,*popt)], axis = 0)
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('signal power (W)')
        plt.title('Schottky frequency spectrum')
        plt.grid(True)
        plt.plot(freqs, fu)
        plt.plot(freqs, gausses)
        '''
    if button is '_DELETE_':
        wavedata = main_values[1]
        if (len(wavedata) != 0):
            wavedata = wavedata[0].split(' ')
            ampl = P.get_amplitude (int(wavedata[1]), int(wavedata[3]), int(wavedata[5]), 1, float(wavedata[4]), float(wavedata[5]))
            freq = P.get_freq(int(wavedata[0]), int(wavedata[1]), int(wavedata[2]))/1E3 #to go to MHz
            siggen.delete_wave(ampl, freq, 0)
            wave = siggen.send_waves()
            listbox_values.remove( 'A: ' + wavedata[1] + ' Z: ' + wavedata[3]  +' charge_state: ' + wavedata[5]  )
            listbox.Update(values = listbox_values)
            allfreqs.remove(freq)
        if (len(wavedata) == 0):
            sg.Popup('No waves found ;( )
        '''

    if button is '_CHANGE_':
        wavedata = main_values[1]
        if (len(wavedata) == 0):
                sg.Popup('No waves found :(')
        if (len(wavedata) != 0):
            change_window = sg.Window('Changing an existing wave').Layout(one_wave_layout('Change', 'Cancel'))
            ch_button, ch_val = change_window.Read()
            if ch_button == 'Cancel' or ch_button == None :
                change_window.Close()
                continue
            if ch_button == 'Change':
                wavedata = wavedata[0].split(' ')

                P.remove_particle(int(wavedata[1]), int(wavedata[3]), int(wavedata[5]) )
                listbox_values.remove( 'A: ' + wavedata[1] + ' Z: ' + wavedata[3]  +' charge_state: ' + wavedata[5]  )
                siggen.delete_wave(ampl, freq, float(ch_val[6]))
                allfreqs.remove(freq)

                P.add_particle_Z(int(ch_val[0]), int(ch_val[1]), int(ch_val[2]))
                ampl = P.get_amplitude (int(ch_val[0]), int(ch_val[1]), int(ch_val[2]), int(ch_val[3]), float(ch_val[4]), float(ch_val[5]))
                freq = P.get_freq(int(ch_val[0]), int(ch_val[1]), int(ch_val[2]))/1E3 #to go to MHz
                siggen.add_wave(ampl, freq, int(ch_val[2]))
                wave = siggen.send_waves()
                listbox_values.append( 'A: ' + ch_val[0] + ' Z: ' + ch_val[1] +' charge_state: ' + ch_val[2]  )
                listbox.Update(values = listbox_values)
                change_window.Close()

    if button is '_CLEAR_':
        wave = np.zeros(siggen.meas_time*siggen.sampfreq)
        listbox_values = 	[]
        listbox.Update(values = listbox_values)

    if button is 'Close' or button is None:
       break

main_window.Close()
