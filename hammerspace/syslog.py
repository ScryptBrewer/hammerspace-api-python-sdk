# hammerspace/syslog.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SyslogClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client
        logger.info("SyslogClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all syslog configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single syslog configuration.
        (Corresponds to GET /syslog/{identifier} - OpId: getSyslogConfigurationByIdentifier)

        Otherwise, lists all syslog configurations.
        (Corresponds to GET /syslog - OpId: listSyslogConfiguration)
        Optional kwargs for listing: spec, page, page.size, page.sort, page.sort.dir
        """
        query_params = {}
        if identifier:
            path = f"/syslog/{identifier}"
            logger.info(f"Getting syslog configuration by identifier: {identifier}")
            # No query params for GET /syslog/{identifier} in spec
        else:
            path = "/syslog"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing syslog configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns SyslogView or List

    def create(
        self,
        syslog_data: Dict[str, Any], # requestBody is BaseEntityView, implies fields for SyslogView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Configures syslog.
        (Corresponds to POST /syslog - OpId: createSyslogConfiguration)
        """
        path = "/syslog"
        query_params = {} # No query params for POST in spec
        logger.info(f"Creating syslog configuration with data: {syslog_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=syslog_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="POST", json_data=syslog_data, query_params=query_params)
            return self.api_client.read_and_parse_json_body(response) # Returns SyslogView

    def update(
        self,
        identifier: str,
        syslog_data: Dict[str, Any], # requestBody is SyslogView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing syslog configuration by its identifier.
        (Corresponds to PUT /syslog/{identifier} - OpId: updateSyslogConfigurationByIdentifier)
        """
        path = f"/syslog/{identifier}"
        query_params = {} # No query params for PUT in spec
        logger.info(f"Updating syslog configuration '{identifier}' with data: {syslog_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=syslog_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="PUT", json_data=syslog_data, query_params=query_params)
            return self.api_client.read_and_parse_json_body(response) # Returns SyslogView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a syslog configuration by its identifier.
        (Corresponds to DELETE /syslog/{identifier} - OpId: deleteSyslogConfigurationByIdentifier)
        """
        path = f"/syslog/{identifier}"
        query_params = {} # No query params for DELETE in spec
        logger.info(f"Deleting syslog configuration '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="DELETE", query_params=query_params)
            return self.api_client.read_and_parse_json_body(response) # Returns SyslogView
    
    def configure_multiple_servers(
        self,
        servers: List[str],
        enabled: bool = True,
        ports: Optional[List[int]] = None,
        transports: Optional[List[str]] = None,
        message_types: Optional[List[str]] = None,
        monitor_task: bool = False,
        task_timeout_seconds: int = 300,
        create_new: bool = False,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Configure multiple syslog servers in a single operation.
        
        Args:
            servers: List of syslog server addresses
            enabled: Whether syslog is enabled (default: True)
            ports: List of ports for each server (default: 514 for all)
            transports: List of transport protocols for each server (default: UDP for all)
            message_types: Types of messages to send (default: FILESYSTEM, EVENT)
            monitor_task: Whether to monitor the task until completion
            task_timeout_seconds: Timeout for task monitoring
            create_new: Create a new configuration instead of updating existing
            
        Returns:
            The created or updated syslog configuration
        """
        # Set defaults
        if ports is None:
            ports = [514] * len(servers)
        elif len(ports) == 1:
            ports = ports * len(servers)
        
        if transports is None:
            transports = ["UDP"] * len(servers)
        elif len(transports) == 1:
            transports = transports * len(servers)
            
        if message_types is None:
            message_types = ["FILESYSTEM", "EVENT"]
            
        # Validate inputs
        if len(ports) != len(servers):
            raise ValueError("Number of ports must match number of servers")
        
        if len(transports) != len(servers):
            raise ValueError("Number of transports must match number of servers")
            
        for transport in transports:
            if transport not in ["UDP", "TCP"]:
                raise ValueError(f"Invalid transport protocol: {transport}. Must be UDP or TCP.")
                
        valid_message_types = ["FILESYSTEM", "EVENT", "AUDIT", "SYSTEM"]
        for msg_type in message_types:
            if msg_type not in valid_message_types:
                raise ValueError(f"Invalid message type: {msg_type}. Must be one of {valid_message_types}")
        
        # Get existing configuration if we're updating
        existing_config = None
        identifier = None
        
        if not create_new:
            configs = self.get()
            if configs and len(configs) > 0:
                existing_config = configs[0]  # Use the first config
                identifier = existing_config["uoid"]["uuid"]
        
        # Prepare syslog server configurations
        syslog_servers = []
        for i, server in enumerate(servers):
            server_config = {
                "server": server,
                "port": ports[i],
                "transport": transports[i],
                "messageTypes": message_types
            }
            syslog_servers.append(server_config)
        
        # Create the configuration data
        syslog_data = {
            "_type": "SYSLOG",
            "enabled": enabled,
            "syslogServers": syslog_servers
        }
        
        if existing_config:
            # Update existing configuration
            syslog_data["uoid"] = existing_config["uoid"]
            syslog_data["created"] = existing_config.get("created", 0)
            syslog_data["modified"] = existing_config.get("modified", 0)
            syslog_data["extendedInfo"] = existing_config.get("extendedInfo", {})
            
            return self.update(identifier, syslog_data, monitor_task=monitor_task, 
                              task_timeout_seconds=task_timeout_seconds)
        else:
            # Create new configuration
            return self.create(syslog_data, monitor_task=monitor_task, 
                              task_timeout_seconds=task_timeout_seconds)
    
    def enable(
        self,
        enabled: bool = True,
        monitor_task: bool = False,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Enable or disable syslog without changing other configuration.
        
        Args:
            enabled: Whether to enable (True) or disable (False) syslog
            monitor_task: Whether to monitor the task until completion
            task_timeout_seconds: Timeout for task monitoring
            
        Returns:
            The updated syslog configuration
        """
        configs = self.get()
        if not configs or len(configs) == 0:
            raise ValueError("No syslog configuration found to enable/disable")
            
        config = configs[0]  # Use the first config
        identifier = config["uoid"]["uuid"]
        
        # Only update the enabled field
        config["enabled"] = enabled
        
        return self.update(identifier, config, monitor_task=monitor_task, 
                          task_timeout_seconds=task_timeout_seconds)