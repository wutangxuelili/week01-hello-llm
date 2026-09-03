import asyncio
import functools
import time

from llm_client import LLMClient

# 异步测试
client = LLMClient()
semaphore = asyncio.Semaphore(3)


async def ask(prompt, idx):
    start = time.time()
    loop = asyncio.get_running_loop()
    async with semaphore:
        reply = await loop.run_in_executor(
            None,
            functools.partial(
                client.chat,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            ),
        )
    elapsed = time.time() - start
    short = (reply or "")[:30]
    print(f"[{idx}/10] 完成，耗时 {elapsed:.2f}s，回复：{short}...")
    return reply


async def main():
    prompts = [
        f"请用一句话解释什么是 {t}"
        for t in [
            "AI",
            "Python",
            "Docker",
            "Redis",
            "Git",
            "API",
            "JSON",
            "SQL",
            "HTTP",
            "LLM",
        ]
    ]
    tasks = [ask(p, i + 1) for i, p in enumerate(prompts)]
    results = await asyncio.gather(*tasks)
    print(f"\n全部完成！共 {len(results)} 个回复")


if __name__ == "__main__":
    asyncio.run(main())
