import asyncio
import uuid
from typing import Dict, Optional
from datetime import datetime

class Job:
    def __init__(self, job_id: str, message: str):
        self.job_id = job_id
        self.message = message
        self.status = "queued"
        self.created_at = datetime.now()
        self.result = None

class QueueService:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.processing = False
    
    def create_job(self, message: str) -> str:
        """Create a new job and add to queue"""
        job_id = str(uuid.uuid4())
        job = Job(job_id, message)
        self.jobs[job_id] = job
        asyncio.create_task(self.queue.put(job))
        return job_id
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return self.jobs.get(job_id)
    
    async def process_queue(self):
        """Process jobs from queue (background task)"""
        while True:
            job = await self.queue.get()
            job.status = "processing"
            # Job processing happens in the SSE endpoint
            self.queue.task_done()

queue_service = QueueService()
