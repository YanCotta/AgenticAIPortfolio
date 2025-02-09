import asyncio
import time
from agents.doc_ingest_agent import DocumentIngestionAgent
from agents.summarizer_agent import SummarizerAgent
from agents.email_agent import EmailAgent

class TaskManager:
    def __init__(self):
        self.ingestion_agent = DocumentIngestionAgent()
        self.summarizer_agent = SummarizerAgent()
        self.email_agent = EmailAgent()
    
    async def execute_pipeline(self, file_path, priority=5):
        start_time = time.time()
        try:
            print("📂 Extracting document...")
            # Running synchronous ingestion in executor
            doc_data = await asyncio.get_event_loop().run_in_executor(None, self.ingestion_agent.process, file_path)
            if not doc_data:
                # Error recovery: stop if ingestion fails
                print("❌ Ingestion failed. Skipping pipeline.")
                return

            print("📝 Summarizing content...")
            summary_data = await self.summarizer_agent.process(doc_data)
            if not summary_data:
                print("❌ Summarization failed. Skipping pipeline.")
                return

            print("📧 Drafting email...")
            # Running synchronous email drafting in executor
            email_data = await asyncio.get_event_loop().run_in_executor(None, self.email_agent.process, summary_data)
            if not email_data:
                print("❌ Email drafting failed. Skipping pipeline.")
                return

            if priority < 5:
                print("⚡ High priority task processed.")
            
            elapsed = time.time() - start_time
            print("\n✅ Generated Email:")
            print(f"Subject: {email_data['subject']}")
            print(f"Body:\n{email_data['body']}")
            print(f"\n⏱ Pipeline executed in {elapsed:.2f} seconds.")

        except Exception as e:
            print(f"❌ Pipeline execution error: {str(e)}")

    async def run_pipeline_queue(self, tasks):
        # tasks: List of tuples (priority, file_path)
        queue = asyncio.PriorityQueue()
        for priority, file_path in tasks:
            await queue.put((priority, file_path))
        total = queue.qsize()
        completed = 0
        
        async def worker():
            nonlocal completed
            while not queue.empty():
                priority, file_path = await queue.get()
                print(f"\n🔄 Processing {file_path} with priority {priority} ({completed+1}/{total})")
                await self.execute_pipeline(file_path, priority)
                completed += 1
                queue.task_done()
        
        # Launch concurrent workers (e.g., 3 concurrent tasks)
        workers = [asyncio.create_task(worker()) for _ in range(3)]
        await queue.join()
        for w in workers:
            w.cancel()
