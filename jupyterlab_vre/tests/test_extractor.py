import json
import logging
import os
import uuid
from unittest import TestCase

import nbformat as nb

from jupyterlab_vre.database.cell import Cell
from jupyterlab_vre.services.converter.converter import ConverterReactFlowChart
from jupyterlab_vre.services.extractor.extractor import Extractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if os.path.exists('resources'):
    base_path = 'resources'
elif os.path.exists('jupyterlab_vre/tests/resources/'):
    base_path = 'jupyterlab_vre/tests/resources/'


def create_cell(payload_path=None):
    with open(payload_path, 'r') as file:
        payload = json.load(file)

    cell_index = payload['cell_index']
    notebook = nb.reads(json.dumps(payload['notebook']), nb.NO_CONVERT)
    extractor = Extractor(notebook)

    source = notebook.cells[cell_index].source
    title = source.partition('\n')[0]
    title = title.replace('#', '').replace(
        '_', '-').replace('(', '-').replace(')', '-').replace('.', '-').strip() if title and title[
        0] == "#" else "Untitled"

    if 'JUPYTERHUB_USER' in os.environ:
        title += '-' + os.environ['JUPYTERHUB_USER'].replace('_', '-').replace('(', '-').replace(')', '-').replace('.',
                                                                                                                   '-').replace(
            '@',
            '-at-').strip()

    ins = []
    outs = []
    params = []
    confs = []
    dependencies = []

    # Check if cell is code. If cell is for example markdown we get execution from 'extractor.infere_cell_inputs(
    # source)'
    if notebook.cells[cell_index].cell_type == 'code':
        ins = set(extractor.infere_cell_inputs(source))
        outs = set(extractor.infere_cell_outputs(source))

        confs = extractor.extract_cell_conf_ref(source)
        dependencies = extractor.infer_cell_dependencies(source, confs)

    node_id = str(uuid.uuid4())[:7]
    cell = Cell(
        node_id=node_id,
        title=title,
        task_name=title.lower().replace(' ', '-'),
        original_source=source,
        inputs=ins,
        outputs=outs,
        params=params,
        confs=confs,
        dependencies=dependencies,
        container_source=""
    )
    return cell


def extract_cell(payload_path):
    # Check if file exists
    if os.path.exists(payload_path):
        cell = create_cell(payload_path)

        node = ConverterReactFlowChart.get_node(
            cell.node_id,
            cell.title,
            cell.inputs,
            cell.outputs,
            cell.params,
            cell.dependencies
        )

        chart = {
            'offset': {
                'x': 0,
                'y': 0,
            },
            'scale': 1,
            'nodes': {cell.node_id: node},
            'links': {},
            'selected': {},
            'hovered': {},
        }

        cell.chart_obj = chart
        return cell.toJSON()
    return None


class TestExtractor(TestCase):

    def test_extract_cell(self):
        cell = extract_cell(os.path.join(base_path, 'notebooks/MULTIPLY_framework_cells.json'))
        cell = extract_cell(os.path.join(base_path, 'notebooks/laserfarm_cells.json'))
        cell = extract_cell(os.path.join(base_path, 'notebooks/vol2bird_cells.json'))
        try:
            cell = extract_cell(os.path.join(base_path, 'notebooks/MULTIPLY_framework_2.json'))
        except SyntaxError as e:
            logger.warning(str(e))
        cell = extract_cell(os.path.join(base_path, 'notebooks/laserfarm.json'))
        if cell:
            cell = json.loads(cell)
            for conf_name in (cell['confs']):
                self.assertFalse('conf_' in cell['confs'][conf_name].split('=')[1],
                                 'conf_ values should not contain conf_ prefix in '
                                 'assignment')
