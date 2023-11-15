import PySimpleGUI as sg
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

# load in guidelines
with open('guidelines.txt', 'r') as f:
        guidelines = f.read()

info_column = [
    [sg.Text("Select a file of data to annotate:")],
    [sg.Text("Folder"),sg.In(size=(20,1),enable_events=True,key="-FILE-"),sg.FileBrowse(),],
    [sg.Text("Selected filename:")],
    [sg.Text(key='-FILENAME-')],
    [sg.HSeparator(),],
    [sg.Text("Annotation Guidelines:")],
    [sg.Text(size=(40, 10), key="-GUIDE-", text=guidelines, text_color= 'black', background_color='light blue')],
    [sg.HSeparator(),],
    [sg.Text('Process Information:',size=(40,1),key='-MONITOR HEADER-')],
    [sg.Text(size=(40,10),key="-MONITOR-", text_color= 'black', background_color='light blue')],
    [sg.Button('Begin')]
]

data_viewer_column = [
    [sg.Text("Data to be annotated:")],
    [sg.Text(size=(50, 25), key="-DATA-", text_color= 'black', background_color='light blue')],
    [sg.Text("Your annotation:")],
    [sg.Input(key='-INPUT-')],
    [sg.Button('Back'), sg.Button('Enter')]
]

layout = [
    [
        sg.Column(info_column),
        sg.VSeparator(),
        sg.Column(data_viewer_column)
    ]
]

window = sg.Window('Annotate',layout=layout)

# initialize empty data flag
data_loaded_flag = False



while True:
    event, values = window.read()

    # bind enter key to Enter button
    window['-INPUT-'].bind("<Return>", "_Enter")
    window['-INPUT-'].bind("<KP_Enter>", "_Enter")


    # end program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # with a folder selected, make a list of file in folder
    elif event == "-FILE-":
        filename = values["-FILE-"]
        window['-FILENAME-'].update(filename)
        window.refresh()

    elif event == 'Begin':
        # when user presses Begin the data annotation should start
        # display each piece of data individually for annotation

        #try to load in data
        try:
            window['-MONITOR-'].update('Loading data..')
            window.refresh()
            data = pd.read_csv(filename)
            data_loaded_flag = True
            window['-MONITOR-'].update('Data loaded')
            window.refresh()
        except:
            window['-MONITOR-'].update('Data failed to load')
            window.refresh()

        # if no data is loaded, do nothing
        if data_loaded_flag == False:
            window['-MONITOR-'].update('No data has been loaded for annotation')
            window.refresh()
        
        else:
            # data counter 
            i = 0
            total = len(data)
            while True:
                event, values = window.read()
                window.refresh()
                try:
                    sample = data.iloc[i]['msg_txt']
                    window['-DATA-'].update(sample)
                    window['-MONITOR-'].update(f'Data loaded \n{i}/{total} annotated')
                except:
                    window['-DATA-'].update('All data has been annotated!')

                window.refresh()

                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                
                # if all data has been annotated, alert user and save annotations
                elif i >= (total):
                    window['-DATA-'].update('All data has been annotated!')
                    window['-MONITOR-'].update(f'Data loaded \n{total}/{total} annotated \nAnnotation finished!')
                    try:
                        data.to_csv(filename[:-4] +'_annotated.csv')
                        window['-MONITOR-'].update(f'Data loaded \nAnnotation finished\nAnnotation saved to {filename[:-4]}_annotated.csv')
                    except:
                        window['-MONITOR-'].update('Data loaded \nAnnotation finished\nAnnotation failed to save')
                    window.refresh()
                    break
                
                elif event == 'Enter' or event == '-INPUT-' + "_Enter" or event == '-INPUT-' + "_Enter":
                # when user presses enter, the annotation should be saved
                # then the next piece of data should be displayed
                    data.at[i, 'annotation'] = values['-INPUT-']
                    i += 1
                    window['-INPUT-'].update('')
                    window.refresh()

                elif event == 'Back':
                    if i > 0:
                        i -= 1
                        window['-INPUT-'].update('')
                        window.refresh()

                
window.close()