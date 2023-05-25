import json
import numpy as np
from flask import Flask, render_template, jsonify, request
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes
        
# def dec_to_rgb(dec):
#     B =  dec & 255
#     G = (dec >> 8) & 255
#     R = (dec >> 16) & 255
#     A = (dec >> 24) & 255
#     return (R, G, B), A


# def argb_to_rgb_hex(argb):
#     b = argb & 255
#     g = (argb >> 8) & 255
#     r = (argb >> 16) & 255
#     return (r << 16) + (g << 8) + b


@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/api/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     if file:
#         solid = json.load(file)
#         meshes = []
#         for mesh in solid['meshes']:
#             positions = mesh['position']
#             orientations = mesh['orientation']
#             if len(positions) == 1: continue

#             for submesh in mesh['submeshes']:
#                 solid_color = int(argb_to_rgb_hex(submesh['color']))
#                 __, a = dec_to_rgb(solid_color)
#                 solid_data = {
#                     'vertices': submesh['vertices'],
#                     'triangles': submesh['faces'],
#                     'color': solid_color,
#                     'instance_count': len(positions),
#                     'instance_positions': positions,
#                     'instance_orientations': orientations,
#                     'alpha': a / 255.0
#                 }
#                 meshes.append(solid_data)
#         print('Uploaded', len(meshes), 'individual meshes')
#         return jsonify({'meshes': meshes})
#     else:
#         return jsonify({'error': 'no file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)