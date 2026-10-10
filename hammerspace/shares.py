# hammerspace/shares.py
import logging
from typing import Optional, List, Dict, Any, Union

from .models.share import ShareCreate, ShareUpdate, ShareView
from .models.base import HammerspaceBaseModel

logger = logging.getLogger(__name__)

class SharesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        simple: bool = False,
        as_model: bool = False,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]], Optional[List[ShareView]], Optional[ShareView]]:
        """
        Gets all shares or a specific share by its identifier (UUID or name).

        If 'identifier' is provided, fetches a single share.
        (Assumes GET /shares/{identifier} - NOT in provided OpenAPI snippet)

        Otherwise, lists all shares.
        (Corresponds to GET /shares - OpId: ListShares)

        Args:
            identifier: Share UUID or name to fetch specific share
            simple: If True, returns only uuid, name, and path fields
            as_model: If True, returns ShareView models instead of raw dicts
            **kwargs: Optional query params for listing (spec, page, page_size, page_sort, page_sort_dir)
        """
        query_params = {}
        if identifier:
            path = f"/shares/{identifier}"
            logger.warning(
                f"get_share by id: Attempting GET from '{path}'. "
            )
        else:
            path = "/shares"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing shares with effective query params: {query_params}")

        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        result = self.api_client.read_and_parse_json_body(response, model=ShareView if as_model else None)

        if simple and result:
            return self._simplify_shares_response(result)

        return result

    def _simplify_shares_response(self, shares_data: Union[List[Any], Dict[str, Any], ShareView]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Simplifies share response to only include uuid, name, and path fields.

        Args:
            shares_data: Full share data from API response (dicts or ShareView models)

        Returns:
            Simplified share data with only uuid, name, and path
        """
        def extract_simple_fields(share: Any) -> Dict[str, Any]:
            if isinstance(share, ShareView):
                return {"uuid": share.uuid, "name": share.name, "path": share.path}
            uoid = share.get("uoid")
            return {
                "uuid": uoid.get("uuid") if isinstance(uoid, dict) else None,
                "name": share.get("name"),
                "path": share.get("path")
            }

        if isinstance(shares_data, list):
            return [extract_simple_fields(share) for share in shares_data]
        else:
            return extract_simple_fields(shares_data)

    def create(
        self,
        share_data: Optional[Union[ShareCreate, Dict[str, Any]]] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        comment: Optional[str] = None,
        export_options: Optional[List[Dict[str, Any]]] = None,
        share_objectives: Optional[List[Dict[str, Any]]] = None,
        share_size_limit: Optional[int] = None,
        warn_utilization_percent_threshold: Optional[int] = None,
        smb_browsable: Optional[bool] = None,
        # New snapshot parameters
        create_snapshots: bool = False,
        snapshot_schedules: Optional[List[Dict[str, Any]]] = None,
        use_default_snapshot_plans: bool = True,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        as_model: bool = False
    ) -> Union[Optional[str], Optional[Dict[str, Any]], Optional[ShareView]]:
        """
        Creates a new share with optional snapshot configuration.

        Args:
            share_data: Complete share configuration as a dict or ShareCreate model
                        (if provided, other params ignored)
            name: Share name (required if share_data not provided)
            path: Share path (required if share_data not provided)
            comment: Share description
            export_options: List of export option dicts
            share_objectives: List of objective dicts
            share_size_limit: Size limit in bytes
            warn_utilization_percent_threshold: Warning threshold percentage
            smb_browsable: Whether share is SMB browsable
            create_snapshots: Whether to create snapshot schedules for this share
            snapshot_schedules: Custom snapshot schedule configurations
            use_default_snapshot_plans: Use system default snapshot retention plans
            monitor_task: Whether to monitor the task
            task_timeout_seconds: Task timeout
            as_model: If True, returns a ShareView model instead of raw data
        """
        if share_data is None:
            if not name or not path:
                raise ValueError("name and path are required when share_data is not provided")
            share_data = self._build_share_data(
                name=name, path=path, comment=comment, export_options=export_options,
                share_objectives=share_objectives, share_size_limit=share_size_limit,
                warn_utilization_percent_threshold=warn_utilization_percent_threshold,
                smb_browsable=smb_browsable
            )
        if isinstance(share_data, HammerspaceBaseModel):
            # Normalize to a wire dict so downstream dict access (share name)
            # keeps working; the client would serialize it anyway.
            share_data = share_data.to_api()

        assumed_path = "/shares"
        logger.warning(f"create_share: Attempting POST to '{assumed_path}'.")

        # Create the share first
        result = self.api_client.execute_and_monitor_task(
            path=assumed_path, method="POST", initial_json_data=share_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds,
            result_model=ShareView if as_model else None
        )

        # If share creation was successful and snapshots requested, create snapshot schedules
        if result and create_snapshots:
            share_name = share_data.get("name")
            if share_name:
                try:
                    self._create_share_snapshots(
                        share_name, snapshot_schedules, use_default_snapshot_plans,
                        monitor_task, task_timeout_seconds
                    )
                except Exception as e:
                    logger.error(f"Failed to create snapshots for share '{share_name}': {e}")
                    # Don't fail the entire operation if snapshot creation fails

        return result

    def update(
        self,
        identifier: str,
        share_data: Optional[Union[ShareUpdate, Dict[str, Any]]] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        comment: Optional[str] = None,
        export_options: Optional[List[Dict[str, Any]]] = None,
        share_objectives: Optional[List[Dict[str, Any]]] = None,
        share_size_limit: Optional[int] = None,
        warn_utilization_percent_threshold: Optional[int] = None,
        smb_browsable: Optional[bool] = None,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        as_model: bool = False
    ) -> Union[Optional[str], Optional[Dict[str, Any]], Optional[ShareView]]:
        """
        Updates a specific share by its identifier.

        Args:
            identifier: Share UUID or name
            share_data: Complete share configuration as a dict or ShareUpdate model
                        (if provided, other params ignored)
            name: Share name
            path: Share path
            comment: Share description
            export_options: List of export option dicts with subnet, accessPermissions, rootSquash, insecure
            share_objectives: List of objective dicts with objective and applicability
            share_size_limit: Size limit in bytes (e.g., 24000000000000 for 24TB)
            warn_utilization_percent_threshold: Warning threshold percentage (e.g., 90)
            smb_browsable: Whether share is SMB browsable
            monitor_task: Whether to monitor the task
            task_timeout_seconds: Task timeout
            as_model: If True, returns a ShareView model instead of raw data
        """
        if share_data is None:
            share_data = self._build_share_data(
                name=name, path=path, comment=comment, export_options=export_options,
                share_objectives=share_objectives, share_size_limit=share_size_limit,
                warn_utilization_percent_threshold=warn_utilization_percent_threshold,
                smb_browsable=smb_browsable
            )
        if isinstance(share_data, HammerspaceBaseModel):
            share_data = share_data.to_api()

        assumed_path = f"/shares/{identifier}"
        logger.warning(f"update_share_by_id: Attempting PUT to '{assumed_path}'.")

        return self.api_client.execute_and_monitor_task(
            path=assumed_path, method="PUT", initial_json_data=share_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds,
            result_model=ShareView if as_model else None
        )

    def _build_share_data(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        comment: Optional[str] = None,
        export_options: Optional[List[Dict[str, Any]]] = None,
        share_objectives: Optional[List[Dict[str, Any]]] = None,
        share_size_limit: Optional[int] = None,
        warn_utilization_percent_threshold: Optional[int] = None,
        smb_browsable: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Builds share data dictionary from individual parameters.

        Delegates to the ShareUpdate model for validation and camelCase
        serialization; only provided fields are included.

        Args:
            name: Share name
            path: Share path
            comment: Share description
            export_options: List of export configurations
            share_objectives: List of share objectives
            share_size_limit: Size limit in bytes
            warn_utilization_percent_threshold: Warning threshold percentage
            smb_browsable: SMB browsable flag

        Returns:
            Dictionary containing share configuration
        """
        share = ShareUpdate(
            name=name,
            path=path,
            comment=comment,
            export_options=export_options,
            share_objectives=share_objectives,
            share_size_limit=share_size_limit,
            warn_utilization_percent_threshold=warn_utilization_percent_threshold,
            smb_browsable=smb_browsable,
        )
        return share.to_api()

    def create_export_option(
        self,
        subnet: str = "*",
        access_permissions: str = "RW", 
        root_squash: bool = False,
        insecure: bool = False
    ) -> Dict[str, Any]:
        """
        Helper method to create export option dictionary.
        
        Args:
            subnet: Network subnet (default "*" for all)
            access_permissions: "RW" or "RO" 
            root_squash: Whether to enable root squashing
            insecure: Whether to allow insecure connections
            
        Returns:
            Export option dictionary
        """
        return {
            "subnet": subnet,
            "accessPermissions": access_permissions,
            "rootSquash": root_squash,
            "insecure": insecure
        }

    def create_share_objective(
        self,
        objective_name: str,
        applicability: str = "TRUE",
        removable: bool = True
    ) -> Dict[str, Any]:
        """
        Helper method to create share objective dictionary.
        
        Args:
            objective_name: Name of the objective (e.g., "keep-online", "optimize-for-capacity")
            applicability: Applicability condition (default "TRUE")
            removable: Whether objective can be removed
            
        Returns:
            Share objective dictionary
        """
        return {
            "objective": {
                "name": objective_name
            },
            "applicability": applicability,
            "removable": removable
        }

    def delete(
        self, identifier: str, 
        delete_snapshots: bool = True,
        monitor_task: bool = True, 
        task_timeout_seconds: int = 300, 
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a specific share by its identifier, optionally deleting snapshots first.

        The plain DELETE (including the post-cascade delete when
        ``delete_snapshots=True``) delegates to the spec-generated typed client
        (``client.generated.shares.delete``) so both entry points share one
        implementation; ``delete_snapshots=True`` only adds the pre-delete
        snapshot cascade on top.

        Args:
            identifier: Share UUID or name
            delete_snapshots: Whether to delete all snapshots before deleting share
            monitor_task: Whether to monitor the task
            task_timeout_seconds: Task timeout
            **kwargs: Additional delete parameters (delete_delay, delete_path)
        """
        # Delete snapshots first if requested
        if delete_snapshots:
            try:
                self._delete_all_share_snapshots(identifier, monitor_task, task_timeout_seconds)
            except Exception as e:
                logger.error(f"Failed to delete snapshots for share '{identifier}': {e}")
                # Continue with share deletion even if snapshot deletion fails

        generated = getattr(self.api_client, "generated", None)
        if generated is not None:
            return generated.shares.delete(
                identifier,
                delete_delay=str(kwargs.get("delete_delay", "0")),
                delete_path=str(kwargs.get("delete_path", True)).lower(),
                monitor_task=monitor_task,
                task_timeout_seconds=task_timeout_seconds,
            )

        # Fallback for api_client doubles without the generated typed layer.
        assumed_path = f"/shares/{identifier}"
        logger.warning(f"delete_share_by_id: Attempting DELETE to '{assumed_path}'.")

        query_params = {}
        query_params["delete-delay"] = str(kwargs.get("delete_delay", "0"))
        query_params["delete-path"] = str(kwargs.get("delete_path", True)).lower()

        return self.api_client.execute_and_monitor_task(
            path=assumed_path, method="DELETE", initial_query_params=query_params,
            initial_headers={"accept": "application/json"},
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def _create_share_snapshots(
        self, 
        share_identifier: str,
        snapshot_schedules: Optional[List[Dict[str, Any]]] = None,
        use_default_plans: bool = True,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300
    ):
        """
        Creates snapshot schedules for a share.
        
        Args:
            share_identifier: Share name or UUID
            snapshot_schedules: Custom snapshot schedule configurations
            use_default_plans: Whether to use default system retention plans
            monitor_task: Whether to monitor tasks
            task_timeout_seconds: Task timeout
        """
        from .share_snapshots import ShareSnapshotsClient
        snapshots_client = ShareSnapshotsClient(self.api_client)
        
        if snapshot_schedules:
            # Create custom snapshot schedules
            for schedule_config in snapshot_schedules:
                schedule_config["share"] = {"name": share_identifier}
                snapshots_client.create_snapshot_schedule(
                    schedule_config, monitor_task, task_timeout_seconds
                )
        elif use_default_plans:
            # Create default snapshot schedules using system retention plans
            default_schedules = self._get_default_snapshot_schedules(share_identifier)
            for schedule_config in default_schedules:
                snapshots_client.create_snapshot_schedule(
                    schedule_config, monitor_task, task_timeout_seconds
                )

    def _get_default_snapshot_schedules(self, share_identifier: str) -> List[Dict[str, Any]]:
        """
        Gets default snapshot schedule configurations based on system retention plans.
        
        Args:
            share_identifier: Share name or UUID
            
        Returns:
            List of default snapshot schedule configurations
        """
        # Get available retention plans
        retention_plans = self._get_snapshot_retention_plans()
        
        default_schedules = []
        
        # Create common snapshot schedules with appropriate retention
        schedule_configs = [
            {
                "name": "daily",
                "cron": "1 0 * * *",  # Daily at 00:01
                "retention_name": "1 week"
            },
            {
                "name": "weekly", 
                "cron": "1 0 * * 1",  # Weekly on Monday at 00:01
                "retention_name": "1 month"
            },
            {
                "name": "monthly",
                "cron": "1 0 1 * *",  # Monthly on 1st at 00:01
                "retention_name": "1 year"
            }
        ]
        
        for config in schedule_configs:
            # Find matching retention plan
            retention_plan = next(
                (plan for plan in retention_plans if plan.get("name") == config["retention_name"]),
                None
            )
            
            if retention_plan:
                schedule_data = {
                    "name": config["name"],
                    "cronExpression": config["cron"],
                    "share": {"name": share_identifier},
                    "retention": {
                        "uuid": retention_plan["uoid"]["uuid"],
                        "name": retention_plan["name"]
                    }
                }
                default_schedules.append(schedule_data)
        
        return default_schedules

    def _get_snapshot_retention_plans(self) -> List[Dict[str, Any]]:
        """
        Gets available snapshot retention plans from the system.
        
        Returns:
            List of available retention plans
        """
        try:
            # This would need to be implemented based on the API endpoint for retention plans
            # For now, return the common ones from the reference material
            return [
                {
                    "uoid": {"uuid": "221c9b5c-4968-49ae-9310-d7357f3244ce"},
                    "name": "1 week",
                    "retentionTime": 604800000
                },
                {
                    "uoid": {"uuid": "ba2bf789-fad7-4ec3-a6fc-64306f699679"},
                    "name": "1 month", 
                    "retentionTime": 2592000000
                },
                {
                    "uoid": {"uuid": "dfbfd8bd-bb27-4056-b5af-8270be76043f"},
                    "name": "1 year",
                    "retentionTime": 31536000000
                }
            ]
        except Exception as e:
            logger.error(f"Failed to get retention plans: {e}")
            return []

    def _delete_all_share_snapshots(
        self, 
        share_identifier: str,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300
    ):
        """
        Deletes all snapshots and snapshot schedules for a share.
        
        Args:
            share_identifier: Share name or UUID
            monitor_task: Whether to monitor tasks
            task_timeout_seconds: Task timeout
        """
        from .share_snapshots import ShareSnapshotsClient
        snapshots_client = ShareSnapshotsClient(self.api_client)
        
        try:
            # Get list of snapshots for the share
            snapshots = snapshots_client.list_share_snapshots_for_share(share_identifier)
            
            if snapshots:
                # Delete each snapshot
                for snapshot_name in snapshots:
                    try:
                        snapshots_client.delete_share_snapshot(
                            share_identifier, snapshot_name, monitor_task, task_timeout_seconds
                        )
                    except Exception as e:
                        logger.error(f"Failed to delete snapshot '{snapshot_name}': {e}")
            
            # Get and delete snapshot schedules
            # This would require getting schedules filtered by share
            # For now, we'll rely on the clear_snapshots parameter in schedule deletion
            
        except Exception as e:
            logger.error(f"Failed to delete snapshots for share '{share_identifier}': {e}")
            raise

    def create_snapshot_schedule_config(
        self,
        name: str,
        cron_expression: str,
        retention_name: str,
        share_identifier: str
    ) -> Dict[str, Any]:
        """
        Helper method to create snapshot schedule configuration.
        
        Args:
            name: Schedule name (e.g., "daily", "weekly")
            cron_expression: Cron expression for schedule
            retention_name: Name of retention plan to use
            share_identifier: Share name or UUID
            
        Returns:
            Snapshot schedule configuration dictionary
        """
        return {
            "name": name,
            "cronExpression": cron_expression,
            "share": {"name": share_identifier},
            "retention": {"name": retention_name}
        }