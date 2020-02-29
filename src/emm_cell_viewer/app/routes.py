from . import app
from .parse import epochs
from flask import render_template
import io
from contextlib import redirect_stdout
from graph_tool.draw import graph_draw
from jinja2 import Markup

def get_prev_next_epoch(epoch):
    """
    Loop through the epoch keys to determine the next and prev. Note that the dict keys are latest first.
    """
    found = False
    last = 0
    for e in epochs.keys():
        if found:
            prev_epoch = e
            break
        prev_epoch = e
        if e == epoch:
            found = True
            next_epoch = last
        last = e
    return prev_epoch, next_epoch

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', epochs=epochs)

@app.route('/epoch/<epoch>')
def epoch(epoch):
    grid = epochs[epoch]
    prev_epoch, next_epoch = get_prev_next_epoch(epoch)
    with io.StringIO() as buf, redirect_stdout(buf):
        grid.print_grid_ascii()
        grid_ascii = buf.getvalue()
    return render_template('epoch.html',
                           grid=grid,
                           grid_ascii=grid_ascii,
                           epoch=epoch,
                           prev_epoch=prev_epoch,
                           next_epoch=next_epoch)

@app.route('/epoch/<epoch>/cell/<identifier>')
def cell(epoch, identifier):
    prev_epoch, next_epoch = get_prev_next_epoch(epoch)
    for c in epochs[epoch].cells:
        if c.identifier.data_members["id"] == int(identifier):
            cell = c
    with io.StringIO() as buf, redirect_stdout(buf):
        cell.print_cell_grid()
        grid_ascii = buf.getvalue()
    return render_template('cell.html',
                           cell=cell,
                           epoch=epoch,
                           identifier=identifier,
                           grid_ascii=grid_ascii,
                           prev_epoch=prev_epoch,
                           next_epoch=next_epoch)

@app.route('/epoch/<epoch>/cell/<identifier>_tree_<treeID>.svg')
def tree_svg(epoch, identifier, treeID):
    prev_epoch, next_epoch = get_prev_next_epoch(epoch)
    for c in epochs[epoch].cells:
        if c.identifier.data_members["id"] == int(identifier):
            cell = c
    return render_template('tree.svg',
                           cell=cell,
                           markup=Markup,
                           treeID=int(treeID),
                           prev_epoch=prev_epoch,
                           next_epoch=next_epoch)
