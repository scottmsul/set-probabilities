from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def plot_results(games):
    games = games.loc[(games['shown']==12)&(games['round']<20),:]
    games['noset'] = games['sets']==0
    chance_noset = games.groupby('round')['noset'].mean()
    x = range(1, len(chance_noset)+1)
    y = chance_noset.values
    plt.plot(x,y,'b-o',label='Distribution from 100,000 games')
    plt.plot(x,[1/34]*20,'r-',label='Probability according to rulebook')
    xticks = [5,10,15,20]
    plt.xticks(xticks, xticks)
    plt.xlabel('Turn')
    plt.ylabel('Probability')
    plt.ylim([0,.1])
    plt.title('Probability of no set on turns with 12 cards')
    #plt.grid()
    plt.legend()
    #plt.show()
    plt.savefig('probability_noset.png')

if __name__=='__main__':
    games = pd.read_csv('games.csv')
    plot_results(games)
