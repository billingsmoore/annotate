import PySimpleGUI as sg
import os
import pandas as pd

# load in guidelines
with open('guidelines.txt', 'r') as f:
        guidelines = f.read()

file_list_column = [
    [sg.Text("Select a file of data to annotate:")],
    [sg.Text("Folder"),sg.In(size=(20,1),enable_events=True,key="-FOLDER-"),sg.FolderBrowse(),],
    [sg.Listbox(values=[],enable_events=True,size=(40,25),key='-FILE LIST-')],
    [sg.HSeparator(),],
    [sg.Text('Process Information:',size=(40,1),key='-MONITOR HEADER-')],
    [sg.Text(size=(40,5),key="-MONITOR-")],
]

guideline_viewer_column = [
    [sg.Text("Annotation Guidelines:")],
    [sg.Text(size=(50, 30), key="-GUIDE-", text=guidelines)],
    [sg.Button('Begin')]
]

data_viewer_column = [
    [sg.Text("Data to be annotated:")],
    [sg.Text(size=(50, 25), key="-DATA-")],
    [sg.Input(key='-INPUT-')],
    [sg.Button('Back'), sg.Button('Enter'), sg.Button('Done')]
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(guideline_viewer_column),
        sg.VSeparator(),
        sg.Column(data_viewer_column)
    ]
]

window = sg.Window('Annotate',layout=layout)

# initialize empty data flag
data_loaded_flag = False

while True:
    event, values = window.read()

    # end program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # with a folder selected, make a list of file in folder
    elif event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f 
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
        ]

        window["-FILE LIST-"].update(fnames)


    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )

            window['-MONITOR-'].update('Loading data..')
            window.refresh()
            try:
                data = pd.read_csv(filename)
                data_loaded_flag = True
                window['-MONITOR-'].update('Data loaded')
                window.refresh()
            except:
                window['-MONITOR-'].update('Data failed to load')
                window.refresh()

        except:
            pass

    elif event == 'Begin':
        # when user presses Begin the data annotation should start
        # display each piece of data individually for annotation

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
                try:
                    sample = data.iloc[i]['msg_txt']
                    window['-DATA-'].update(sample)
                    window['-MONITOR-'].update(f'Data loaded \n{i}/{total} annotated')
                except:
                    window['-DATA-'].update('All data has been annotated!')

                window.refresh()
                
                if event == 'Enter':
                # when user presses enter, the annotation should be saved
                # then the next piece of data should be displayed
                    data.at[i, 'annotation'] = values['-INPUT-']
                    i += 1
                elif event == 'Back':
                    if i > 0:
                        i -= 1
                elif event == 'Done' or i >= (total - 1):
                    window['-DATA-'].update('All data has been annotated!')
                    window.refresh()
                    break

            window['-MONITOR-'].update('Data loaded \nAnnotation finished')
            try:
                data.to_csv('annotated_data.csv')
                window['-MONITOR-'].update('Data loaded \nAnnotation finished\nAnnotation saved to annotated_data.csv')
            except:
                window['-MONITOR-'].update('Data loaded \nAnnotation finished\nAnnotation failed to save')

window.close()