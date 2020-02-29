import os
from mfm_emm_graph.grid import Grid

directory = os.environ.get("EMM_GD_DIR")
epochs = {}
for filename in os.listdir(directory):
    print(filename)
    if filename.endswith('.json'):
        epochs.update({filename.split('.')[0].split('-')[-1]: Grid(f'{directory}/{filename}')})

