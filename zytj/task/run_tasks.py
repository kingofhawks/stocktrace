if __name__ =='__main__':
    from tasks import add
    result = add.delay(4,4)
    print result
    print(result.backend)
    print result.ready()
    #TODO get result timeout?
    print (result.get(timeout=10))
