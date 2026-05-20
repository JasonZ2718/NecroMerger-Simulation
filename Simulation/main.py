from Simulation.Classes import board as b, stations as s, creatures as c, champions as ch
from Simulation.Classes.stations import HackedState
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

start = time.time()
highDiscardNormal = [[] for i in range(5)]
highDiscardHacked = [[] for i in range(2)]
lowDiscardNormal = [[] for i in range(5)]
lowDiscardHacked = [[] for i in range(2)]

def calc(stationName, resource, champion: ch.Champion):
    STATIONS = {"Grave": s.Grave, "Lectern": s.Lectern, "Portal": s.Portal}
    for lv in range(1, 6):
        station = STATIONS[stationName](lv, HackedState.NORMAL)
        for col in range(5, 26):
            board = b.Board(1, col)
            n, num1, num2 = 10, 0, 0
            for i in range(n):
                num1 += board.numChampHighDiscard(station, resource, champion)
                board.reset()
                num2 += board.numChampLowDiscard(station, resource, champion)
                board.reset()
            highDiscardNormal[lv-1].append(num1/n)
            lowDiscardNormal[lv-1].append(num2/n)
    for lv in [3, 5]:
        station = STATIONS[stationName](lv, HackedState.HACKED)
        for col in range(5, 26):
            board = b.Board(1, col)
            n, num1, num2 = 10, 0, 0
            for i in range(n):
                num1 += board.numChampHighDiscard(station, resource, champion)
                board.reset()
                num2 += board.numChampLowDiscard(station, resource, champion)
                board.reset()
            highDiscardHacked[[3,5].index(lv)].append(num1/n)
            lowDiscardHacked[[3,5].index(lv)].append(num2/n)
    return stationName, resource, champion

stationName, resource, champion = calc("Portal", 1e6, ch.Rival())

size = np.arange(5, 26)
fig, axs = plt.subplots(2, 2)

colors = ["C1", "C0", "C2", "C4", "C3"]
for i in range(5):
    axs[0][0].plot(size, np.array(highDiscardNormal)[i], label=f"Lv {i+1}", color=colors[i])
    axs[1][0].plot(size, np.array(lowDiscardNormal)[i], label=f"Lv {i+1}", color=colors[i])
for i in range(2):
    axs[0][1].plot(size, np.array(highDiscardHacked)[i], label=f"Lv {3*i+2}", color=colors[3*i+1])
    axs[1][1].plot(size, np.array(lowDiscardHacked)[i], label=f"Lv {3*i+2}", color=colors[3*i+1])

axs[0][0].set_title("Normal Station, High Lv Discard Method")
axs[1][0].set_title("Normal Station, Low Lv Discard Method")
axs[0][1].set_title("Hacked Station, High Lv Discard Method")
axs[1][1].set_title("Hacked Station, Low Lv Discard Method")

axsFlatten = axs.flatten()
maxylim = max(ax.get_ylim()[1] for ax in axsFlatten)
minylim = min(ax.get_ylim()[0] for ax in axsFlatten)
for i in range(2):
    for j in range(2):
        axs[i][j].legend(loc="lower right")
        axs[i][j].minorticks_on()
        axs[i][j].tick_params(axis="both", which="minor", size=3)
        axs[i][j].grid(linestyle="--")
plt.setp(axs, xticks=np.arange(5, 26, 5), ylim=(minylim, maxylim))
fig.supxlabel('Board Size', y=.03, fontsize=15)
fig.supylabel('Number of Champions Spawned', x=.05, fontsize=15)
fig.suptitle(f"# of {champion.name}s spawned using {stationName} with {resource:.1e} resources per trial",
             fontsize=24)
fig.subplots_adjust(left=.1,bottom=.1,right=.9,top=.87,wspace=.1,hspace=.2)

end = time.time()
print(end-start)

totalArray = highDiscardNormal + highDiscardHacked + lowDiscardNormal + lowDiscardHacked
df = pd.DataFrame(totalArray).T
df.to_excel("Portal_Rival.xlsx", index=False, header=False)
plt.show()
