# ChromaCamera (Experimental)

This tool was built of a need to quickly visualize [`chroma`](https://github.com/Benland100/chroma) geometries without having to use a CUDA-equipped GPU. Instead of running a full raytracing simulation to generate an image, like in how `chroma.Camera` is implemented, the optimized THREE.js library is used to render the 3D scene quickly in the browser using OpenGL. Geometries must first be converted to the `.json` format using the `jsonGeometry` class to be loaded into js.

A demo of this tool can be found on my website at [https://samy.ng/chroma-cam/](https://samy.ng/chroma-cam/). Click "load theia" in the top right of the screen, or upload your own json file to see the tool in action. All computations are done solely on the client side, so no data is sent to any server. You can see an example of the structure of the json file in [static/geo/dichroicon.json](https://raw.githubusercontent.com/youngsm/chromaCamera/main/static/geo/dichroicon.json). The json file contains a list of unique meshes, their colors, and their positions for placment in the scene.

Like in `chroma`, solid instancing has been implemented, so that no single triangle in a scene is unneccesarily duplicated more than once. This allows for very large scenes using copies of the same couple meshes to be rendered quickly, and relatively small json files. For example, a full neutrino detector geometry outfitted with around 60,000 PMTs and 30,000 light concentrators is rendered on my M1 MacBook Pro at around 40 fps in Microsoft Edge, and has a json file size of 7.1 MB. In `chroma` this entire geometry loaded on the GPU requires around 20 GB of VRAM. In the browser, only around 80 MB of memory is used.

## Usage

To use this tool, you must first convert your chroma geometry to the json format. This can be done using the `jsonGeometry` class:

```python
import json
from geometry import jsonGeometry

chroma_geo = <some chroma.Geometry or chroma.detector object>
json_geo = jsonGeometry(chroma_geo)
json_data = json_geo.as_json()
with open('chroma_geo.json', 'w') as f:
    json.dump(json_data, f)
```

To load the geometry into the browser, you can start up a local Flask server serving the index.html file in the `templates/` directory:

```bash
$ python server.py
```

Then, navigate to `localhost:5000` in your browser and upload `chroma_geo.json`. Alternatively, the exact page is being hosted on my Github pages site, [https://samy.ng/chroma-cam/](https://samy.ng/chroma-cam/).