import plotly.graph_objects as go
import numpy as np

import load_obj
import load_temp

temp_data = load_temp.nested_temperature_list()
obj_mesh = load_obj.obj_meshing()
data_sensor = []

SENSOR_1 = 100, 200, 100, 200, 100, 150
SENSOR_2 = 100, 200, 100, 200, 350, 400
SENSOR_3 = 100, 200, 400, 500, 100, 150
SENSOR_4 = 100, 200, 400, 500, 350, 400
SENSOR_5 = 400, 500, 400, 500, 100, 150
SENSOR_6 = 400, 500, 400, 500, 350, 400
SENSOR_7 = 400, 500, 100, 200, 100, 150
SENSOR_8 = 400, 500, 100, 200, 350, 400
SENSOR_LIST = [
    SENSOR_1, SENSOR_2, SENSOR_3, SENSOR_4,
    SENSOR_5, SENSOR_6, SENSOR_7, SENSOR_8
]


def sensor_boxes(xmin, xmax, ymin, ymax, zmin, zmax) -> dict:
    ''' Function for creating mesh3d box objects. '''
    mesh = dict(
        x=[xmin, xmin, xmax, xmax, xmin, xmin, xmax, xmax],
        y=[ymin, ymax, ymax, ymin, ymin, ymax, ymax, ymin],
        z=[zmin, zmin, zmin, zmin, zmax, zmax, zmax, zmax],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        type='mesh3d',
        cmin=30,
        cmax=45,
        name='',
    )
    data_sensor.append(mesh)


for i in range(len(SENSOR_LIST)):
    sensor_boxes(
        SENSOR_LIST[i][0],
        SENSOR_LIST[i][1],
        SENSOR_LIST[i][2],
        SENSOR_LIST[i][3],
        SENSOR_LIST[i][4],
        SENSOR_LIST[i][5],
    )


def temp_pack(i):
    ''' Function to assign temperature to mesh3d boxes. '''
    packed = data_sensor
    for j in range(8):
        packed[j]['intensity'] = np.linspace(temp_data[i][j], temp_data[i][j], 8)
        packed[j]['text'] = temp_data[i][j]
    packed.append(obj_mesh)
    return packed


fig = go.Figure(
    data=data_sensor,
    layout=go.Layout(updatemenus=[dict(type='buttons', buttons=[dict(label='Play', method='animate', args=[None])])]),
    frames=[go.Frame(data=temp_pack(i), name=str(i)) for i, k in enumerate(temp_data)],
)


fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 600]),
            yaxis=dict(range=[0, 600]),
            zaxis=dict(range=[0, 500]),
            aspectratio=dict(
                x=1,
                y=1,
                z=1,
            ),
        ),
)


def frame_args(duration):
    return {
            'frame': {'duration': duration},
            'mode': 'immediate',
            'fromcurrent': True,
            'transition': {'duration': duration, 'easing': 'linear'},
        }


sliders = [
            {
                'pad': {'b': 10, 't': 60},
                'len': 0.9,
                'x': 0.1,
                'y': 0,
                'steps': [
                    {
                        'args': [[f.name], frame_args(0)],
                        'label': str(k),
                        'method': 'animate',
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

fig.update_layout(sliders=sliders)
fig.show()
