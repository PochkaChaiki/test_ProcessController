import multiprocessing as mp
import threading as th

class ProcessController:

    def __init__(self):
        self.max_processes = 0
        self.current_tasks = mp.JoinableQueue()
        self.start_new_tasks = True
        self.active_processes = []
        self.run_flag = False
        
    
    def set_max_proc(self, n : int) -> None:
        self.semaphore = th.Semaphore(n)

    def run(self) -> None:
        self.run_flag = True
        main_thread = th.Thread(target=self._start)
        main_thread.start()
        

    def start(self, tasks: list[tuple[callable[..., any], tuple[any, ...]]], max_exec_time : int) -> None:
        if self.start_new_tasks:
            for func, args in tasks:
                self.current_tasks.put((func, args, max_exec_time))

            
    def _start(self) -> None:
        while self.run_flag:
            self.semaphore.acquire()
            if not self.current_tasks.empty():
                func, args, max_exec_time = self.current_tasks.get(block=True)
                new_proc = th.Thread(target=self._run_proc, args=(func, args, max_exec_time))
                new_proc.start()
                self.active_processes.append(new_proc)
            self.semaphore.release(1)
            self.active_processes = [p for p in self.active_processes if p.is_alive()]
        

    def _run_proc(self, func: callable[..., any], args: tuple[any, ...], max_exec_time: int):
        proc = mp.Process(target=func, args = args)
        proc.start()
        proc.join(max_exec_time)

        if proc.is_alive():
            proc.terminate()
            proc.join()
        

    def wait(self) -> None:
        self.current_tasks.join()

    def wait_count(self) -> int:
        return len(self.current_tasks)

    def alive_count(self) -> int:
        return len(self.active_processes)