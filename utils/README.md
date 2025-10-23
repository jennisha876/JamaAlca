# Utils Module

This directory contains utility functions and helper classes used throughout the JamaAlca application.

## Available Utilities

1. `notifications.py` - Notification system
   ```python
   from utils.notifications import NotificationManager, NotificationCenter

   # Usage
   notif_manager = NotificationManager(root)
   notif_manager.post("Title", "Message", "Category")
   ```

### Notification Categories
- Weather
- Disease
- Market
- Sustainability
- System

### Notification Features
- Toast notifications
- Notification center
- Category filtering
- Read/unread tracking

## Best Practices

1. Keep utility functions focused and single-purpose
2. Include proper error handling
3. Add documentation for complex functions
4. Write unit tests for critical utilities

## Adding New Utilities

When adding new utility functions:
1. Create a new file for related functions
2. Update this README
3. Add proper documentation
4. Include usage examples