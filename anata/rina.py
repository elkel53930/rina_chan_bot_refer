from anata import *

#countdown()
set_exp(eyes['normal'] + mouth['normal'])
talk("スタート",eyes['normal'])
s(5)
move(0.7, [0,0,-0.2])
move_add(0.7, [0,0,0])
talk("こんにちは。まだちょっと声が変だね", eyes['normal'])
s(1)
move(2, [0,0.2,0])
talk("でも、少しだけ話せるようになったよ", eyes['normal'])
s(1)
move(0.6, [-0.05,-0.2,0])
move_add(0.6, [0.05,0.2,0])
move_add(0.6, [-0.05,-0.2,0])
move_add(0.6, [0.05,0.2,0])
talk("早くみんなに会いたいな", eyes['batsu'])
s(0.6)
move(0.3, [-0.2,0.2,-0.2])
s(0.1)
set_exp(eyes['wink'] + mouth['normal'])
s(3)

end_script()
