import sys
import traceback

'''
Finally executes even after return, break or continue!!!
'''

try:
    x = 1/0
except:
    print(sys.exc_info()[0])
    print(traceback.print_exc(file=sys.stdout))


try:
    f = open('my_file.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS Error {0}".format(err))
except ValueError:
    print("Could not convert data to integer")
except:
    print("Unexcepted error:", sys.exc_info()[0])
    raise
else:
    print("No exception raised")
finally:
    print("I do some clean up")


try:
    raise Exception('spam', 'eggs')
except Exception as inst:
    print(inst.args)


'''
USER DEFINED EXCEPTIONS
'''
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    
try:
    raise MyError(2*2)
except MyError as e:
    print(e.value)


