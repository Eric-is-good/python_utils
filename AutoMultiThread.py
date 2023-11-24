import threading
import time


class AutoMultiThread:
    def __init__(self, thread_num, total_list, break_file="./break.txt", time_interval=10):
        self.thread_num = thread_num
        self.total_list = total_list
        self.length = len(total_list)
        self.break_file = break_file
        self.break_list = []
        self.break_num = 0
        self.count = 0
        self.count_lock = threading.Lock()
        self.break_lock = threading.Lock()
        self.break_file_lock = threading.Lock()
        self.time_interval = time_interval
        self.test_()

    def test_(self):
        with open(self.break_file, 'r') as f:
            pass

    def subtask_thread(self, subtask_list):
        for subtask in subtask_list:
            try:
                self.subtask_function(subtask)
                self.count_lock.acquire()
                self.count += 1
                self.count_lock.release()
            except Exception as e:
                print(e)
                print('subtask failed: ' + subtask)
                self.break_lock.acquire()
                self.break_list.append(str(subtask))
                self.break_num += 1
                self.break_lock.release()
                self.break_file_lock.acquire()
                with open(self.break_file, 'a') as f:
                    f.write(str(subtask))
                    f.write('\n')
                self.break_file_lock.release()

    def count_num(self):
        while True:
            self.count_lock.acquire()
            print('finished: ' + str(self.count) + '/' + str(self.length) +
                  "=" + str(self.count / self.length * 100) + '%')
            self.count_lock.release()
            time.sleep(self.time_interval)
            if self.count + self.break_num == self.length:
                print("success :" + str(self.count) + ", failed: " + str(self.break_num))
                break

    def run(self):
        print('total: ' + str(self.length))
        print('thread: ' + str(self.thread_num))
        print('time interval: ' + str(self.time_interval))
        print('break file: ' + self.break_file)
        print('start')
        t1 = threading.Thread(target=self.count_num, )
        t1.start()
        thread_list = []
        for i in range(self.thread_num):
            t = threading.Thread(target=self.subtask_thread,
                                 args=(self.total_list[i::self.thread_num],))
            thread_list.append(t)
            t.start()

    def subtask_function(self, single_subtask):
        raise NotImplementedError
