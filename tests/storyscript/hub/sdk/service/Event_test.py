import json

from storyscript.hub.sdk.service.Action import Action
from storyscript.hub.sdk.service.Argument import Argument
from storyscript.hub.sdk.service.Event import Event

from storyscript.hub.sdk.service.EventOutput import EventOutput
from storyscript.hub.sdk.service.HttpOptions import HttpOptions

event_fixture = {
    "name": "listen",
    "event": {
        "help": "Nothing to see here.",
        "http": {
            "port": 8889,
            "subscribe": {
                "path": "/register",
                "method": "post",
                "contentType": "application/json"
            }
        },
        "output": {
            "type": "object",
            "actions": {
                "write": {
                    "http": {
                        "path": "/digest",
                        "port": 8080,
                        "method": "post",
                        "contentType": "application/json",
                        "use_event_conn": True,
                        "subscribe": {
                            "path": "/stream/subscribe",
                            "method": "post",
                            "contentType": "application/json"
                        },
                        "unsubscribe": {
                            "path": "/stream/unsubscribe",
                            "method": "post"
                        }
                    },
                    "arguments": {
                        "flush": {
                            "in": "responseBody",
                            "type": "boolean",
                            "required": False
                        }
                    }
                }
            },
            "properties": {
                "query_params": {
                    "help": "The parsed query parameters of the HTTP request",
                    "type": "map"
                }
            },
            "contentType": "application/json"
        },
        "arguments": {
            "path": {
                "type": "string",
                "required": True
            }
        }
    }
}

event_fixture_json = json.dumps(event_fixture)


def test_deserialization(mocker):
    mocker.patch.object(json, 'loads', return_value=event_fixture)

    mocker.patch.object(Argument, 'from_dict')
    mocker.patch.object(Action, 'from_dict')
    mocker.patch.object(EventOutput, 'from_dict')
    mocker.patch.object(HttpOptions, 'from_dict')

    assert Event.from_json(jsonstr=event_fixture_json) is not None

    json.loads.assert_called_with(event_fixture_json)

    Argument.from_dict.assert_any_call(data={
        "name": "path",
        "argument": event_fixture["event"]["arguments"]["path"]
    })

    EventOutput.from_dict.assert_any_call(data={
        "event_output": event_fixture["event"]["output"]
    })

    HttpOptions.from_dict.assert_called_once_with(data={
        "http_options": event_fixture["event"]["http"]
    })


def test_serialization(mocker):
    mocker.patch.object(json, 'dumps', return_value=event_fixture_json)

    service_event = Event.from_dict(data=event_fixture)

    assert service_event.as_json(compact=True) is not None
    json.dumps.assert_called_with(event_fixture, sort_keys=True)

    assert service_event.as_json() is not None
    json.dumps.assert_called_with(event_fixture, indent=4, sort_keys=True)