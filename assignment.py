import sqlite3

# Connect to the database
connection = sqlite3.connect("dbase.db")
cursor = connection.cursor()

# 1. What is the structure of the table? What are the columns and what datatypes do they store?
query = "PRAGMA table_info(npc)"
cursor.execute(query)
structure = cursor.fetchall()
print("Table structure:", structure)

# 2. How many records are in the table?
query = "SELECT COUNT(*) FROM npc"
cursor.execute(query)
record_count = cursor.fetchone()
print("Number of records:", record_count[0])

# 3. How many Knights are in the table?
query = "SELECT COUNT(*) FROM npc WHERE class = 'Knight'"
cursor.execute(query)
knight_count = cursor.fetchone()
print("Number of Knights:", knight_count[0])

# 4. Which class has the highest number of members?
query = "SELECT class, COUNT(*) as count FROM npc GROUP BY class ORDER BY count DESC"
cursor.execute(query)
highest_class = cursor.fetchone()
print("Class with the highest number of members:", highest_class)

# 5. What is the ID number of the Jester with the most gold?
query = "SELECT id FROM npc WHERE class = 'Jester' ORDER BY gold DESC LIMIT 1"
cursor.execute(query)
jester_most_gold = cursor.fetchone()
print("ID of the Jester with the most gold:", jester_most_gold[0])

# 6. What is the total gold of the 100 wealthiest npc's in the table?
query = "SELECT SUM(gold) FROM (SELECT gold FROM npc ORDER BY gold DESC LIMIT 100)"
cursor.execute(query)
total_gold_wealthiest = cursor.fetchone()
print("Total gold of the 100 wealthiest NPCs:", total_gold_wealthiest[0])

# 7. What is the total gold of the 100 wealthiest npc's under level 5?
query = "SELECT SUM(gold) FROM (SELECT gold FROM npc WHERE level < 5 ORDER BY gold DESC LIMIT 100)"
cursor.execute(query)
total_gold_wealthiest_under_5 = cursor.fetchone()
print("Total gold of the 100 wealthiest NPCs under level 5:", total_gold_wealthiest_under_5[0])

# 8. What is the stats of the Bard with the highest strength?
query = "SELECT * FROM npc WHERE class = 'Bard' ORDER BY strength DESC LIMIT 1"
cursor.execute(query)
bard_highest_strength = cursor.fetchone()
print("Stats of the Bard with the highest strength:", bard_highest_strength)

# 9. What is the ID number of the npc with highest total sum of their 6 primary stats?
query = "SELECT id FROM npc ORDER BY (strength + intelligence + wisdom + dexterity + constitution + charisma) DESC LIMIT 1"
cursor.execute(query)
npc_highest_stats = cursor.fetchone()
print("ID of the NPC with the highest total sum of their 6 primary stats:", npc_highest_stats[0])

# 10. What percentage of all fighter classes (Barbarian, Warrior, Knight, Samurai) are Warriors?
query = "SELECT COUNT(*) FROM npc WHERE class IN ('Barbarian', 'Warrior', 'Knight', 'Samurai')"
cursor.execute(query)
total_fighters = cursor.fetchone()[0]
query = "SELECT COUNT(*) FROM npc WHERE class = 'Warrior'"
cursor.execute(query)
warriors_count = cursor.fetchone()[0]
percentage_warriors = (warriors_count / total_fighters) * 100
print("Percentage of Warriors among all fighter classes:", percentage_warriors)

# 11. What is the average hit points per level of the npc's that are level 10 or higher?
query = "SELECT AVG(hp / level) FROM npc WHERE level >= 10"
cursor.execute(query)
average_hp_per_level = cursor.fetchone()
print("Average hit points per level for NPCs level 10 or higher:", average_hp_per_level[0])

# Problem: Determine how many NPC's have chosen the wrong class based on their statistics
query = """
SELECT id, class, strength, intelligence, wisdom, dexterity, constitution, charisma
FROM npc
"""
cursor.execute(query)
npcs = cursor.fetchall()

wrong_class_count = 0
for npc in npcs:
    id, class_name, str, int, wis, dex, con, cha = npc
    primary_stat = max(str, int, wis, dex, con, cha)
    if (class_name in ['Knight', 'Warrior', 'Barbarian', 'Samurai', 'Ranger'] and primary_stat != str) or \
       (class_name in ['Sage', 'Sorcerer', 'Bard', 'Jester'] and primary_stat != int) or \
       (class_name in ['Thief', 'Assassin', 'Monk'] and primary_stat != dex) or \
       (class_name == 'Priest' and primary_stat != wis):
        wrong_class_count += 1

print("Number of NPCs with the wrong class based on their statistics:", wrong_class_count)

connection.close()
