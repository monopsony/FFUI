import aiohttp, asyncio
import logging, time

logger = logging.getLogger(__name__)
UNIVERSALIS_BASE_URL = "https://universalis.app/api"


class Connector:
    def __init__(self):
        super().__init__()
        self.eventSubscribe("CLIENT_INIT", self.initializeConnector)

    def initializeConnector(self):
        nSemaphore = self.getConfig("nSemaphores")
        self.asyncioEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.asyncioEventLoop)
        self.semaphore = asyncio.Semaphore(nSemaphore)
        self.asyncioLock = asyncio.Lock()

    async def universalisQuery(self, *args):
        args = [str(x) for x in args]
        lst = [UNIVERSALIS_BASE_URL] + list(args)
        query = "/".join(lst)
        return await self.query(query, "UNIVERSALIS")

    async def query(self, query, raw=False):
        ret = None
        retry = False
        async with aiohttp.ClientSession() as session:
            await self.semaphore.acquire()
            self.setProgress(progressText=f"Querying {query}")
            r = await session.get(query)
            if r.status == 200:
                ret = await r.json()
            elif r.status == 404:
                logger.error(f"Status code 404 for query {query}. Skipping")
            elif r.status == 429:
                logger.warn(
                    f"Status code 429 for query {query}. If this happens frequently, consider increasing sleep time or decreasing the number of semaphores."
                )
                retry = True
            else:
                logger.error(f"Status code {r.status} for query {query}. Skipping")

            async with self.asyncioLock:
                if not retry:
                    self.currentProgress += 1

            if not retry:
                self.semaphore.release()

        if retry:
            self.setProgress(
                progressText=f"Sleeping 5s to wait for Universalis servers"
            )
            await asyncio.sleep(5)
            self.semaphore.release()
            return await self.query(query, raw=raw)

        return ret

    def gatherUniversalisQueries(self, lst, callback=None):
        if type(lst) == tuple:
            lst = [lst]
        t = []
        for item, world in lst:
            t.append(asyncio.ensure_future(self.universalisQuery(world, item)))

        data = self.gatherTasks(t, callback=callback)
        # Nones happen for 404 mostly (i.e. item has no page in universalis/is not sellable)
        data = [x if x is not None else {} for x in data]
        return data

    def gatherTasks(self, tasks, callback=None):
        # self.currentProgress = 0
        # self.currentMax = len(tasks)
        # self.progressText = "Gathering data"
        self.setProgress(
            currentProgress=0, currentMax=len(tasks), progressText=f"Gatering data"
        )

        a = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        return a


if __name__ == "__main__":
    c = Connector()

    t = []
    for i in range(15):
        t.append(asyncio.ensure_future(c.universalisQuery("Shiva", "5510")))

    a = c.gatherTasks(t, callback=c.printProgress)
    print("DONE", len(a))
