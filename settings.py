WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

weapon_data = {
    "sword" : {"cooldown" : 100, "damage" : 15, "graphic" : "assets/weapons/sword/full.png"}
}

enemies_data = {
	'squid': {'health': 100,'exp':150,'damage':20,'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
}

player_stats = {"health" : 100, "energy" : 60, "attack" : 10, "magic" : 4, "speed" : 5}