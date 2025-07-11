
from typing import Any, final


@final
class UserStats:
    def __init__(self, level: int, ascension: int, talent: tuple[int, int, int], const: int, hp: float,  
                hp_f: float, atk: float, atk_f: float, def_p: float, def_f: float, anemo: float, phys: float,
                em: float, cdmg: float, crate: float, heal: float, outgoing_heal: float, er: float
                ) -> None:
        self.hp = hp
        self.hp_f = hp_f
        self.atk = atk
        self.atk_f = atk_f
        self.def_p = def_p
        self.def_f = def_f
        self.anemo = anemo
        self.phys = phys
        self.em = em
        self.cdmg = cdmg
        self.crate = crate
        self.heal = heal
        self.outgoing_heal = outgoing_heal
        self.er = er
        self.level = level
        self.ascension = ascension
        self.talent = talent
        self.const = const

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'UserStats':
        level: int = data.get("level", 90)
        ascension: int = data.get("ascension", 6)
        talent= data.get('talent', (10,10,10))
        if isinstance(talent, dict):
            talent = (talent["AA"], talent["E"], talent["Q"])
        const: int = data.get("const", 0)
        hp: float = data.get("HP%", 1.0)
        hp_f: float = data.get("Flat HP", 0)
        atk: float = data.get("ATK%", 1.0)
        atk_f: float = data.get("Flat ATK", 0)
        def_p: float = data.get("DEF%", 1.0) # def is python keyword
        def_f: float = data.get("Flat DEF", 0)
        anemo: float = data.get("Anemo DMG%", 0.24)
        phys: float = data.get("Phys DMG%", 0)
        em: float = data.get("EM", 0)
        cdmg: float = data.get("Crit DMG", 0.5)
        crate: float = data.get("Crit Rate", 0.05)
        heal: float = data.get("Heal Bonus%", 0)
        outgoing_heal: float = data.get("Outgoing Heal Bonus%", 0)
        er: float = data.get("Energy Recharge", 1.0)
        return UserStats(level, ascension, talent, const, hp, hp_f, atk, atk_f, def_p, def_f, anemo, 
                         phys, em, cdmg, crate, heal, outgoing_heal, er)

