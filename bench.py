import gc, timeit, tracemalloc
import operator


def bench(algo_list: list, algo_args: list, repeat_count: int) -> list:
    # NOTE: 对算法的评测必须一个一个来，不能用 map 等操作
    # 返回 (_qualname__, time, memory) 构成的 list

    result = []

    for algo in algo_list:
        avg_time = 0.0

        for j in range(repeat_count):
            start_time = timeit.default_timer()
            algo(*algo_args)
            end_time = timeit.default_timer()

            # 回收垃圾，消除垃圾回收的影响
            gc.collect()

            avg_time += float(end_time - start_time)

        # 最后再除，避免浮点误差
        avg_time /= 5

        avg_memory = 0

        tracemalloc.start()

        for j in range(repeat_count):
            algo(*algo_args)

            # 得到内存使用峰值，以字节为单位
            memory_diff = tracemalloc.get_traced_memory()[1]

            # 回收垃圾，消除垃圾回收的影响
            gc.collect()

            avg_memory += memory_diff

        # 最后再除，减少浮点误差，同时单位转换成 MB
        avg_memory /= (1024 * 1024)
        avg_memory /= repeat_count

        tracemalloc.stop()

        result.append((algo.__qualname__, avg_time, avg_memory))

    return result


def bench_output(algo_list: list, algo_args: list, repeat_count: int):
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x,
                        bench(algo_list, algo_args, repeat_count))))
