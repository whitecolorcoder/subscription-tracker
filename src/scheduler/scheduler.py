import logging
import threading
import time
from typing import Optional, Callable, Any, Dict, List
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import uuid

from src.services.expenses_counting import build_class

logger = logging.getLogger(__name__)


class Job:
    """Represents a scheduled job"""

    def __init__(self, job_id: str, func: Callable, trigger_type: str, **kwargs):
        self.job_id = job_id
        self.func = func
        self.trigger_type = trigger_type  # 'interval', 'cron', 'date'
        self.kwargs = kwargs
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.is_paused = False
        self.max_instances = kwargs.get('max_instances', 1)
        self.running_instances = 0

        self._calculate_next_run()

    def _calculate_next_run(self):
        """Calculate the next run time based on trigger type"""
        now = datetime.now()

        if self.trigger_type == 'interval':
            seconds = self.kwargs.get('seconds', 0)
            minutes = self.kwargs.get('minutes', 0)
            hours = self.kwargs.get('hours', 0)
            days = self.kwargs.get('days', 0)

            interval = timedelta(
                seconds=seconds,
                minutes=minutes,
                hours=hours,
                days=days
            )

            if self.last_run:
                self.next_run = self.last_run + interval
            else:
                self.next_run = now + interval

        elif self.trigger_type == 'cron':
            # Simple cron implementation
            hour = self.kwargs.get('hour')
            minute = self.kwargs.get('minute', 0)
            second = self.kwargs.get('second', 0)

            if hour is not None:
                next_run = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
                if next_run <= now:
                    next_run += timedelta(days=1)
                self.next_run = next_run
            else:
                self.next_run = now + timedelta(minutes=1)  # Default to 1 minute

        elif self.trigger_type == 'date':
            self.next_run = self.kwargs.get('run_date')

    def should_run(self) -> bool:
        """Check if the job should run now"""
        if self.is_paused or not self.next_run:
            return False

        if self.running_instances >= self.max_instances:
            return False

        return datetime.now() >= self.next_run

    def run(self):
        """Execute the job"""
        try:
            self.running_instances += 1
            self.last_run = datetime.now()
            logger.info(f"Executing job: {self.job_id}")
            self.func()

            # Recalculate next run for recurring jobs
            if self.trigger_type in ['interval', 'cron']:
                self._calculate_next_run()
            else:
                # One-time job, mark as completed
                self.next_run = None

        except Exception as e:
            logger.error(f"Error executing job {self.job_id}: {e}")
        finally:
            self.running_instances -= 1


