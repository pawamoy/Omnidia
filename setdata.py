# -*- coding: utf-8 -*-
from omnidia.models import *

# ** File types ***********************************
oft_text = FileType.objects.create(name='Text')
oft_audio = FileType.objects.create(name='Audio')
oft_video = FileType.objects.create(name='Video')
oft_picture = FileType.objects.create(name='Picture')
oft_document = FileType.objects.create(name='Document')
oft_archive = FileType.objects.create(name='Archive')

#** Data types ***********************************
dt_string = DataType.ojects.create(name='String')
dt_integer = DataType.ojects.create(name='Integer')
dt_decimal = DataType.ojects.create(name='Decimal')
dt_boolean = DataType.ojects.create(name='Boolean')

#** Datasets *************************************
ds_genre_movie = Dataset.objects.create(name='Movie genre')
ds_genre_music = Dataset.objects.create(name='Music genre')

for mg in ['Abstrait', 'Action', 'Amateur', 'Americana', 'Amour', 'Animation',
           'Arts Martiaux', 'Autobiographique', 'Aventure', 'Bidasse',
           'Biographique', 'Bollywood', 'Bridge', 'Buddy Movie', 'Burlesque',
           'Business-Thriller', 'Casse', 'Catastrophe', 'Chanbara',
           'Chevalerie', 'Choral', 'Chronique', 'Cirque', 'Colonial', 'Comédie',
           'Conte', u'Court Métrage', 'Cross-Over', 'Danse',
           u"De Cape Et D'épée", 'Direct', 'Documentaire',
           'Documentaire Nature', 'Drame', 'Enfants', 'Enigme', 'Erotique',
           'Espionnage', u'Essai Cinématographique', 'Ethnographique',
           u'Expérimental', 'Exploitation', 'Fantastique', 'Faux Documentaire',
           'Ferroviaire', 'Gangster', 'Giallo', 'Gore', 'Grindhouse', 'Guerre',
           u'Héroïc-Fantasy', 'Heimatfilm', 'Historique', 'Horreur',
           u'Indépendant', 'Institutionnel', 'Jidai-geki', u'Journal Filmé',
           'Juridique', 'Ken Geki', 'Machinima', 'Making-Of', 'Maneater Series',
           'Maritime', 'Masala', u'Mélodrame', 'Midnight Movie', 'Mondo',
           'Montagne', 'Musical', u'Mystère', 'Narratif', 'Nazisploitation',
           u'Néo-Polar Italien', 'Noir', 'Nonnesploitation', 'Northern',
           'Omnibus', 'Parodie', u'Péplum', 'Policier', 'Politique',
           'Pornographique', 'Propagande', 'Publicitaire', 'Rape And Revenge',
           'Reportage', 'Road Movie', 'Robinsonade', 'Romance', 'Romantique',
           'Science-Fiction', 'Screwball Comedy', u'Sérial', u'Série B',
           u'Série Z', 'Sketches', 'Slasher', 'Snuff Movie', u'Spéléologie',
           'Structurel', 'Style Guy Ritchie', u'Super-héros', u'Surréaliste',
           'Suspense', 'Thriller', 'Torture Porn', 'Troma', 'Vampirisme',
           'Western', 'Western Spaghetti', 'Wuxiapian', 'Zombie']:
    DatasetValue.objects.create(dataset=ds_genre_movie, value=mg)

