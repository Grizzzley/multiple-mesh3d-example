import numpy as np
import pandas as pd


file_obj = '.\\mesh_test1.obj'
csv_data = pd.read_csv(file_obj, encoding='utf-8')


def obj_to_mesh3d(odata):
    ''' Function to convert obj data to mesh3d data. '''
    vertices = []
    faces = []
    for i in range(len(odata)):
        list = odata.loc[i]
        slist = [item.split(' ') for item in list][0]
        if slist:
            if slist[0] == 'v':
                vertex = np.array(slist[1:], dtype=float)
                vertices.append(vertex)
            elif slist[0] == 'f':
                face = []
                for k in range(1, len(slist)):
                    face.append([int(s) for s in slist[k].replace('//','/').split('/')])
                if len(face) > 3:
                    faces.extend([[face[0][0]-1, face[k][0]-1, face[k+1][0]-1] for k in range(1, len(face)-1)])
                else:
                    faces.append([face[j][0]-1 for j in range(len(face))])
            else:
                continue
        else:
            pass

    return np.array(vertices), np.array(faces)


def obj_meshing():
    vertices, faces = obj_to_mesh3d(csv_data)
    x, y, z = vertices[:, :3].T
    I, J, K = faces.T

    mesh = dict(
        type='mesh3d',
        cmin=30,
        cmax=45,
        x=x,
        y=y,
        z=z,
        i=I,
        j=J,
        k=K,
        name='',    
    )

    mesh.update(intensity=z*100)
    return mesh
