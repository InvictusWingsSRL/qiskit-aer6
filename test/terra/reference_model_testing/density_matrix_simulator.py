import numpy as np
import math
from qstructs import DensityMatrix, QuantumState
from qstructs import phase

class DensityMatrixSimulator:

    def __init__(self):

        self.gate2mats = {
            'id': [np.array([[1, 0], [0, 1]])],
            'h': [math.sqrt(0.5)*np.array([[1, 1], [1, -1]])],
            'x': [np.array([[0, 1], [1, 0]])],
            'y': [np.complex(0, 1)*np.array([[0, -1], [1, 0]])],
            'z': [np.array([[1, 0], [0, -1]])],
            #'t': [np.array([[1, 0], [0, phase(math.pi/4)]])],
            #'tdg': [np.array([[1, 0], [0, phase(-math.pi/4)]])],
            #'s': [np.array([[1, 0], [0, np.complex(0,1)]])],
            #'sdg': [np.array([[1, 0], [0, -np.complex(0,1)]])],
            'cx': [np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])],
            'cz': [np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])],
            'measure': [np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])]
            }


    def get_supported_gates(self):
        result = list(self.gate2mats.keys())
        result.append('reset')
        return result


    def run(self, qobj):

        for circuit in qobj.experiments:
            n_qubits = circuit.header.number_of_qubits
            density_matrix = DensityMatrix(QuantumState.ground_state(n_qubits))

            for op in circuit.instructions:
                if op.name == 'reset':
                    density_matrix = density_matrix.reset(op.qubits[0])
                else:
                    density_matrix = density_matrix.qop_on_qubits(op.qubits, self.gate2mats[op.name])

        return density_matrix