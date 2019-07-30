import numpy as np
import matplotlib.pyplot as plt

n = 100000
prof = 5
armours = list(range(5,21))

def attack(dmg:int, ac:int, profficiency=5, advantage=False, heavy=False):
    hit_mod = (profficiency-5) if heavy else profficiency  # heavy attack has -5 to hit
    rolls = (np.random.random(n)*20+1).astype(np.int)
    if advantage:
        rolls = np.maximum(rolls, (np.random.random(n)*20+1).astype(np.int))  # roll twice, take higher

    damage_roll1 = (np.random.random(n)*dmg+1).astype(np.int)
    mask = (damage_roll1 <= 2)  # reroll on 1's and 2's
    damage_roll1[mask] = (np.random.random(mask.sum())*dmg+1).astype(np.int)
    
    damage_roll2 = (np.random.random(n)*dmg+1).astype(np.int)
    mask = (damage_roll2 <= 2)
    damage_roll2[mask] = (np.random.random(mask.sum())*dmg+1).astype(np.int)

    damage_roll = np.maximum(damage_roll1, damage_roll2)  # savage attacker, take higher damage

    if heavy:
        damage_roll += 10

    damage_roll[rolls+hit_mod <= ac] = 0  # no damage when attack roll is <= enemy armour class
    damage_roll[rolls == 20] += dmg  # add max damage on critical hit
    return damage_roll

two_normal = []
one_normal = []
two_wreckless = []
one_wreckless = []
two_heavy = []
two_heavy_wreckless = []

for armour in armours:
    d = []

    two_normal_att = attack(12, armour)
    one_normal_att = attack(8, armour) + attack(6, armour, 0)
    two_wreckless_att = attack(12, armour, advantage=True)
    one_wreckless_att = attack(8, armour, advantage=True) + attack(6, armour, 0, advantage=True)
    two_heavy_att = attack(12, armour, heavy=True)
    two_heavy_wreckless_att =  attack(12, armour, heavy=True, advantage=True)

    two_normal.append(two_normal_att.mean())
    one_normal.append(one_normal_att.mean())
    two_wreckless.append(two_wreckless_att.mean())
    one_wreckless.append(one_wreckless_att.mean())
    two_heavy.append(two_heavy_att.mean())
    two_heavy_wreckless.append(two_heavy_wreckless_att.mean())
        
plt.plot(armours, two_normal, 'r.', label="two_normal")
plt.plot(armours, one_normal, 'b.', label="one_normal")
plt.plot(armours, two_wreckless, 'g.', label="two_advantage")
plt.plot(armours, one_wreckless, 'y.', label="one_advantage")
plt.plot(armours, two_heavy, 'c.', label="two_heavy")
plt.plot(armours, two_heavy_wreckless, 'k.', label="two_heavy_advantage")

plt.legend()
plt.ylabel("Average damage")
plt.xlabel("Enemy AC")
plt.show()
