"""
Example usage scripts for Coupa SFTP Integration
"""

import json
from coupa_sftp_integration import CoupaSFTPIntegration
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_file: str = 'config.json') -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
        logger.info("Please create config.json based on config.example.json")
        raise


def example_export_requisitions():
    """Example: Export requisitions from Coupa."""
    config = load_config()
    integration = CoupaSFTPIntegration(config['sftp'])
    
    try:
        if not integration.connect():
            return
        
        # Download all requisition files
        exported_files = integration.export_requisitions(
            remote_export_path=config['paths']['remote_export_path'],
            file_pattern=config['file_patterns'].get('export_filter')
        )
        
        # Process each exported file
        all_requisitions = []
        for file_path in exported_files:
            if file_path.endswith('.csv'):
                requisitions = integration.parse_requisition_csv(file_path)
                all_requisitions.extend(requisitions)
                logger.info(f"Processed {len(requisitions)} requisitions from {file_path}")
            elif file_path.endswith('.xml'):
                requisitions = integration.parse_requisition_xml(file_path)
                all_requisitions.extend(requisitions)
                logger.info(f"Processed {len(requisitions)} requisitions from {file_path}")
        
        logger.info(f"Total requisitions exported: {len(all_requisitions)}")
        
        # Do something with the requisitions (save to database, process, etc.)
        return all_requisitions
        
    finally:
        integration.disconnect()


def example_import_requisitions():
    """Example: Import requisitions to Coupa."""
    config = load_config()
    integration = CoupaSFTPIntegration(config['sftp'])
    
    try:
        if not integration.connect():
            return
        
        # Create sample requisition data
        # In real scenario, this would come from your system/database
        requisitions = [
            {
                'requisition_number': f'REQ-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                'status': 'Draft',
                'requester_email': 'requester@company.com',
                'ship_to_attention': 'Department Manager',
                'ship_to_address': '123 Business Ave',
                'ship_to_city': 'San Francisco',
                'ship_to_state': 'CA',
                'ship_to_postal_code': '94105',
                'ship_to_country': 'US',
                'line_number': 1,
                'description': 'Laptop Computer',
                'quantity': 1,
                'unit_price': 1200.00,
                'currency': 'USD',
                'commodity_name': 'Computer Equipment',
                'account_code': '60100',
                'department': 'IT',
                'supplier_name': 'Tech Supplier Inc',
                'supplier_number': 'SUP-12345',
                'contract_number': 'CNT-2024-001',
                'need_by_date': '2025-12-15'
            },
            {
                'requisition_number': f'REQ-{datetime.now().strftime("%Y%m%d-%H%M%S")}-002',
                'status': 'Draft',
                'requester_email': 'requester@company.com',
                'ship_to_attention': 'Department Manager',
                'ship_to_address': '123 Business Ave',
                'ship_to_city': 'San Francisco',
                'ship_to_state': 'CA',
                'ship_to_postal_code': '94105',
                'ship_to_country': 'US',
                'line_number': 2,
                'description': 'Monitor 27 inch',
                'quantity': 2,
                'unit_price': 350.00,
                'currency': 'USD',
                'commodity_name': 'Computer Equipment',
                'account_code': '60100',
                'department': 'IT',
                'supplier_name': 'Tech Supplier Inc',
                'supplier_number': 'SUP-12345',
                'contract_number': 'CNT-2024-001',
                'need_by_date': '2025-12-15'
            }
        ]
        
        # Choose file format based on config
        file_format = config['processing'].get('file_format', 'csv')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%SZ')
        
        if file_format == 'csv':
            file_path = integration.create_requisition_csv(
                requisitions=requisitions,
                output_file=f'RequisitionHeader_{timestamp}.csv'
            )
        else:
            file_path = integration.create_requisition_xml(
                requisitions=requisitions,
                output_file=f'RequisitionHeader_{timestamp}.xml'
            )
        
        logger.info(f"Created requisition file: {file_path}")
        
        # Upload to Coupa
        success = integration.import_requisitions(
            local_files=[file_path],
            remote_import_path=config['paths']['remote_import_path']
        )
        
        if success:
            logger.info("Successfully imported requisitions to Coupa")
        else:
            logger.error("Failed to import requisitions")
        
        return success
        
    finally:
        integration.disconnect()


def example_batch_process():
    """Example: Continuous batch processing - export, process, and import."""
    config = load_config()
    integration = CoupaSFTPIntegration(config['sftp'])
    
    try:
        if not integration.connect():
            return
        
        logger.info("Starting batch processing...")
        
        # Step 1: Export requisitions from Coupa
        logger.info("Step 1: Exporting requisitions...")
        exported_files = integration.export_requisitions(
            remote_export_path=config['paths']['remote_export_path']
        )
        
        # Step 2: Process exported requisitions
        logger.info("Step 2: Processing requisitions...")
        processed_requisitions = []
        
        for file_path in exported_files:
            if file_path.endswith('.csv'):
                requisitions = integration.parse_requisition_csv(file_path)
            elif file_path.endswith('.xml'):
                requisitions = integration.parse_requisition_xml(file_path)
            else:
                continue
            
            # Apply business logic transformations
            for req in requisitions:
                # Example: Add custom fields, validate data, enrich, etc.
                req['processed_date'] = datetime.now().isoformat()
                req['processed'] = True
                processed_requisitions.append(req)
        
        logger.info(f"Processed {len(processed_requisitions)} requisitions")
        
        # Step 3: Import processed requisitions (if needed)
        if processed_requisitions:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = integration.create_requisition_csv(
                requisitions=processed_requisitions,
                output_file=f'processed_requisitions_{timestamp}.csv'
            )
            logger.info(f"Created processed file: {output_file}")
        
        logger.info("Batch processing completed")
        
    finally:
        integration.disconnect()


def example_scheduled_sync():
    """Example: Scheduled synchronization between systems."""
    import time
    
    config = load_config()
    sync_interval = 300  # 5 minutes
    
    logger.info(f"Starting scheduled sync (every {sync_interval} seconds)...")
    
    while True:
        try:
            logger.info("=== Starting sync cycle ===")
            
            # Export from Coupa
            exported = example_export_requisitions()
            logger.info(f"Exported {len(exported) if exported else 0} requisitions")
            
            # Here you would:
            # 1. Process the exported requisitions
            # 2. Update your local database
            # 3. Prepare new requisitions to import
            # 4. Import to Coupa
            
            logger.info("=== Sync cycle completed ===")
            
        except Exception as e:
            logger.error(f"Error during sync cycle: {str(e)}")
        
        # Wait for next cycle
        logger.info(f"Waiting {sync_interval} seconds until next sync...")
        time.sleep(sync_interval)


if __name__ == '__main__':
    # Uncomment the example you want to run
    
    # Example 1: Export requisitions
    # example_export_requisitions()
    
    # Example 2: Import requisitions
    example_import_requisitions()
    
    # Example 3: Batch processing
    # example_batch_process()
    
    # Example 4: Scheduled sync (runs continuously)
    # example_scheduled_sync()
    
    print("Please uncomment one of the examples in __main__ to run")
