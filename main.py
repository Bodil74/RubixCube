from WireFrame import WireFrame
from Projection import ProjectionViewer
import numpy as np

cube_nodes = [(x, y, z) for x in (50, 250)for y in (50, 250) for z in (50, 250)]

cube = WireFrame()
cube.addNodes(np.array(cube_nodes))
cube.addEdges([[n, n + 4] for n in range(0, 4)])
cube.addEdges([[n, n + 1] for n in range(0, 8, 2)])
cube.addEdges([[n, n + 2] for n in (0, 1, 4, 5)])
cube.addFaces([cube.edges[n] + cube.edges[n + 1][::-1] for n in range(0, len(cube.edges) - 4, 2)] + [[0, 4, 6, 2], [1, 5, 7, 3]])
cube.addColors([(255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 165, 0)])
cube._outputNodes()
cube._outputEdges()
'''
triangle = WireFrame()
triangle_nodes = [(50, 150, 50), (250, 150, 50), (250, 150, 250), (50, 150, 250), (150, 50, 150)]
triangle.addNodes(np.array(triangle_nodes))
triangle.addEdges([[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 4], [2, 4], [3, 4]])
#triangle.addFaces([[0, 1, 2, 3], [0, 4, 1], [1, 4, 2], [2, 4, 3], [3, 4, 0]])
#triangle.addColors([(255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)])
triangle._outputNodes()
triangle._outputEdges()
#triangle._outputFaces()
'''
pv = ProjectionViewer(600, 600)
pv.addWireFrame('cube', cube)
#pv.addWireFrame('triangle', triangle)
pv.run()
