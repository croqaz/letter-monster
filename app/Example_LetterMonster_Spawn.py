
import os, sys
sys.path.insert( 0, os.getcwd() )
from _letter_monster import LetterMonster

#

lm = LetterMonster()
lm.DEBUG = True

print( 'Spawning...\n' )

lm.Spawn( lmgl='test.lmgl', out='txt' )

#

print( 'Finished.\n' )
os.system( 'pause' )

#