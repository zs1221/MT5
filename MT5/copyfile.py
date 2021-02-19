import os
import multiprocessing
import time


def copy_file(q, file, old, new):
    old_f = open(old + '/' + file, 'rb')
    con_read = old_f.read()
    old_f.close()

    new_f = open(new + '/' + file, 'wb')
    new_f.write(con_read)
    new_f.close()
    q.put(file)


def main():
    old_f_name = input('请输入要拷贝的文件: ')
    try:
        new_file_name = old_f_name + '附件s'
        os.mkdir(new_file_name)
    except Exception as e:
        pass

    file_names = os.listdir(old_f_name)

    po = multiprocessing.Pool(5)

    q = multiprocessing.Manager().Queue()

    for file_name in file_names:
        po.apply_async(copy_file, args=(q, file_name, old_f_name, new_file_name))

    po.close()

    all_file = len(file_names)
    ct = 0

    while True:
        time.sleep(0.5)
        file_name = q.get()
        ct += 1
        print('\r%s 已经完成 ： %.2f %%' % (file_name, ct*100/all_file), end=' ')

        if ct >= all_file:
            print()
            break





if __name__ == '__main__':
    main()



