import discord
from discord.ext import commands
import random

import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


# Remplacez par votre ID de rôle HDR
HDR_ROLE_ID = 1290289392874688615
# Remplacez par votre ID de rôle D
D_ROLE_ID = 1290414648918540389

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


STATS_FILE = "stats.json"  # Nom du fichier pour stocker les statistiques

# Fonction pour charger les statistiques
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {}

# Fonction pour sauvegarder les statistiques
def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

# Fonction pour initialiser les statistiques d'un utilisateur
def init_user_stats(user_id):
    stats = load_stats()
    if str(user_id) not in stats:
        stats[str(user_id)] = {
            "**Force**": 0,
            "**Vitesse**": 0,
            "**Endurance**": 0,
            "**Agilité**": 0,
            "**FDD**": 0,
            "**HDR**": 0,
            "**HDO**": 0,
            "**HDA**": 0,
            "**Maîtrise corps à corps**": 0,
            "**Maîtrise épée**": 0,
            "**PointsNonUtilisés**": 0  # Points non utilisés par défaut
        }
        save_stats(stats)

# Commande pour afficher les statistiques d'un autre utilisateur
@bot.tree.command(name="stats-view", description="Affiche les statistiques d'un autre utilisateur.")
async def stats_view(interaction: discord.Interaction, member: discord.Member):
    user_id = member.id
    init_user_stats(user_id)  # Initialisation des stats si nécessaire
    stats = load_stats()
    user_stats = stats[str(user_id)]

    # Création du message avec les statistiques
    stat_message = f"Voici les statistiques de {member.display_name} :\n"
    for stat, value in user_stats.items():
        if stat != "PointsNonUtilisés":
            stat_message += f"{stat} : {value}\n"
    stat_message += f"Points non utilisés : {user_stats['PointsNonUtilisés']}"

    await interaction.response.send_message(stat_message)


    # Création du message avec les statistiques
    stat_message = "Voici vos statistiques :\n"
    for stat, value in user_stats.items():
        if stat != "PointsNonUtilisés":
            stat_message += f"{stat} : {value}\n"
    stat_message += f"Points non utilisés : {user_stats['PointsNonUtilisés']}"

    await interaction.response.send_message(stat_message)

# Commande pour ajouter des points à sa propre statistique
@bot.tree.command(name="stats-add", description="Ajoutez des points dans votre statistique.")
async def stats_add(interaction: discord.Interaction, stat: str, points: int):
    user_id = interaction.user.id
    init_user_stats(user_id)
    stats = load_stats()
    user_stats = stats[str(user_id)]

    if stat not in user_stats:
        await interaction.response.send_message("Statistique invalide.")
        return

    if user_stats["PointsNonUtilisés"] < points:
        await interaction.response.send_message("Vous n'avez pas assez de points non utilisés.")
        return

    user_stats[stat] += points
    user_stats["PointsNonUtilisés"] -= points
    save_stats(stats)

    await interaction.response.send_message(f"Vous avez ajouté {points} points à votre {stat}.")

# Commande pour que le staff ajoute des points non utilisés à un utilisateur
@bot.tree.command(name="staff-add", description="Ajoutez des points non utilisés à la statistique d'un utilisateur.")
async def staff_add(interaction: discord.Interaction, member: discord.Member, points: int):
    # Vérifiez si l'utilisateur a le rôle "Staff"
    if "Administrateur" not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    user_id = member.id
    init_user_stats(user_id)
    stats = load_stats()
    user_stats = stats[str(user_id)]

    # Ajout des points aux Points Non Utilisés
    user_stats["PointsNonUtilisés"] += points
    save_stats(stats)

    await interaction.response.send_message(f"Vous avez ajouté {points} points non utilisés à {member.display_name}.")
