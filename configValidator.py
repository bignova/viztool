from jsonschema import validate

schema = {
  "type": "object",
  "properties": {
    "py/object": {
      "type": "string"
    },
    "urlExtension": {
      "type": "string"
    },
    "devices": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "py/object": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "events": {
            "type": "array",
            "items": [
              {
                "type": "object",
                "properties": {
                  "py/object": {
                    "type": "string"
                  },
                  "name": {
                    "type": "string"
                  },
                  "graphs": {
                    "type": "object"
                  },
                  "token": {
                    "type": "string"
                  }
                },
                "required": [
                  "py/object",
                  "name",
                  "graphs",
                  "token"
                ]
              }
            ]
          }
        },
        "required": [
          "py/object",
          "name",
          "events"
        ]
      }
    },
    "graphs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "py/object": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "json_format": {
            "type": "object"
          },
          "sources": {
            "type": "object",
            "properties": {
              "patternProperties": {
                "[a-zA-Z0-9]": {
                  "type": "object",
                  "properties": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  }
                }
              }
            }
          }
        },
        "required": [
          "py/object",
          "name",
          "json_format",
          "sources"
        ]
      }
    }
  },
  "required": [
    "py/object",
    "urlExtension",
    "devices",
    "graphs"
  ]
}

class configValidator(object):
    def isValidConfig(self, config):
        global schema

        try:
            #if no exception is raised by validate(), the instance is valid
            validate(config, schema)
        except:
            print "Error: Invalid JSON config file; see example.json for the correct format"
            return False

        return True
