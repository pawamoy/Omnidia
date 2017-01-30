# -*- coding: utf-8 -*-
import cProfile

from .models import Dataset, DatasetValue


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(2)

    return profiled_func

MOVIE_GENRES = [
    'Abstrait', 'Action', 'Amateur', 'Americana', 'Amour', 'Animation',
    'Arts Martiaux', 'Autobiographique', 'Aventure', 'Bidasse',
    'Biographique', 'Bollywood', 'Bridge', 'Buddy Movie', 'Burlesque',
    'Business-Thriller', 'Casse', 'Catastrophe', 'Chanbara',
    'Chevalerie', 'Choral', 'Chronique', 'Cirque', 'Colonial', 'Comédie',
    'Conte', 'Court Métrage', 'Cross-Over', 'Danse',
    "De Cape Et D'épée", 'Direct', 'Documentaire',
    'Documentaire Nature', 'Drame', 'Enfants', 'Enigme', 'Erotique',
    'Espionnage', 'Essai Cinématographique', 'Ethnographique',
    'Expérimental', 'Exploitation', 'Fantastique', 'Faux Documentaire',
    'Ferroviaire', 'Gangster', 'Giallo', 'Gore', 'Grindhouse', 'Guerre',
    'Héroïc-Fantasy', 'Heimatfilm', 'Historique', 'Horreur',
    'Indépendant', 'Institutionnel', 'Jidai-geki', 'Journal Filmé',
    'Juridique', 'Ken Geki', 'Machinima', 'Making-Of', 'Maneater Series',
    'Maritime', 'Masala', 'Mélodrame', 'Midnight Movie', 'Mondo',
    'Montagne', 'Musical', 'Mystère', 'Narratif', 'Nazisploitation',
    'Néo-Polar Italien', 'Noir', 'Nonnesploitation', 'Northern',
    'Omnibus', 'Parodie', 'Péplum', 'Policier', 'Politique',
    'Pornographique', 'Propagande', 'Publicitaire', 'Rape And Revenge',
    'Reportage', 'Road Movie', 'Robinsonade', 'Romance', 'Romantique',
    'Science-Fiction', 'Screwball Comedy', 'Sérial', 'Série B',
    'Série Z', 'Sketches', 'Slasher', 'Snuff Movie', 'Spéléologie',
    'Structurel', 'Style Guy Ritchie', 'Super-héros', 'Surréaliste',
    'Suspense', 'Thriller', 'Torture Porn', 'Troma', 'Vampirisme',
    'Western', 'Western Spaghetti', 'Wuxiapian', 'Zombie'
]

