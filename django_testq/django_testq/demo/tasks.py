# tasks.py
from django_q.tasks import async_task, schedule
from django_q.models import Schedule
import json
from datetime import timedelta, datetime
import time

def check_async_process(process_id):
    """
    Helper function to check status of an async process
    Replace this with your actual implementation
    """
    # This is a placeholder - replace with actual code to check your async process
    # For example, calling an API, checking a database, etc.
    
    # For demonstration purposes, let's pretend we randomly get a result sometimes
    import random
    if random.random() < 0.2:  # 20% chance of success
        return json.dumps({
            "status": "completed",
            "process_id": process_id,
            "data": {"key1": "value1", "key2": "value2"}
        })
    return None



def task_a(key, param2):
    """
    Task A: Takes parameters, does some work, and returns a string
    """
    # Do something with parameters
    result = f"Processed {key} and {param2}"

    time.sleep(2)  # Simulate a long-running task
    
    # Queue Task B with the result from Task A
    async_task('demo.tasks.task_b', result, key, group=f'task_b_for_{key}')
    # async_task('demo.tasks.task_b', result, param2, hook='demo.tasks.task_b_callback')
    
    return result


def task_b(result_from_a, key):
    """
    Task B: Takes the returned string from Task A and additional parameters
    """
    # Do something with the result from Task A and param3
    processed_data = f"{result_from_a} with {key}"

    time.sleep(2)  # Simulate a long-running task
    
    # Set up Task C to run every 10 seconds
    # First, ensure any existing schedule for this task_id is deleted
    # Schedule.objects.filter(name='task_c_scheduler').delete()
    
    # Schedule Task C to run every 10 seconds
    schedule('demo.tasks.task_c',
             key,
             name=f'task_c_for_{key}',
             schedule_type=Schedule.MINUTES,
             minutes=5/60,  # Every 10 seconds (10/60 minutes)
             repeats=5,  # Repeat up to 5 times
            )
    
    return processed_data


# def task_b_callback(task):
#     """
#     Callback function for Task B (optional)
#     Automatically called after Task B completes
#     """
#     if task.success:
#         print(f"Task B completed successfully with result: {task.result}")
#     else:
#         print(f"Task B failed with error: {task.exception}")


def task_c(key):
    """
    Task C: Checks an async process until it has a JSON result
    Runs every 10 seconds due to scheduling
    """
    # Check some external async process
    json_result = check_async_process(key)
    
    # If we have a result, stop the recurring task and queue Task D
    if json_result:
        # Cancel the recurring Task C
        Schedule.objects.filter(name=f'task_c_for_{key}').delete()
        
        # Queue Task D with the JSON result
        async_task('demo.tasks.task_d', json_result, group=f'task_d_for_{key}')
        
        return json_result
    
    # If no result yet, we return None and the scheduled task will run again
    return None



def task_d(json_result):
    """
    Task D: Processes the JSON from Task C
    """
    # Parse the JSON string to a Python dictionary if it's a string
    if isinstance(json_result, str):
        data = json.loads(json_result)
    else:
        data = json_result
    
    # Process the JSON data
    processed_result = f"Processed JSON with keys: {', '.join(data.keys())}"
    
    # Do something with the processed data
    # ...
    
    return processed_result