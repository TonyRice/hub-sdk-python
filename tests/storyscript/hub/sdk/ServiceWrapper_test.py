import tempfile
import os
import json
from storyscript.hub.sdk.ServiceWrapper import ServiceWrapper
from storyscript.hub.sdk.GraphQL import GraphQL

from storyscript.hub.sdk.service.HubService import HubService

# note: needs updates/cleanup
hub_service_fixture = [{
    "service": {
        "name": "python",
        "alias": "python",
        "owner": {
            "username": "microservice"
        },
        "topics": [
            "python",
            "microservice"
        ],
        "description": "Execute a Python file with arguments.",
        "isCertified": False,
        "public": True
    },
    "serviceUuid": "0453f136-fe37-4c03-98a9-6ee38165c19e",
    "state": "BETA",
    "configuration": {
        "volumes": {
            "py": {
                "target": "/data"
            }
        },
        "entrypoint": {
            "help": "Execute a Python file.",
            "arguments": {
                "path": {
                    "help": "Path to the Python file to execute.",
                    "type": "string",
                    "required": True
                }
            }
        }
    },
    "readme": "nothing to see here."
},
    {
        "service": {
            "name": "hashes",
            "alias": None,
            "owner": {
                "username": "microservice"
            },
            "topics": [
                "hashing",
                "omg",
                "microservice"
            ],
            "description": "An OMG service which provides various hashing capabilities",
            "isCertified": False,
            "public": True
        },
        "serviceUuid": "0ceab9e4-b353-467d-8c77-e1538ab80ec1",
        "state": "BETA",
        "configuration": {
            "omg": 1,
            "info": {
                "title": "Hashes",
                "license": {
                    "url": "https://opensource.org/licenses/MIT",
                    "name": "MIT"
                },
                "version": "0.1.0",
                "description": "Digest and hashing capabilities"
            },
            "actions": {
                "hmac": {
                    "http": {
                        "path": "/hmac",
                        "port": 8080,
                        "method": "post"
                    },
                    "output": {
                        "type": "object",
                        "properties": {
                            "digest": {
                                "type": "string"
                            }
                        },
                        "contentType": "application/json"
                    },
                    "arguments": {
                        "data": {
                            "in": "requestBody",
                            "type": "string",
                            "required": True
                        }
                    }
                },
                "digest": {
                    "http": {
                        "path": "/digest",
                        "port": 8080,
                        "method": "post"
                    },
                    "output": {
                        "type": "object",
                        "properties": {
                            "digest": {
                                "type": "string"
                            }
                        },
                        "contentType": "application/json"
                    },
                    "arguments": {
                        "data": {
                            "in": "requestBody",
                            "type": "string",
                            "required": True
                        }
                    }
                }
            },
            "lifecycle": {
                "startup": {
                    "command": []
                }
            }
        },
        "readme": "Hashes\n=======\n\n[![Build status](https://img.shields.io/travis/microservice/hashes/master.svg?style=for-the-badge)](https://travis-ci.org/microservice/hashes)\n\nThis OMG service provides various digest and hashing capabilities.\n\nUsage\n-----\n\n```coffee\n# Storyscript\ndigest = hashes digest method: \"sha1\" data: \"hello world\"\n# {\"method\":\"sha1\",\"digest\":\"2AAE6C35C94FCFB415DBE95F408B9CE91EE846ED\"}\n```\n\n```coffee\n# Storyscript\ndigest = hashes hmac method: \"sha1\" data: \"hello world\" secret: \"my secret\"\n# {\"method\":\"sha1\",\"digest\":\"9F60EE4B05E590A7F3FAC552BFB9D98FA46F78D9\"}\n```\n"
    },
    {
        "service": {
            "name": "http",
            "alias": "http",
            "owner": {
                "username": "storyscript"
            },
            "topics": [
                "omg",
                "storyscript",
                "microservice"
            ],
            "description": "The Asyncy API gateway server for executing Stories via HTTP.",
            "isCertified": True,
            "public": True
        },
        "serviceUuid": "18564840-7551-4bb7-9ba7-bb9c9e2d92b4",
        "state": "BETA",
        "configuration": {
            "omg": 1,
            "actions": {
                "help": "Make http calls and listen for http connections through the Asyncy Gateway\nresulting in serverless http endpoints.\n",
                "fetch": {
                    "help": "Make a HTTP request to the outside world.\nThis command is native to the platform for performance reasons.\n",
                    "output": {
                        "type": "any"
                    },
                    "arguments": {
                        "url": {
                            "in": "requestBody",
                            "type": "string",
                            "required": True
                        }
                    }
                },
                "server": {
                    "events": {
                        "listen": {
                            "help": "Listen and respond to http connections by\nregistering with the Asyncy Gateway resulting in a serverless function.\n",
                            "http": {
                                "port": 8889,
                                "subscribe": {
                                    "path": "/register",
                                    "method": "post",
                                    "contentType": "application/json"
                                },
                                "unsubscribe": {
                                    "path": "/unregister",
                                    "method": "post",
                                    "contentType": "application/json"
                                }
                            },
                            "output": {
                                "type": "object",
                                "actions": {
                                    "flush": {
                                        "http": {
                                            "contentType": "application/json",
                                            "use_event_conn": True
                                        }
                                    }
                                },
                                "properties": {
                                    "uri": {
                                        "help": "The URI of the incoming HTTP request",
                                        "type": "string"
                                    }
                                },
                                "contentType": "application/json"
                            },
                            "arguments": {
                                "path": {
                                    "in": "requestBody",
                                    "type": "string",
                                    "required": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "readme": "# Asyncy HTTP Gateway\n\nAPI gateway server for executing Stories via HTTP.\n\n```coffee\nhttp server as server\n  when server listen method:'get' path:'/' as r\n    log info msg:r.body\n    log info msg:r.headers\n    log info msg:r.headers['Host']\n    r write data:'Hello World'\n    r status code:200\n    r finish\n```\n\n```sh\n$ curl https://foobar.storyscriptapp.com/\nHello World\n```\n\n\n## Development\n\nSetup virtual environment and install dependencies\n```\nvirtualenv -p python3.6 venv\nsource venv/bin/activate\npip install -r requirements.txt\n```\n\nRun locally by calling\n\n```\npython -m app.main --logging=debug --debug\n```\n\n### Register an endpoint\n\n```shell\ncurl --data '{\"endpoint\": \"http://localhost:9000/story/foo\", \"data\":{\"path\":\"/ping\", \"method\": \"post\", \"host\": \"a\"}}' \\\n     -H \"Content-Type: application/json\" \\\n     localhost:8889/register\n```\n\nNow access that endpoint\n\n```shell\ncurl -X POST -d 'foobar' -H \"Host: a.storyscriptapp.com\" http://localhost:8888/ping\n```\n\n\n### Unregister an endpoint\n\n```shell\ncurl --data '{\"endpoint\": \"http://localhost:9000/story/foo\", \"data\":{\"path\":\"/ping\", \"method\": \"post\", \"host\": \"a\"}}' \\\n     -H \"Content-Type: application/json\" \\\n     localhost:8889/unregister\n```\n"
    },
    {
        "service": {
            "name": "helloworld",
            "alias": "hello",
            "owner": {
                "username": "test"
            },
            "topics": [
                "hello"
            ],
            "description": "Does something completely pointless",
            "isCertified": False,
            "public": True
        },
        "serviceUuid": "0453f136-fe37-4c03-98a9-6ee38165c19e",
        "state": "BETA",
        "configuration": {
            "entrypoint": {
                "help": "Hello World",
                "arguments": {
                    "path": {
                        "help": "Path to something pointless",
                        "type": "string",
                        "required": True
                    }
                }
            }
        },
        "readme": "Hello World"
    }, {
        "service": {
            "name": "hashes",
            "alias": None,
            "owner": {
                "username": "microservice"
            },
            "topics": [
                "hashing",
                "omg",
                "microservice"
            ],
            "description": "An OMG service which provides various hashing capabilities",
            "isCertified": False,
            "public": True
        },
        "serviceUuid": "0ceab9e4-b353-467d-8c77-e1538ab80ec1",
        "state": "BETA",
        "configuration": {
            "omg": 1,
            "info": {
                "title": "Hashes",
                "license": {
                    "url": "https://opensource.org/licenses/MIT",
                    "name": "MIT"
                },
                "version": "0.1.0",
                "description": "Digest and hashing capabilities"
            },
            "actions": {
                "hmac": {
                    "http": {
                        "path": "/hmac",
                        "port": 8080,
                        "method": "post"
                    },
                    "output": {
                        "type": "object",
                        "properties": {
                            "digest": {
                                "type": "string"
                            }
                        },
                        "contentType": "application/json"
                    },
                    "arguments": {
                        "data": {
                            "in": "requestBody",
                            "type": "string",
                            "required": True
                        }
                    }
                }
            },
            "lifecycle": {
                "startup": {
                    "command": []
                }
            }
        },
        "readme": "Hashes\n=======\n\n[![Build status](https://img.shields.io/travis/microservice/hashes/master.svg?style=for-the-badge)](https://travis-ci.org/microservice/hashes)\n\nThis OMG service provides various digest and hashing capabilities.\n\nUsage\n-----\n\n```coffee\n# Storyscript\ndigest = hashes digest method: \"sha1\" data: \"hello world\"\n# {\"method\":\"sha1\",\"digest\":\"2AAE6C35C94FCFB415DBE95F408B9CE91EE846ED\"}\n```\n\n```coffee\n# Storyscript\ndigest = hashes hmac method: \"sha1\" data: \"hello world\" secret: \"my secret\"\n# {\"method\":\"sha1\",\"digest\":\"9F60EE4B05E590A7F3FAC552BFB9D98FA46F78D9\"}\n```\n"
    }]

not_python_fixture = {
    "service": {
        "name": "not_python",
        "alias": "npython",
        "owner": {
            "username": "microservice"
        },
        "topics": [
            "npython",
            "microservice"
        ],
        "description": "Don't execute a Python file with arguments.",
        "isCertified": False,
        "public": True
    },
    "serviceUuid": "0453f136-fe67-4c03-98a9-6ee38165c19e",
    "state": "BETA",
    "configuration": {
        "volumes": {
            "py": {
                "target": "/data"
            }
        },
        "entrypoint": {
            "help": "Don't execute a python file file.",
            "arguments": {
                "path": {
                    "help": "Path to the Python file to not execute.",
                    "type": "string",
                    "required": True
                }
            }
        }
    },
    "readme": "nothing to see here."
}


def test_deserialization():
    hub_services = [{
        "service": {
            "name": "helloworld",
            "alias": "hello",
            "owner": {
                "username": "test"
            },
            "topics": [
                "hello"
            ],
            "description": "Does something completely pointless",
            "isCertified": False,
            "public": True
        },
        "serviceUuid": "0453f136-fe37-4c03-98a9-6ee38165c19e",
        "state": "BETA",
        "configuration": {
            "entrypoint": {
                "help": "Hello World",
                "arguments": {
                    "path": {
                        "help": "Path to something pointless",
                        "type": "string",
                        "required": True
                    }
                }
            }
        },
        "readme": "Hello World"
    }]

    hub = ServiceWrapper.from_dict(hub_services)

    assert hub.get_all_service_names() == ["test/helloworld", "hello"]


def test_deserialization_from_file(mocker):
    expected_hub_services = ['microservice/python', 'python', 'microservice/hashes', 'storyscript/http', 'http', 'test/helloworld', 'hello']

    temp_file = tempfile.mktemp(suffix=".json")

    with open(temp_file, 'w') as outfile:
        json.dump(hub_service_fixture, outfile)

    hub = ServiceWrapper.from_json_file(path=temp_file)

    mocker.patch.object(HubService, 'from_dict')

    assert hub.get_all_service_names() == expected_hub_services

    assert hub.get('python') is not None

    HubService.from_dict.assert_called_with(data={"hub_service": hub_service_fixture[0]})

    os.remove(path=temp_file)


def test_deserialization_from_json(mocker):
    expected_hub_services = ["microservice/python", "python"]

    jsonstr = json.dumps([hub_service_fixture[0]])

    hub = ServiceWrapper.from_json(jsonstr)

    assert hub.get_all_service_names() == expected_hub_services

    mocker.patch.object(HubService, 'from_dict')
    assert hub.get('python') is not None

    HubService.from_dict.assert_called_with(data={
        "hub_service": hub_service_fixture[0]
    })


def test_dynamic_loading_with_deserialization(mocker):
    expected_hub_services = ['microservice/not_python', 'npython', 'test/helloworld', 'hello', 'microservice/hashes']

    mocker.patch.object(GraphQL, 'get_all', return_value=hub_service_fixture)

    hub = ServiceWrapper([not_python_fixture,
        "hello",
        "microservice/hashes"
    ])

    assert hub.get_all_service_names() == expected_hub_services


def test_serialization(mocker):
    expected_hub_services = ['microservice/not_python', 'npython', 'test/helloworld', 'hello', 'microservice/hashes']

    mocker.patch.object(GraphQL, 'get_all', return_value=hub_service_fixture)

    hub = ServiceWrapper([not_python_fixture,
        "hello",
        "microservice/hashes"
    ])

    temp_file = tempfile.mktemp(suffix=".json")

    hub.as_json_file(temp_file)

    assert hub.get_all_service_names() == expected_hub_services

    test_hub = ServiceWrapper.from_json_file(path=temp_file)

    assert test_hub.get_all_service_names() == expected_hub_services

    os.remove(temp_file)