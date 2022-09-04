import asyncio
import time
responses = [1, 2, 3]

  

async def main():
    
    
    print("Hello")
    task = asyncio.create_task(foo("x"))
    task_2 = asyncio.create_task(funcer())
    
    await asyncio.gather(task, task_2)
    await asyncio.sleep(1)
    print("Finished")
    await task
    
async def funcer():
    async for response in it:
        # Sleep for a second
        print(response)
        await asyncio.sleep(5)  
        
async def foo(name):
    async for response in it_2:
        # Sleep for a second
        print(str(response) + 'foo')
        await asyncio.sleep(5)    


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

x = [1, 2, 3]
it = AsyncIterator(x)
it_2 = AsyncIterator(x)
    
asyncio.run(main())