import json
from uuid import UUID

from storyscript.hub.sdk.GraphQL import GraphQL

from storyscript.hub.sdk.service.HubService import HubService


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


"""
The ServiceWrapper provides an improved way to access storyscript hub services
"""


class ServiceWrapper:

    def __init__(self, services=None):
        self.services = {}
        self.reload_services(services)

    @classmethod
    def from_dict(cls, dictionary=None):
        services = []

        if dictionary is not None:
            services = dictionary

        return cls(services)

    @classmethod
    def from_json(cls, jsonstr=None):
        services = []

        if jsonstr is not None:
            services = json.loads(jsonstr)

        return cls(services)

    @classmethod
    def from_json_file(cls, path=None):
        services = []

        if path is not None:
            with open(path, 'r') as f:
                services = json.load(f)

        return cls(services)

    def reload_services(self, services=None):
        # reset services
        self.services = {}

        all_services = None
        if type(services) is list:
            for service in services:
                if type(service) is dict:
                    hub_service = service["service"]
                    self.services[(hub_service["owner"]["username"] + '/' + hub_service["name"])] = service
                elif type(service) is str:
                    # this allows us to utilize dynamic loading
                    if not all_services:
                        all_services = GraphQL.get_all()

                    for _service in all_services:
                        service_owner = _service["service"]["owner"]["username"]
                        service_name = _service["service"]["name"]
                        service_alias = _service["service"]["alias"]
                        if service == service_owner + "/" + service_name or service == service_alias:
                            self.services[service_owner + "/" + service_name] = _service

        elif type(services) is dict:
            for service in services:
                _service = services[service]
                service_owner = _service["service"]["owner"]["username"]
                service_name = _service["service"]["name"]
                self.services[service_owner + "/" + service_name] = _service

    def as_json(self):
        services = []

        for service in self.services:
            services.append(self.services[service])

        return json.dumps(services, indent=4, sort_keys=True, cls=UUIDEncoder)

    def as_json_file(self, out_file=None):
        services = []

        for service in self.services:
            services.append(self.services[service])

        if out_file is not None:
            with open(out_file, 'w') as f:
                json.dump(services, f, indent=4, sort_keys=True, cls=UUIDEncoder)

    def get_all_service_names(self, include_aliases=True):
        service_names = []

        for service in self.services:
            _service = self.services[service]["service"]
            service_names.append(service)
            alias = _service["alias"]

            if include_aliases and alias is not None and alias not in service_names:
                service_names.append(alias)

        return service_names

    def get(self, alias=None, owner=None, name=None):
        service = None

        if alias and alias in self.services:
            service = self.services[alias]
        elif f'{owner}/{name}' in self.services:
            service = self.services[f'{owner}/{name}']
        else:
            for _service in self.services:
                hub_service = self.services[_service]["service"]
                if owner is not None and name is not None and\
                        hub_service["owner"]["username"] == owner and \
                        hub_service["name"] == name:
                    service = self.services[_service]
                elif name is not None and hub_service["name"] == name:
                    service = self.services[_service]
                elif alias is not None and (hub_service["alias"] == alias or hub_service["name"] == alias):
                    service = self.services[_service]

        if service is None:
            return None
        else:
            return HubService.from_dict(data={
                "hub_service": service
            })