# Commande pour que le staff réinitialise tous les points d'un utilisateur
@bot.tree.command(name="staff-clear", description="Réinitialisez tous les points d'un utilisateur.")
async def staff_clear(interaction: discord.Interaction, member: discord.Member):
    # Vérifiez si l'utilisateur a le rôle "Staff"
    if "Administrateur" not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    user_id = member.id
    init_user_stats(user_id)
    stats = load_stats()
    user_stats = stats[str(user_id)]

    # Réinitialisation des statistiques
    user_stats["Force"] = 0
    user_stats["Vitesse"] = 0
    user_stats["Endurance"] = 0
    user_stats["Agilité"] = 0
    user_stats["FDD"] = 0
    user_stats["HDR"] = 0
    user_stats["HDO"] = 0
    user_stats["HDA"] = 0
    user_stats["Maîtrise corps à corps"] = 0
    user_stats["Maîtrise épée"] = 0
    user_stats["PointsNonUtilisés"] = 0  # Réinitialisation des points non utilisés

    save_stats(stats)

    await interaction.response.send_message(f"Tous les points de {member.display_name} ont été réinitialisés.")


    user_id = member.id
    init_user_stats(user_id)
    stats = load_stats()
    user_stats = stats[str(user_id)]

    if stat not in user_stats:
        await interaction.response.send_message("Statistique invalide.")
        return

    user_stats[stat] += points
    save_stats(stats)

    await interaction.response.send_message(f"Vous avez ajouté {points} points à {member.display_name} dans {stat}.")



# Commande slash pour obtenir le rôle HDR
@bot.tree.command(name="roll-hdr", description="Essaye de gagner le rôle HDR!")
async def roll_hdr(interaction: discord.Interaction):
    chance = random.randint(1, 100)
    if chance > 85:
        role = interaction.guild.get_role(HDR_ROLE_ID)
        member = interaction.guild.get_member(interaction.user.id)
        await interaction.response.send_message("Vous avez obtenu le HDR ! 🎉\nhttps://images-ext-1.discordapp.net/external/INehF05BMADYSeyLkdWumCDGMr51zN-tXCFoam2S4uw/https/media1.tenor.com/m/fep5_H3WNy8AAAAC/haki-luffy.gif?width=622&height=350")
    else:
        await interaction.response.send_message("Pas de HDR pour cette fois ! 😔\nhttps://media1.tenor.com/m/zC27qanB5wYAAAAC/one-piece-anime.gif")

# Commande slash pour obtenir le rôle D
@bot.tree.command(name="roll-d", description="Essaye de gagner le D!")
async def roll_d(interaction: discord.Interaction):
    chance = random.randint(1, 100)
    if chance > 90:
        role = interaction.guild.get_role(D_ROLE_ID)
        member = interaction.guild.get_member(interaction.user.id)
        await interaction.response.send_message("Vous avez obtenu le D ! 🎉\nhttps://media.tenor.com/m/G0dP5NM52YwAAAAC/roof-piece-luffy.gif")
    else:
        await interaction.response.send_message("Tu ne possèdes pas le D... 😔\nhttps://cdn.discordapp.com/attachments/1289978193415245916/1290300547286564977/luffycrying-puffy.gif")

