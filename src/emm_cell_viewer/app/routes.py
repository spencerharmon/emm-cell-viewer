from . import app
from .parse import epochs
from flask import render_template
import io
from contextlib import redirect_stdout
from graph_tool.draw import graph_draw
from jinja2 import Markup

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', epochs=epochs)

@app.route('/epoch/<epoch>')
def epoch(epoch):
    grid = epochs[epoch]
    with io.StringIO() as buf, redirect_stdout(buf):
        grid.print_grid_ascii()
        grid_ascii = buf.getvalue()
    return render_template('epoch.html', grid=grid, grid_ascii=grid_ascii, epoch=epoch)

@app.route('/epoch/<epoch>/cell/<identifier>')
def cell(epoch, identifier):
    for c in epochs[epoch].cells:
        if c.identifier.data_members["id"] == identifier:
            cell = c
    return render_template('cell.html', cell=cell, graph_draw=graph_draw, epoch=epoch, identifier=identifier)

@app.route('/epoch/<epoch>/cell/<identifier>_tree_<treeID>.svg')
def tree_svg(epoch, identifier, treeID):
    for c in epochs[epoch].cells:
        if c.identifier.data_members["id"] == identifier:
            cell = c
    return render_template('tree.svg', cell=cell, graph_draw=graph_draw, markup=Markup, treeID=treeID)
