# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import unittest
import numpy as np
from extensions.ops.space_to_depth import SpaceToDepth
from mo.graph.graph import Node
from mo.utils.error import Error
from mo.utils.unittest.graph import build_graph

nodes = {
    'in_data_node': {'value': None, 'kind': 'data', 'shape': np.array([1, 2048, 1152, 64])},
    'StD': {'op': 'SpaceToDepth', 'kind': 'op', 'block_size': 2},
    'out_data_node': {'value': None, 'kind': 'data', 'shape': None}
}

edges = [
    ('in_data_node', 'StD'),
    ('StD', 'out_data_node')
]

class TestSpaceToDepthPartialInfer(unittest.TestCase):
    def test_tf_space_to_depth_infer_nhwc(self):
        graph = build_graph(nodes, edges)
        graph.graph['layout'] = 'NHWC'
        std_node = Node(graph, 'StD')
        SpaceToDepth.infer(std_node)
        exp_shape = np.array([1, 1024, 576, 256])
        res_shape = graph.node['out_data_node']['shape']
        self.assertTrue(np.array_equal(exp_shape, res_shape))

    def test_tf_space_to_depth_infer_nchw(self):
        graph = build_graph(nodes, edges)
        graph.graph['layout'] = 'NCHW'
        graph.node['in_data_node']['shape'] = np.array([1, 64, 2048, 1152])
        std_node = Node(graph, 'StD')
        SpaceToDepth.infer(std_node)
        exp_shape = np.array([1, 256, 1024, 576])
        res_shape = graph.node['out_data_node']['shape']
        self.assertTrue(np.array_equal(exp_shape, res_shape))

    def test_tf_space_to_depth_infer_shape_error(self):
        graph = build_graph(nodes, edges)
        graph.graph['layout'] = 'NHWC'
        graph.node['in_data_node']['shape'] = np.array([1024, 576, 256])
        std_node = Node(graph, 'StD')
        self.assertRaises(Error, SpaceToDepth.infer, std_node)

    def test_tf_space_to_depth_infer_divisibility_error_1(self):
        graph = build_graph(nodes, edges)
        graph.graph['layout'] = 'NHWC'
        graph.node['in_data_node']['shape'] = np.array([1, 1024, 577, 256])
        std_node = Node(graph, 'StD')
        self.assertRaises(Error, SpaceToDepth.infer, std_node)

    def test_tf_space_to_depth_infer_divisibility_error_2(self):
        graph = build_graph(nodes, edges)
        graph.graph['layout'] = 'NCHW'
        graph.node['in_data_node']['shape'] = np.array([1, 256, 1024, 577])
        std_node = Node(graph, 'StD')
        self.assertRaises(Error, SpaceToDepth.infer, std_node)