class SchedulerService:
    """
    Synchronous scheduler service for managing scheduled tasks
    """

    def __init__(self, max_workers: int = 5):
        """
        Initialize the scheduler service

        Args:
            max_workers: Maximum number of worker threads
        """
        self.jobs: Dict[str, Job] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler started successfully")

    def shutdown(self):
        """Shutdown the scheduler"""
        if not self.running:
            return

        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)

        self.executor.shutdown(wait=True)
        logger.info("Scheduler shutdown successfully")

    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                with self._lock:
                    jobs_to_run = [job for job in self.jobs.values() if job.should_run()]

                for job in jobs_to_run:
                    if not self.running:
                        break
                    self.executor.submit(job.run)

                time.sleep(1)  # Check every second

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")

    def add_interval_job(
        self,
        func: Callable,
        seconds: Optional[int] = None,
        minutes: Optional[int] = None,
        hours: Optional[int] = None,
        days: Optional[int] = None,
        job_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Add a job that runs at regular intervals

        Args:
            func: Function to execute
            seconds: Interval in seconds
            minutes: Interval in minutes
            hours: Interval in hours
            days: Interval in days
            job_id: Unique job identifier
            **kwargs: Additional job parameters

        Returns:
            Job ID
        """
        if job_id is None:
            job_id = str(uuid.uuid4())

        job = Job(
            job_id=job_id,
            func=func,
            trigger_type='interval',
            seconds=seconds or 0,
            minutes=minutes or 0,
            hours=hours or 0,
            days=days or 0,
            **kwargs
        )

        with self._lock:
            self.jobs[job_id] = job

        logger.info(f"Added interval job: {job_id}")
        return job_id

    def add_cron_job(
        self,
        func: Callable,
        cron_expression: str = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        day: Optional[int] = None,
        month: Optional[int] = None,
        day_of_week: Optional[int] = None,
        job_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Add a job that runs on a cron schedule (simplified)

        Args:
            func: Function to execute
            cron_expression: Cron expression string (not implemented)
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
            second: Second to run (0-59)
            day: Day of month to run (1-31) (not implemented)
            month: Month to run (1-12) (not implemented)
            day_of_week: Day of week to run (0-6, Monday=0) (not implemented)
            job_id: Unique job identifier
            **kwargs: Additional job parameters

        Returns:
            Job ID
        """
        if job_id is None:
            job_id = str(uuid.uuid4())

        job = Job(
            job_id=job_id,
            func=func,
            trigger_type='cron',
            hour=hour,
            minute=minute,
            second=second,
            day=day,
            month=month,
            day_of_week=day_of_week,
            **kwargs
        )

        with self._lock:
            self.jobs[job_id] = job

        logger.info(f"Added cron job: {job_id}")
        return job_id

    def add_date_job(
        self,
        func: Callable,
        run_date: datetime,
        job_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Add a job that runs once at a specific date/time

        Args:
            func: Function to execute
            run_date: When to run the job
            job_id: Unique job identifier
            **kwargs: Additional job parameters

        Returns:
            Job ID
        """
        if job_id is None:
            job_id = str(uuid.uuid4())

        job = Job(
            job_id=job_id,
            func=func,
            trigger_type='date',
            run_date=run_date,
            **kwargs
        )

        with self._lock:
            self.jobs[job_id] = job

        logger.info(f"Added date job: {job_id} for {run_date}")
        return job_id

    def remove_job(self, job_id: str) -> bool:
        """
        Remove a job by ID

        Args:
            job_id: Job identifier

        Returns:
            True if job was removed, False if not found
        """
        with self._lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                logger.info(f"Removed job: {job_id}")
                return True

        logger.warning(f"Job not found: {job_id}")
        return False

    def pause_job(self, job_id: str) -> bool:
        """
        Pause a job by ID

        Args:
            job_id: Job identifier

        Returns:
            True if job was paused, False if not found
        """
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id].is_paused = True
                logger.info(f"Paused job: {job_id}")
                return True

        logger.warning(f"Job not found: {job_id}")
        return False

    def resume_job(self, job_id: str) -> bool:
        """
        Resume a paused job by ID

        Args:
            job_id: Job identifier

        Returns:
            True if job was resumed, False if not found
        """
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id].is_paused = False
                logger.info(f"Resumed job: {job_id}")
                return True

        logger.warning(f"Job not found: {job_id}")
        return False

    def get_jobs(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled jobs

        Returns:
            List of job information dictionaries
        """
        with self._lock:
            jobs_info = []
            for job in self.jobs.values():
                jobs_info.append({
                    'id': job.job_id,
                    'trigger_type': job.trigger_type,
                    'next_run': job.next_run,
                    'last_run': job.last_run,
                    'is_paused': job.is_paused,
                    'running_instances': job.running_instances
                })
            return jobs_info

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific job by ID

        Args:
            job_id: Job identifier

        Returns:
            Job information dictionary or None if not found
        """
        with self._lock:
            if job_id in self.jobs:
                job = self.jobs[job_id]
                return {
                    'id': job.job_id,
                    'trigger_type': job.trigger_type,
                    'next_run': job.next_run,
                    'last_run': job.last_run,
                    'is_paused': job.is_paused,
                    'running_instances': job.running_instances
                }
        return None


# Global scheduler instance
scheduler_service = SchedulerService()


# Example usage and helper functions
def example_task():
    """Example scheduled task"""
    logger.info(f"Example task executed at {datetime.now()}")


def subscription_reminder_task():
    """Task for subscription reminders"""
    logger.info("Checking for subscription reminders...")
    # Add your subscription reminder logic here


def trial_expiry_check_task():
    """Task for checking trial expiries"""
    logger.info("Checking for trial expiries...")
    # Add your trial expiry logic here


def setup_default_jobs():
    """Setup default scheduled jobs"""
    try:
        # Create the expense counter instance
        expense_counter = build_class()

        # Example: Check for subscription reminders every hour
        scheduler_service.add_interval_job(
            expense_counter,  # Pass the callable instance
            minutes=1,
            job_id="subscription_reminders"
        )

        # Example: Check for trial expiries daily at 9:00 AM
        scheduler_service.add_cron_job(
            expense_counter,  # Pass the callable instance
            hour=9,
            minute=0,
            job_id="trial_expiry_check"
        )

        logger.info("Default jobs setup completed")

    except Exception as e:
        logger.error(f"Failed to setup default jobs: {e}")


def initialize_scheduler(max_workers: int = 5):
    """
    Initialize and start the scheduler

    Args:
        max_workers: Maximum number of worker threads
    """
    global scheduler_service

    scheduler_service = SchedulerService(max_workers)
    scheduler_service.start()
    setup_default_jobs()


def cleanup_scheduler():
    """Cleanup scheduler on application shutdown"""
    scheduler_service.shutdown()

if __name__=='__main__':
    import traceback
    try:
        initialize_scheduler()
    except Exception as e:
        print(traceback.print_exc(e))
