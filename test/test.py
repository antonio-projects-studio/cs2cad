from pathlib import Path
from cs2cad import cs2cad

json_dict = {
 "entities": {
  "FI4bCL9y0XvsF52": {
   "name": "Extrude 1", 
   "type": "ExtrudeFeature", 
   "profiles": [
    {
     "profile": "JGC", 
     "sketch": "FQgWGf8WhgalpUy"
    }
   ], 
   "extent_two": {
    "distance": {
     "type": "ModelParameter", 
     "role": "AgainstDistance", 
     "name": "none", 
     "value": 0.0
    }, 
    "type": "DistanceExtentDefinition", 
    "taper_angle": {
     "type": "ModelParameter", 
     "role": "Side2TaperAngle", 
     "name": "none", 
     "value": 0.0
    }
   }, 
   "extent_one": {
    "distance": {
     "type": "ModelParameter", 
     "role": "AlongDistance", 
     "name": "none", 
     "value": 0.025400000000000002
    }, 
    "type": "DistanceExtentDefinition", 
    "taper_angle": {
     "type": "ModelParameter", 
     "role": "TaperAngle", 
     "name": "none", 
     "value": 0.0
    }
   }, 
   "operation": "NewBodyFeatureOperation", 
   "start_extent": {
    "type": "ProfilePlaneStartDefinition"
   }, 
   "extent_type": "OneSideFeatureExtentType"
  }, 
  "FQgWGf8WhgalpUy": {
   "transform": {
    "origin": {
     "y": 0.0, 
     "x": 0.0, 
     "z": 0.0
    }, 
    "y_axis": {
     "y": 1.0, 
     "x": 0.0, 
     "z": 0.0
    }, 
    "x_axis": {
     "y": 0.0, 
     "x": 1.0, 
     "z": 0.0
    }, 
    "z_axis": {
     "y": 0.0, 
     "x": 0.0, 
     "z": 1.0
    }
   }, 
   "type": "Sketch", 
   "name": "Sketch 1", 
   "profiles": {
    "JGC": {
     "loops": [
      {
       "is_outer": True, 
       "profile_curves": [
        {
         "center_point": {
          "y": 0.0, 
          "x": 0.0, 
          "z": 0.0
         }, 
         "type": "Circle3D", 
         "radius": 0.09104851, 
         "curve": "JGB", 
         "normal": {
          "y": 0.0, 
          "x": 0.0, 
          "z": 1.0
         }
        }
       ]
      }
     ], 
     "properties": {}
    }
   }, 
   "reference_plane": {}
  }
 }, 
 "properties": {
  "bounding_box": {
   "max_point": {
    "y": 0.09104851445359824, 
    "x": 0.09104851445359824, 
    "z": 0.025400000000000002
   }, 
   "type": "BoundingBox3D", 
   "min_point": {
    "y": -0.09104851445359824, 
    "x": -0.09104851445359824, 
    "z": 0.0
   }
  }
 }, 
 "sequence": [
  {
   "index": 0, 
   "type": "Sketch", 
   "entity": "FQgWGf8WhgalpUy"
  }, 
  {
   "index": 1, 
   "type": "ExtrudeFeature", 
   "entity": "FI4bCL9y0XvsF52"
  }
 ]
}

cs2cad(json_dict, Path(__file__).parent / "step")