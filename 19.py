import numpy as np
import re
import logging
from logging import debug as D
import math
import sys
from dataclasses import dataclass
from dataclasses import replace

np.set_printoptions(threshold=np.inf, linewidth=1000)
indent = 0

@dataclass
class State:
    ores: int = 0
    clays: int = 0
    obsis: int = 0
    geodes: int = 0
    orebots: int = 1
    claybots: int = 0
    obsbots: int = 0
    geobots: int = 0


class Blueprint(object):

    def __init__(self, name, orebot, claybot, obsidianbot, geodebot):
        self.name = name
        self.orebot_cost = orebot
        self.claybot_cost = claybot
        self.obsbot_cost = obsidianbot
        self.geobot_cost = geodebot

    def time_to_n_ores(self, n, s):
        if s.ores >= n: return 0
        return math.ceil((n - s.ores) / s.orebots)

    def time_to_n_clays(self, n, s):
        if not s.claybots: return -1
        if s.clays >= n: return 0
        return math.ceil((n - s.clays) / s.claybots)

    def time_to_n_obsis(self, n, s):
        if not s.obsbots: return -1
        if s.obsis >= n: return 0
        return math.ceil((n - s.obsis) / s.obsbots)

    def orebot_in(
            self,
            s):  # min num of minutes to new orebot in current configuration
        materials = self.time_to_n_ores(self.orebot_cost, s)
        return -1 if materials == -1 else materials + 1

    def claybot_in(self, s):
        materials = self.time_to_n_ores(self.claybot_cost, s)
        return -1 if materials == -1 else materials + 1

    def obsbot_in(self, s):  # ore and clay
        if self.time_to_n_clays(self.obsbot_cost[1], s) == -1:
            return -1
        return max(self.time_to_n_ores(self.obsbot_cost[0], s),
                   self.time_to_n_clays(self.obsbot_cost[1], s)) +1

    def geobot_in(self, s):  # ore and obsidian
        if self.time_to_n_obsis(self.geobot_cost[1], s) == -1:
            return -1
        return max(self.time_to_n_ores(self.geobot_cost[0], s),
                   self.time_to_n_obsis(self.geobot_cost[1], s)) +1

    def __str__(self):
        return f"{self.name}: {self.orebot_cost=} {self.claybot_cost=} {self.obsbot_cost=} {self.geobot_cost=}"

    def max_geodes(self, mins, s=State()):
        global indent
        indent +=1
        D(f"{' '*indent}{mins=} {s=}")
        if mins <= 0: return s.geodes
        #        D(f"{s} so {self.orebot_in(s)=}")
        max_g = s.geodes + s.geobots * mins # if nothing else just crack geodes for remaining time

        # note: if it takes so long to create more geobots than there would be no time to exploit them, don't bother
        # either we bother making one more robot of some kind or we already have our solution
        build_orebot_state = replace(
            s,
            ores=s.ores + s.orebots * self.orebot_in(s) - self.orebot_cost,
            clays=s.clays + s.claybots * self.orebot_in(s),
            obsis=s.obsis + s.obsbots * self.orebot_in(s),
            geodes=s.geodes + s.geobots * self.orebot_in(s),
            orebots=s.orebots + 1)
    
        build_claybot_state = replace(
            s,
            ores=s.ores + s.orebots * self.claybot_in(s) - self.claybot_cost,
            clays=s.clays + s.claybots * self.claybot_in(s),
            obsis=s.obsis + s.obsbots * self.claybot_in(s),
            geodes=s.geodes + s.geobots * self.claybot_in(s),
            claybots=s.claybots + 1)

        build_obsbot_state = replace(
            s,
            ores=s.ores + s.orebots * self.obsbot_in(s) - self.obsbot_cost[0],
            clays=s.clays + s.claybots * self.obsbot_in(s) - self.obsbot_cost[1],
            obsis=s.obsis + s.obsbots * self.obsbot_in(s),
            geodes=s.geodes + s.geobots * self.obsbot_in(s),
            obsbots=s.obsbots + 1)

        build_geobot_state = replace(
            s,
            ores=s.ores + s.orebots * self.geobot_in(s) - self.geobot_cost[0],
            clays=s.clays + s.claybots * self.geobot_in(s),
            obsis=s.obsis + s.obsbots * self.geobot_in(s) - self.geobot_cost[1],
            geodes=s.geodes + s.geobots * self.geobot_in(s),
            geobots=s.geobots + 1)

        candidates = [max_g]

        if self.geobot_in(s) != -1 and mins - self.geobot_in(s) > 0 \
           and build_geobot_state.ores >= 0 and build_geobot_state.obsis >= 0 :
            D(f"+Geobot with {mins=} to go ends on  {mins-self.geobot_in(s)} to go , {build_geobot_state}"
              )
            indent +=1
            candidates.append(
                self.max_geodes(mins - self.geobot_in(s), build_geobot_state))
            indent -=1

        if self.obsbot_in(s) != -1 and mins - self.obsbot_in(s) > 0 \
           and build_obsbot_state.clays >= 0 and build_obsbot_state.ores >= 0 \
           and s.obsbots <= self.geobot_cost[1]+5:
            D(f"+Obsbot w {mins=} to go ends on minute  {mins-self.obsbot_in(s)} to go {build_obsbot_state}"
              )
            indent +=1
            candidates.append(
                self.max_geodes(mins - self.obsbot_in(s), build_obsbot_state))
            indent -=1            


        if self.claybot_in(s) != -1 and mins - self.claybot_in(s) > 0 \
           and build_claybot_state.ores >= 0  \
           and s.claybots <= self.obsbot_cost[0]+5:
            D(f"+Claybot w {mins=} to go ends on {mins-self.claybot_in(s)} to go {build_claybot_state}")
            indent +=1            
            candidates.append(
                self.max_geodes(mins - self.claybot_in(s),
                                build_claybot_state))
            indent -=1            

        if self.orebot_in(s) != -1 and  mins - self.orebot_in(s) > 0 \
           and s.orebots < max([self.claybot_cost, self.obsbot_cost[0], self.geobot_cost[0]])*2:
            D(f"+Orebot {mins-self.orebot_in(s)}→{build_orebot_state}")
            indent +=1
            candidates.append(
                self.max_geodes(mins - self.orebot_in(s), build_orebot_state))
            indent -=1            


        indent -=1
        D(candidates)
        return max(candidates)


def read_input(filename):
    blueprints = []
    f = open(filename)
    for l in f:
        m = re.match(
            "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
            l)
        blueprints.append(
            Blueprint(m.group(1), int(m.group(2)), int(m.group(3)),
                      (int(m.group(4)), int(m.group(5))),
                      (int(m.group(6)), int(m.group(7)))))
    return blueprints


filename = ""
mins = 24
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr,
                            level=logging.DEBUG,
                            format="%(message)s")
        mins = int(sys.argv[3])
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 25.py <filename> (opt: --debug)")

bps = read_input(filename)

qualities = []
for bp in bps:
    D(f"{str(bp)=}")
    max_for_bp = bp.max_geodes(mins)
    print(f"{mins=} in {bp.name=}: {max_for_bp=}")
    qualities.append(max_for_bp*int(bp.name))

print(sum(qualities))