for mg in ['Abstract', 'Acid', 'Alternative', 'Ambient', 'Big', 'Bouncy',
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
           'Black Metal', 'Bluegrass', 'Blues', u'Boléro', 'Boogie',
           'Bossa-Nova', u'Bourrée', 'Brain Dance', 'Brass Band', 'Break',
           'Breakbeat', 'Breakcore', 'Breakstep', 'Bretonne', 'Bubblegum Dance',
           'Cabaret', 'Cantate', 'Cantate Profane', u'Cantate Sacrée',
           u'Cantilène', 'Capoeira', 'Cavatine', 'Celtique', 'Chaconne',
           'Chanson', u'Chanson Française', u'Chant Grégorien', 'Chant Lyrique',
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
           'Folktronica', 'Forlane', u'Forrò', 'Fox-Trot', 'Freestyle',
           'French Touch', 'Fugue', 'Full On', 'Funk', 'Gabber', 'Gaillarde',
           'Gavotte', 'Gigue', 'Glitch', 'Glitchcore', 'Gnaouas', 'Goregrind',
           'Gospel', 'Gothic', 'Grime', 'Grind', 'Grindcore', 'Grunge',
           'Habanera', 'Hall', 'Handsup', 'Hardcore', 'Hardstep', 'Hardstyle',
           'Hardtek', 'Heavy Metal', 'Hi-NRG', 'Hip-Hop', 'House', 'Humour',
           'Hymne', 'IDM', 'Illbient', 'Impromptu', 'Inclassable',
           'Instrumental', 'Invention', 'Irlandaise', 'Jam', 'Japanoise',
           'Japonais', 'Java', 'Javanaise', 'Jazz', 'Jerk', u'Jeux Vidéo',
           'Jpop', 'Jrock', 'Jumpstyle', 'Jump-Up', 'Jungle', 'Kizomba',
           'Klezmer', 'Kompa', 'Kpop', 'Krautrock', 'Kuduro', 'Kwaito', 'Latin',
           'Lied', 'Liquid Funk', 'Locale', 'Lo-Fi', 'Logobi', 'Louange',
           'Lounge', 'Loure', 'Madison', 'Madrigal', 'Makina', 'Maloya',
           'Mambo', 'Marche', 'Mashup', 'Masque', 'Mazurka', 'Mbalax',
           'Mediatif', u'Mélodie', 'Mental Tribe', 'Menuet', 'Merengue',
           'Messe', 'Messe Pour Orgue', 'Metal', 'Metalcore', 'Milonga',
           'Minimal', 'Motet', 'Murga', 'Musette', 'Ndombolo',
           'Negro Spiritual', 'Neo', 'Neo Metal', 'Neurofunk', 'New Age',
           'Nintendocore', 'Nitzhonot', 'No Wave', 'Nocturne', 'Noise',
           'Noisecore', 'Noisy Pop', 'Nortec', 'Nu Skool Breaks', 'Oi!',
           'Opéra', u'Opéra Ballet', 'Opera Seria', 'Oratorio', 'Ordre',
           'Original Soundtrack', 'Ouverture', 'Ouverture Française',
           'Ouverture Italienne', 'Pachanga', 'Pagan', 'Paillarde', 'Partita',
           'Paso Doble', 'Passacaille', 'Passepied', 'Passion',
           u'Pastorale Héroïque', 'Pavane', 'Pidikhtos', 'Pirate Metal',
           'Polka', 'Polonaise', 'Pop', 'Power Metal', 'Power Noise',
           u'Prélude', 'Psaume', 'Psy', 'Psybient', 'Psybreaks', 'Psyprog',
           'Psytrance Sud-Africaine', 'Pumping Tribe', 'Punk', 'Quatuor',
           'Quintette', 'Rabiz', 'RAC', 'Ragga', 'Raggacore', u'Raï',
           u"Raï'n'b", 'Rap', u'Rap Français', 'Rave', 'Rave Breaks',
           u'Rébétiko', u'Récitatif', 'Reggae', 'Reggaeton', 'Renaissance',
           'Requiem', 'Retro', 'Rhapsodie', 'Rhythm And Blues', 'Ricercare',
           'Rigodon', "R'n'B", 'Rock', "Rock 'n Roll", 'Romantique', 'Ronde',
           'Rondeau', 'Roots', 'Rumba', 'Salsa', 'Salsaton', 'Samba', 'Sambass',
           'Sarabande', 'Saudade', 'Scherzo', 'Schranz', 'Screamo', u'Séga',
           'Seggae', 'Semba', u'Semi-Opéra', u'Sérénade', 'Shibuya-Kei',
           'Shoegaze', 'Sinfonia', 'Sirtaki', 'Ska', 'Skacore', 'Skate Punk',
           'Sketchs', 'Skweee', 'Slam', 'Soca', 'Son Cubain', 'Sonate',
           u"Sonate D'église", 'Songo', 'Soukous', 'Soul', 'Speed Garage',
           'Speed Metal', 'Speedcore', 'Step', 'Suite', 'Suomisaundi', 'Swing',
           'Symphonie', 'Symphonie Concertante', 'Synth', 'Synthcore',
           'Synthwave', 'Tambourin', 'Tango', 'Tango Argentin', 'Tarentelle',
           'Te Deum', 'Teen Pop', 'Tekfunk', 'Terrorcore', 'Thrash Metal',
           'Tiento', 'Timba', 'Toccata', 'Tombeau', u'Tragédie Lyrique',
           'Trailer', 'Trance', 'Trance-Goa', 'Tribal', 'Tribe', 'Tribecore',
           'Trip-Hop', 'Tumba', 'Twee Pop', 'Twist', 'Unblack Metal', 'Valse',
           u'Valse Péruvienne', 'Valse Tyrolienne', 'Variations', u'Vêpres',
           'Viking Metal', 'Visual Kei', 'Washboard', 'Wave', 'World Beat',
           'World Music', 'Worship', 'X-Over', 'Yal', 'Yela', 'Yirmi',
           'Yorkshire Techno', 'Zouglou', 'Zouk', 'Zydeco']:
    DatasetValue.objects.create(dataset=ds_genre_music, value=mg)

#** Models ***************************************
om_movie = Model.objects.create(name='Movie')
om_music = Model.objects.create(name='Music')
om_album = Model.objects.create(name='Album')

#** Models fields ********************************
mgf_description = ModelGlobalField.objects.create(
    name='Description',
    minimum=0,
    maximum=1,
    datatype=dt_string)

mdf_movie_genre = ModelDatasetField.objects.create(
    name='Genre',
    minimum=0,
    maximum=0,
    model=om_movie,
    dataset=ds_genre_movie)

mdf_music_genre = ModelDatasetField.objects.create(
    name='Genre',
    minimum=0,
    maximum=0,
    model=om_music,
    dataset=ds_genre_music)

mdf_album_genre = ModelDatasetField.objects.create(
    name='Genre',
    minimum=0,
    maximum=0,
    model=om_album,
    dataset=ds_genre_music)
