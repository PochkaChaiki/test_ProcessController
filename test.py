from collections import deque

class ProcessController:

    def __init__(self):
        self.max_proc = 0
        self.tasks = deque()
        self.start_new_tasks = True
        self.processes = []
    
    def set_max_proc(self, n : int) -> None:
        self.max_proc = n

    def start(self, tasks: list[tuple[callable[..., any], tuple[any, ...]]], max_exec_time : int) -> None:
        self.tasks.extend([(func, args, max_exec_time) for func, args in tasks])
            
    def _start(self) -> None:
        pass

    def wait(self) -> None:
        self.start_new_tasks = False

    def wait_count(self) -> int:
        return len(self.tasks)

    def alive_count(self) -> int:
        return self.active_count