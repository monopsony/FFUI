import aiohttp
import asyncio
import time

start_time = time.time()

N = 0


async def get_pokemon(sem, session, url):
    global N
    async with session.get(url) as resp:
        await sem.acquire()
        await asyncio.sleep(0.3)
        pokemon = await resp.json()
        sem.release()
        for i in range(1000):
            N += 1
        print(N)
        return pokemon["name"]


async def main():
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for number in range(1, 151):
            url = f"https://pokeapi.co/api/v2/pokemon/{number}"
            tasks.append(asyncio.ensure_future(get_pokemon(sem, session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print(pokemon)


# https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