# Commande slash pour fouiller
@bot.tree.command(name="fouille", description="Tente d'obtenir une arme ou des objets!")
async def fouille(interaction: discord.Interaction):
    chance = random.randint(1, 100)
    
    if chance <= 30:
        # Obtention d'une arme
        weapon_chance = random.randint(1, 100)
        if weapon_chance <= 50:
            await interaction.response.send_message("Vous avez obtenu une arme **Basique** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290645055446712390/wado-ichimonji.gif?ex=66fd3660&is=66fbe4e0&hm=6d0c4c9dbfbdfd79055d0b8b7695a44693c7aa37d0a0bfade9166633625a18d7&")
        elif weapon_chance <= 80:
            await interaction.response.send_message("Vous avez obtenu une arme **Peu Commune** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290645198048596020/yubashiri.gif?ex=66fd3682&is=66fbe502&hm=1235fb7dbe64e5e86b0d31d0749acac01572604b0e5abff3003f05ee27c798ff&")
        elif weapon_chance <= 95:
            await interaction.response.send_message("Vous avez obtenu une arme **Rare** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290645419868684298/anime-trafalgar-law.gif?ex=66fd36b7&is=66fbe537&hm=e939ff2f5f0220c52bde21695841e6e14cad4c246a20b5daa8c5a819890e4512&")
        else:
            await interaction.response.send_message("Vous avez obtenu une arme **Légendaire** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290645769896071250/dracule-mihawk-one-piece.gif?ex=66fd370a&is=66fbe58a&hm=96ca3f01e8fbd17e7fa1c736b9b5295c5762be3ee410491daa231bb898dcfd25&")
    else:
        # Obtention d'argent ou d'autres objets
        if random.randint(1, 100) <= 15:
            await interaction.response.send_message("Vous n'avez rien obtenu.\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290646133370126390/luffy-one-piece.gif?ex=66fd3761&is=66fbe5e1&hm=c5d70f7c2d8da994ad5f845c3eb007b8038e3f5c14370d9073fbe302c39937c6&")
        else:
            money_chance = random.randint(1, 100)
            if money_chance <= 40:
                amount = random.choice([250000, 500000, 1000000])
                await interaction.response.send_message(f"Vous avez obtenu **argent** ! Vous avez gagné **{amount} Berries** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290646254648295556/nami-cat-burglar.gif?ex=66fd377e&is=66fbe5fe&hm=688505d1d1bde5af91364dc0fa6cc5374807217e0db94d498c6fd06fc8d8ad1a&")
            else:
                # Obtention de fruits du démon
                fruit_chance = random.randint(1, 100)
                if fruit_chance <= 50:
                    await interaction.response.send_message("Vous avez obtenu un **fruit du démon Zoan** !\nhttps://cdn.discordapp.com/attachments/762314390253862983/1290782542303199304/rob-lucci-one-piece.gif?ex=66fdb66b&is=66fc64eb&hm=4b24b1d0ee4d162ac5cea5878307ec217d0cb6858641683f4ae9fd0e8411e956&")
                elif fruit_chance <= 70:
                    await interaction.response.send_message("Vous avez obtenu un **fruit du démon Zoan Antique** !\nhttps://media.discordapp.net/attachments/762314390253862983/1290647273457324044/sanji-vs-queen-sanji.gif?ex=66fd3871&is=66fbe6f1&hm=1544c64267fe84380264b8793ee31af629619d38e6120e5e7828cf350278a930&=&width=467&height=263")
                elif fruit_chance <= 85:
                    await interaction.response.send_message("Vous avez obtenu un **fruit du démon Paramecia** !\nhttps://media.discordapp.net/attachments/762314390253862983/1290647498591047840/big-mom-one-piece.gif?ex=66fd38a6&is=66fbe726&hm=98f58bfff326a5ba5959101c8221c13145afe55298d3accb376f138965df2fea&=&width=622&height=353")
                elif fruit_chance <= 95:
                    await interaction.response.send_message("Vous avez obtenu un **fruit du démon Logia** !\nhttps://media.discordapp.net/attachments/762314390253862983/1290647692208378020/ich-ichi.gif?ex=66fd38d4&is=66fbe754&hm=bb351ed869db08727d9d0bfd57ae02a0bc4707ef5df8dc6f269da628025241c0&=&width=622&height=446")
                else:
                    await interaction.response.send_message("Vous avez obtenu un **fruit du démon Zoan Mythologique** !\nhttps://media.discordapp.net/attachments/762314390253862983/1290647908806561853/one-piece-fenix.gif?ex=66fd3908&is=66fbe788&hm=c7b70d2608b15e91d1db3d812cc4894c1955546937387c65b254410cd4fecc91&=&width=800&height=445")



@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    await bot.tree.sync()  # Synchronisation des commandes slash


# Token du bot
bot.run('MTI5MDYzOTU0OTE0NzM4MTc3MA.GfQ4uQ.flJZLnC0TBXzq-4tjHBYK5xqzK9YJ9XOuy67Yg')  # Remplacez par votre token
