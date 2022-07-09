def apple():
  a = 'apple'
  yield a
  
  print('banana')

def hi_apple():
  print(apple())

hi_apple()