MUSIC_GENRES = [
    'Abstract', 'Acid', 'Alternative', 'Ambient', 'Big', 'Bouncy',
    'Broken', 'Brutal', 'Celtic', 'Chicago', 'Chill', 'Cosmic', 'Dark',
    'Deep', 'Depressive', 'Digital', 'Euro', 'Filth', 'Gangsta',
    'Garage', 'Ghetto', 'Happy', 'Hard', 'Horror', 'Indie', 'Industrial',
    'Italo', 'Melodic', 'New', 'New York', 'Northern', 'Norvegian',
    'Oldschool', 'Post', 'Progressive', 'Psychadelic', 'Slow', 'Smooth',
    'Southern', 'Space', 'Symphonic', 'Terror', 'True', 'UK', 'Vocal',
    '2-Step', '8-Bit', 'A Cappella', 'Acoustique', 'Acte De Ballet',
    'Aggrotech', 'Allaoui', 'Anarcho-Punk', 'Antienne', 'Arfa', 'Aria',
    'Art Acousmatique', 'Art Sonore', 'Aubade', 'Autres',
    'Avant-Gardiste', 'Bacalao', 'Bachata', 'Bachatango', 'Baile Funk',
    'Balearic Beat', 'Ballade', 'Ballet', 'Baltimore Club', 'Baroque',
    'Bassline', 'Batcave', 'Beat', 'Bebop', 'Berceuse', 'Berlin School',
    'Black Metal', 'Bluegrass', 'Blues', 'Boléro', 'Boogie',
    'Bossa-Nova', 'Bourrée', 'Brain Dance', 'Brass Band', 'Break',
    'Breakbeat', 'Breakcore', 'Breakstep', 'Bretonne', 'Bubblegum Dance',
    'Cabaret', 'Cantate', 'Cantate Profane', 'Cantate Sacrée',
    'Cantilène', 'Capoeira', 'Cavatine', 'Celtique', 'Chaconne',
    'Chanson', 'Chanson Française', 'Chant Grégorien', 'Chant Lyrique',
    'Charleston', 'ChillOut', 'Chiptune', 'Choral', 'Clash', 'Classique',
    'Clownstep', 'Club', 'Coimbra', 'Coldwave', 'Concerto',
    'Concerto Grosso', 'Contredanse', 'Core', 'Country', 'Courante',
    'Crossover', 'Crunk', 'Culte', 'Cumbia', 'Cybergrind', 'Dance',
    'Darkstep', 'Death Metal', 'Dirty South', 'Disco', 'Divertimento',
    'Doom', 'Downtempo', 'Dream', "Drill'n Bass", 'Drone Music',
    'Drum & Bass', 'Drumstep', 'Drumfunk', 'Dub', 'Dubstep',
    'East Coast', 'EBM', 'Electro', 'Electroacoustique', 'Emergente',
    'Ethereal Wave', 'Experimental', 'Fado', 'Fanfare', 'Fantaisie',
    'Filin', 'Flamenco', 'Florida Breaks', 'Folk', 'Folk Metal',
    'Folktronica', 'Forlane', 'Forrò', 'Fox-Trot', 'Freestyle',
    'French Touch', 'Fugue', 'Full On', 'Funk', 'Gabber', 'Gaillarde',
    'Gavotte', 'Gigue', 'Glitch', 'Glitchcore', 'Gnaouas', 'Goregrind',
    'Gospel', 'Gothic', 'Grime', 'Grind', 'Grindcore', 'Grunge',
    'Habanera', 'Hall', 'Handsup', 'Hardcore', 'Hardstep', 'Hardstyle',
    'Hardtek', 'Heavy Metal', 'Hi-NRG', 'Hip-Hop', 'House', 'Humour',
    'Hymne', 'IDM', 'Illbient', 'Imprompt', 'Inclassable',
    'Instrumental', 'Invention', 'Irlandaise', 'Jam', 'Japanoise',
    'Japonais', 'Java', 'Javanaise', 'Jazz', 'Jerk', 'Jeux Vidéo',
    'Jpop', 'Jrock', 'Jumpstyle', 'Jump-Up', 'Jungle', 'Kizomba',
    'Klezmer', 'Kompa', 'Kpop', 'Krautrock', 'Kuduro', 'Kwaito', 'Latin',
    'Lied', 'Liquid Funk', 'Locale', 'Lo-Fi', 'Logobi', 'Louange',
    'Lounge', 'Loure', 'Madison', 'Madrigal', 'Makina', 'Maloya',
    'Mambo', 'Marche', 'Mashup', 'Masque', 'Mazurka', 'Mbalax',
    'Mediatif', 'Mélodie', 'Mental Tribe', 'Menuet', 'Merengue',
    'Messe', 'Messe Pour Orgue', 'Metal', 'Metalcore', 'Milonga',
    'Minimal', 'Motet', 'Murga', 'Musette', 'Ndombolo',
    'Negro Spiritual', 'Neo', 'Neo Metal', 'Neurofunk', 'New Age',
    'Nintendocore', 'Nitzhonot', 'No Wave', 'Nocturne', 'Noise',
    'Noisecore', 'Noisy Pop', 'Nortec', 'Nu Skool Breaks', 'Oi!',
    'Opéra', 'Opéra Ballet', 'Opera Seria', 'Oratorio', 'Ordre',
    'Original Soundtrack', 'Ouverture', 'Ouverture Française',
    'Ouverture Italienne', 'Pachanga', 'Pagan', 'Paillarde', 'Partita',
    'Paso Doble', 'Passacaille', 'Passepied', 'Passion',
    'Pastorale Héroïque', 'Pavane', 'Pidikhtos', 'Pirate Metal',
    'Polka', 'Polonaise', 'Pop', 'Power Metal', 'Power Noise',
    'Prélude', 'Psaume', 'Psy', 'Psybient', 'Psybreaks', 'Psyprog',
    'Psytrance Sud-Africaine', 'Pumping Tribe', 'Punk', 'Quatuor',
    'Quintette', 'Rabiz', 'RAC', 'Ragga', 'Raggacore', 'Raï',
    "Raï'n'b", 'Rap', 'Rap Français', 'Rave', 'Rave Breaks',
    'Rébétiko', 'Récitatif', 'Reggae', 'Reggaeton', 'Renaissance',
    'Requiem', 'Retro', 'Rhapsodie', 'Rhythm And Blues', 'Ricercare',
    'Rigodon', "R'n'B", 'Rock', "Rock 'n Roll", 'Romantique', 'Ronde',
    'Rondeau', 'Roots', 'Rumba', 'Salsa', 'Salsaton', 'Samba', 'Sambass',
    'Sarabande', 'Saudade', 'Scherzo', 'Schranz', 'Screamo', 'Séga',
    'Seggae', 'Semba', 'Semi-Opéra', 'Sérénade', 'Shibuya-Kei',
    'Shoegaze', 'Sinfonia', 'Sirtaki', 'Ska', 'Skacore', 'Skate Punk',
    'Sketchs', 'Skweee', 'Slam', 'Soca', 'Son Cubain', 'Sonate',
    "Sonate D'église", 'Songo', 'Soukous', 'Soul', 'Speed Garage',
    'Speed Metal', 'Speedcore', 'Step', 'Suite', 'Suomisaundi', 'Swing',
    'Symphonie', 'Symphonie Concertante', 'Synth', 'Synthcore',
    'Synthwave', 'Tambourin', 'Tango', 'Tango Argentin', 'Tarentelle',
    'Te Deum', 'Teen Pop', 'Tekfunk', 'Terrorcore', 'Thrash Metal',
    'Tiento', 'Timba', 'Toccata', 'Tombeau', 'Tragédie Lyrique',
    'Trailer', 'Trance', 'Trance-Goa', 'Tribal', 'Tribe', 'Tribecore',
    'Trip-Hop', 'Tumba', 'Twee Pop', 'Twist', 'Unblack Metal', 'Valse',
    'Valse Péruvienne', 'Valse Tyrolienne', 'Variations', 'Vêpres',
    'Viking Metal', 'Visual Kei', 'Washboard', 'Wave', 'World Beat',
    'World Music', 'Worship', 'X-Over', 'Yal', 'Yela', 'Yirmi',
    'Yorkshire Techno', 'Zouglou', 'Zouk', 'Zydeco'
]


@do_cprofile
def load_genres():
    ds_movie_genre = Dataset(name='Movie genre').save()
    ds_music_genre = Dataset(name='Music genre').save()

    similar = set(MOVIE_GENRES) & set(MUSIC_GENRES)
    from neomodel import db
    with db.transaction:
        movie_dvs = DatasetValue.create_or_update(
            *[{'name': g} for g in set(MOVIE_GENRES) - similar],
            relationship=ds_movie_genre.values
        )
        music_dvs = DatasetValue.create_or_update(
            *[{'name': g} for g in set(MUSIC_GENRES) - similar],
            relationship=ds_music_genre.values
        )
        both_dvs = DatasetValue.create_or_update(
            *[{'name': g} for g in similar]
        )

        for node in both_dvs:
            node.dataset.connect(ds_movie_genre)
            node.dataset.connect(ds_music_genre)


def run():
    load_genres()
