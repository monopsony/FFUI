import aiohttp, asyncio

UNIVERSALIS_BASE_URL = "https://universalis.app/api"


class Connector:
    def __init__(self):
        super().__init__()
        self.eventSubscribe("CLIENT_INIT", self.initializeConnector)

    def initializeConnector(self):
        nSemaphore = self.getPara("nSemaphores")
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
        async with aiohttp.ClientSession() as session:
            await self.semaphore.acquire()
            r = await session.get(query)
            if r.status == 200:
                ret = await r.json()
            else:
                print(f"Status code {r.status} for query {query}. Skipping")

            async with self.asyncioLock:
                self.currentProgress += 1

            self.semaphore.release()
        self.currentCallback()
        return ret

    def gatherUniversalisQueries(self, lst, callback=None):
        if type(lst) == tuple:
            lst = [lst]
        t = []
        for item, world in lst:
            t.append(asyncio.ensure_future(self.universalisQuery(world, item)))

        data = self.gatherTasks(t, callback=callback)
        return data

    def gatherDefaultCallback(self):
        self.eventPush("CLIENT_PROGRESS", self.currentProgress, self.currentMax)

    def printProgress(self):
        print(f"{self.currentProgress}/{self.currentMax}")

    progressText = None
    currentMax = 0
    currentProgress = 0

    def gatherTasks(self, tasks, callback=None):
        self.currentProgress = 0
        self.currentMax = len(tasks)
        self.progressText = "Gathering data"

        if callback is None:
            self.currentCallback = self.gatherDefaultCallback
        else:
            self.currentCallback = callback

        a = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        return a


if __name__ == "__main__":
    c = Connector()

    t = []
    for i in range(15):
        t.append(asyncio.ensure_future(c.universalisQuery("Shiva", "5510")))

    a = c.gatherTasks(t, callback=c.printProgress)
    print("DONE", len(a))

    # a = asyncio.run(c.universalis_query("Shiva", "5510"))
    # print(a)
